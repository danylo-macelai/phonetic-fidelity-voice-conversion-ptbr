import os
import sys

def prepare_subset(libri_speech_dir: str, seconds: int = 18000) -> None:
    """Executa o pipeline completo de criação do subset filtrado do LibriSpeech."""

    # Verifica se o diretório existe
    if not os.path.isdir(libri_speech_dir):
        print(f"[ERRO] O diretório informado não existe: {libri_speech_dir}")
        sys.exit(1)

    print(f"[OK] Diretório encontrado: {libri_speech_dir}")
    print(f"[INFO] Tempo máximo configurado: {seconds} segundos")