import logging

import click

from ect.file_comparison import compare_files

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOGGER = logging.getLogger(__name__)


@click.group()
def cli():
    LOGGER.info("STARTED Environment Comparison Tool")


@cli.command()
@click.option("--env-left", required=True, type=str, help="left env you want to compare")
@click.option("--env-right", required=True, type=str, help="right env you want to compare")
@click.option("--name-dir", required=True, type=str, help="the directory name of the files you want to compare")
def run(
    env_left: str,
    env_right: str,
    name_dir: str,
) -> None:
    """Runs the environment comparison tool"""

    compare_files(
        left_name_env=env_left,
        right_name_env=env_right,
        name_dir=name_dir,
    )


if __name__ == "__main__":
    cli()
