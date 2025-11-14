import click
from utils.dataset_preparation import prepare_subset


@click.group()
def cli():
    """
    Command Line Interface (CLI) for the phonemic post-processing pipeline.

    Available subcommands:

        - prepare    → Generates a filtered subset of the LibriSpeech ASR corpus.
    """


@cli.command(name="prepare")
@click.option(
    "-d", "--dataset",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Root directory of the MLS dataset (e.g., D://.../mls_portuguese)."
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
def prepare(dataset: str, level: str, seconds: int):
    """
    Generates a filtered subset of the MLS Portuguese dataset.

    Examples:

        python src/main_pipeline.py prepare -d D://.../mls_portuguese -l dev -s 14400
        python src/main_pipeline.py prepare --dataset D://.../mls_portuguese --level dev --seconds 14400
    """
    prepare_subset(dataset, level, seconds)


if __name__ == "__main__":
    cli()
