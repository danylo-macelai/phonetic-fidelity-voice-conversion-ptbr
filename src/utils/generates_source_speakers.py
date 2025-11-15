import os
from typing import Dict, List, Tuple
from tqdm import tqdm
import pandas as pd
from .common import convert_audio_to_wav

def load_segments(segments_path: str) -> List[Tuple[str, float, float]]:
    """
    Reads segments.txt and returns a list of tuples (clip_id, start_sec, end_sec).
    """
    segs: List[Tuple[str, float, float]] = []
    with open(segments_path, "r", encoding="utf8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 4:
                continue
            cid, _, start, end = parts
            segs.append((cid, float(start), float(end)))
    return segs


def load_transcripts(transcripts_path: str) -> Dict[str, str]:
    """
    Reads transcripts.txt and returns a dictionary {clip_id: sentence}.
    """
    txt: Dict[str, str] = {}
    with open(transcripts_path, "r", encoding="utf8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 2:
                continue
            cid, sentence = parts
            txt[cid] = sentence
    return txt


def index_flacs(audio_dir: str) -> Dict[str, str]:
    """
    Indexes all FLAC audio files inside MLS structure and returns {clip_id: path}.
    """
    idx: Dict[str, str] = {}

    for spk in os.listdir(audio_dir):
        p1 = os.path.join(audio_dir, spk)
        if not os.path.isdir(p1):
            continue

        for book in os.listdir(p1):
            p2 = os.path.join(p1, book)
            if not os.path.isdir(p2):
                continue

            for f in os.listdir(p2):
                if f.endswith(".flac"):
                    clip_id = f[:-5]  # remove .flac
                    idx[clip_id] = os.path.join(p2, f)

    return idx


def prepare_mls(mls_dir: str, level: str, seconds: int) -> None:
    """
    Generates metadata.csv with: [audio_path, transcription, duration_ms] and converts filtered audio
    to WAV mono 16 kHz and saves them under datasets/source.
.    """

    seg_file = f"{mls_dir}/{level}/segments.txt"
    txt_file = f"{mls_dir}/{level}/transcripts.txt"
    segs = load_segments(seg_file)
    texts = load_transcripts(txt_file)

    audio_mls_dir = f"{mls_dir}/{level}/audio"
    flacs = index_flacs(audio_mls_dir)

    out_source = "datasets/source"
    os.makedirs(out_source, exist_ok=True)

    os.makedirs("datasets", exist_ok=True)
    metadata_path = "datasets/source_metadata.csv"

    limit_ms = seconds * 1000
    total_ms = 0

    rows: List[List] = []

    for cid, start, end in tqdm(segs, desc=f"MLS(Source Speakers) Resampling to mono 16 kHz"):
        if cid not in texts or cid not in flacs:
            continue

        dur_ms = int((end - start) * 1000)
        if total_ms + dur_ms > limit_ms:
            continue

        src = flacs[cid]
        dst = f"{out_source}/{cid}.wav"

        if convert_audio_to_wav(src, dst):
            total_ms += dur_ms
            rows.append([dst, texts[cid], dur_ms])

    df = pd.DataFrame(rows, columns=["audio", "transcription", "duration_ms"])
    df.to_csv(metadata_path, sep="\t", index=False)

def prepare_subset_source(mls_dir: str, level: str, seconds: int) -> None:
    """
    Runs the full pipeline to generate a filtered subset of the MLS dataset.
    """
    prepare_mls(
        mls_dir, 
        level, 
        seconds
    )
