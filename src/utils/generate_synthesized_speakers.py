import os
import sys
import glob
import shutil
import random
import subprocess
import pandas as pd
from tqdm import tqdm
from pathlib import Path


def load_sources(metadata_csv: str) -> pd.DataFrame:
    """
    Reads metadata_csv and returns a DataFrame containing the filtered source audios.
    """
    if not os.path.exists(metadata_csv):
        raise FileNotFoundError(f"{metadata_csv} not found.")

    return pd.read_csv(metadata_csv, sep="\t", encoding="utf-8")


def sanitize_file_name(source_path: str, target_path: str, output_path: str) -> str:
    """
    Finds the SeedVC generated file and renames it to the original source file name.

    Example:
        vc_12710_10229_000000_common_voice_pt_19273358_1.0_20_0.7.wav
        → 12710_10229_000000.wav
    """
    source_stem = Path(source_path).stem
    target_stem = Path(target_path).stem

    pattern = f"vc_{source_stem}_{target_stem}_*.wav"
    search_path = os.path.join(output_path, pattern)

    matched_files = glob.glob(search_path)

    if not matched_files:
        print(f"[ERROR] Nenhum arquivo encontrado para padrão: {pattern}")
        return None

    # If multiple files, choose the latest one
    final_file_generated = max(matched_files, key=os.path.getmtime)

    final_name = Path(source_path).name
    final_path = os.path.join(output_path, final_name)

    shutil.move(final_file_generated, final_path)
    return final_path


def synthesize_speaker(source_path: str, target_path: str, output_path: str,
                       seedvc_inference: str, diffusion_steps: int = 20,
                       fp16: bool = True) -> str:
    """
    Executes SeedVC inference to synthesize a new voice based on the target speaker.
    """
    cmd = [
        sys.executable,
        seedvc_inference,
        "--source", source_path,
        "--target", target_path,
        "--output", output_path,
        "--diffusion-steps", str(diffusion_steps),
        "--fp16", str(fp16)
    ]

    try:
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        subprocess.run(cmd, check=True, cwd=project_root)

        # Rename final output
        return sanitize_file_name(source_path, target_path, output_path)

    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to synthesize: {source_path}")
        return None


def generate_synthesized_speakers(metadata_csv: str, target_base: str,
                                  output_dir: str, seedvc_inference: str,
                                  metadata_output_csv="outputs/seedvc-metadata.csv") -> None:
    """
    Iterates through all source audios, converts each one using SeedVC, and
    generates a metadata file describing all conversions.
    """
    os.makedirs(output_dir, exist_ok=True)

    df_sources = load_sources(metadata_csv)

    # List target WAV files
    target_files = [
        os.path.join(target_base, f)
        for f in os.listdir(target_base)
        if f.endswith(".wav")
    ]

    if not target_files:
        raise FileNotFoundError(f"No target speaker files found in: {target_base}")

    metadata_rows = []

    for _, row in tqdm(df_sources.iterrows(), total=len(df_sources),
                       desc="Synthesizing voices"):
        source_file = row["audio"]

        if not os.path.exists(source_file):
            print(f"[WARNING] Source audio not found: {source_file}")
            continue

        target_file = random.choice(target_files)

        converted_file = synthesize_speaker(
            source_file, target_file, output_dir, seedvc_inference
        )

        metadata_rows.append({
            "source": source_file,
            "target": target_file,
            "converted": converted_file
        })

    df_meta = pd.DataFrame(metadata_rows)
    df_meta.to_csv(metadata_output_csv, sep="\t", index=False, encoding="utf-8")


def prepare_synthesized_subset(metadata_csv: str = "datasets/source_metadata.csv",
                               target_base: str = "datasets/target",
                               output_dir: str = "outputs/seedvc",
                               seedvc_inference: str = "models/seedvc/inference.py") -> None:
    """
    Runs the full pipeline required to generate a SeedVC-based
    synthesized dataset using pairs of source → target speakers.
    """
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    seedvc_inference_abs = os.path.join(project_root, seedvc_inference)

    generate_synthesized_speakers(
        metadata_csv,
        target_base,
        output_dir,
        seedvc_inference_abs
    )
