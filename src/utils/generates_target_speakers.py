import os
from typing import List
import pandas as pd
from tqdm import tqdm
from .common import convert_audio_to_wav


def load_clips(mcv_dir: str, level: str) -> pd.DataFrame:
    """
    Reads the <level>.tsv file, filters clips for the 'Portuguese (Brasil)' variant,
    and keeps only one record per client_id.
    """
    tsv_file = f"{mcv_dir}/{level}.tsv"
    df = pd.read_csv(tsv_file, sep="\t", encoding="utf-8")

    # Strip whitespace and standardize client_id
    df["client_id"] = df["client_id"].astype(str).str.strip()

    # Filter only Portuguese (Brazil) clips with valid sentences
    df = df[(df["variant"] == "Portuguese (Brasil)") & (df["sentence"].notna())]

    # Keep only one clip per client_id, chosen randomly for diversity
    df = df.groupby("client_id").sample(n=1, random_state=42).reset_index(drop=True)

    return df


def prepare_mcv(mcv_dir: str, level: str) -> None:
    """
    Converts filtered audio clips to WAV mono 16 kHz
    and saves them under datasets/target.
    """
    clips = load_clips(mcv_dir, level)

    out_target = "datasets/target"
    os.makedirs(out_target, exist_ok=True)

    clips_dir = os.path.join(mcv_dir, "clips")
    if not os.path.exists(clips_dir):
        raise FileNotFoundError(f"Directory {clips_dir} not found.")

    # Iterate through clips and convert each to WAV
    for _, row in tqdm(clips.iterrows(), total=len(clips), desc="MCV(Target Speakers) Resampling to mono 16 kHz"):
        input_path = os.path.join(clips_dir, row["path"])
        if not os.path.exists(input_path):
            continue

        dst = os.path.join(out_target, os.path.splitext(row["path"])[0] + ".wav")
        convert_audio_to_wav(input_path, dst)


def prepare_subset_target(mcv_dir: str, level: str) -> None:
    """
    Runs the full pipeline to generate a filtered subset of the MCV dataset.
    """
    prepare_mcv(mcv_dir, level)
