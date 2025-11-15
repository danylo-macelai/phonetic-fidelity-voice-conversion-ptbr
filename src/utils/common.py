import subprocess


def convert_audio_to_wav(src: str, dst: str, sample_rate: int = 16000) -> bool:
    """
    Converts an audio file to WAV (mono, 16 kHz, 16-bit PCM) using ffmpeg.
    """
    cmd = [
        "ffmpeg",
        "-nostdin",              # Prevents ffmpeg from waiting for input
        "-threads", "0",         # Uses all available CPU threads
        "-i", src,        # Input file
        "-f", "wav",             # Output format
        "-acodec", "pcm_s16le",  # 16-bit PCM
        "-ac", "1",              # Mono
        "-ar", str(sample_rate), # 16 kHz
        "-y",                    # Overwrite output without asking
        dst,
    ]

    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False