import click
from utils.generates_source_speakers import prepare_subset_source
from utils.generates_target_speakers import prepare_subset_target

@click.group()
def cli():
    """
    Command Line Interface (CLI) for the phonemic post-processing pipeline.

    Available subcommands:

        - prepare    → Generates a filtered subset of the LibriSpeech ASR corpus.
    """


@cli.command(name="prepare")
@click.option(
    "-ls", "--librispeech",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Root directory of the MLS dataset (e.g., D://.../mls_portuguese)."
)
@click.option(
    "-cv", "--commonvoice",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Root directory of the MCV dataset (e.g., D://.../pt)."
)
@click.option(
    "-l", "--level",
    default="dev",
    show_default=True,
    type=click.Choice(["dev", "test", "train"], case_sensitive=False),
    help="Dataset split to use: dev, test, or train. Default is dev."
)
@click.option(
    "-s", "--seconds",
    default=18000,
    show_default=True,
    help="Maximum total audio time in the subset, in seconds (default: 18000 ≈ 5 hours)."
)
def prepare(librispeech: str, commonvoice: str, level: str, seconds: int):
    """
    Generates a filtered subset of the MLS Portuguese dataset.

    Examples:

        python src/main_pipeline.py prepare -ls D://.../mls_portuguese -cv D://.../pt -l dev -s 14400
        python src/main_pipeline.py prepare --dataset     D://.../mls_portuguese  --commonvoice D://.../pt --level dev --seconds 14400
    """
    prepare_subset_source(librispeech, level, seconds)
    prepare_subset_target(commonvoice, level)


if __name__ == "__main__":
    cli()
