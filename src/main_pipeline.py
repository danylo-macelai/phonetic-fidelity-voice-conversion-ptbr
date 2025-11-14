import click
from utils.dataset_preparation import prepare_subset


@click.group()
def cli():
    """
    Interface de linha de comando (CLI) para o pipeline de pós-processamento fonêmico.

    Subcomandos disponíveis:

        - prepare    → Gera um subset filtrado do LibriSpeech ASR corpus.
    """


@cli.command(name="prepare")
@click.option(
    "-l", "--libri_speech_dir",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Diretório raiz do LibriSpeech (por exemplo: D://.../mls_portuguese)."
)
@click.option(
    "-s", "--seconds",
    default=18000,
    show_default=True,
    help="Tempo máximo total de áudio no subset, em segundos (padrão: 18000 ≈ 5 horas)."
)
def prepare(libri_speech_dir: str, seconds: int):
    """
    Gera um subconjunto do dataset LibriSpeech ASR corpus em português do Brasil.

    Exemplos:

        python src/main_pipeline.py prepare -l D://.../mls_portuguese -s 14400
        python src/main_pipeline.py prepare --libri_speech_dir D://.../mls_portuguese --seconds 14400
    """
    prepare_subset(libri_speech_dir, seconds)


if __name__ == "__main__":
    cli()
