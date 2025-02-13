
from . import features

from typing import *

import concurrent
import itertools
import pathlib
import click
import sys
import os


_DEF_BLOCK    = 10000
_DEF_OUT_PATH = "out.csv"
_DEF_WORKERS  = os.cpu_count()


@click.group()
def cli():
    pass


def process_url(url: str) -> str:
    """
    Process a single URL and convert it into a CSV string of its
    features.

    This function attempts to create a `Features` object from the URL
    (after stripping whitespace) and then returns its string
    representation. If the URL is invalid, it returns an empty string.

    Args:
        url (str): The URL string to process.

    Returns:
        str: A comma-separated string of features as defined by
        `Features.__str__()`, or an empty string if an error occurs.
    """
    try:
        return str(features.Features(url.strip()))
    except features.url.InvalidURL:
        pass 
    return ""


def parse_urls(inpth: pathlib.Path, outpth: pathlib.Path, block: int, workers: int) -> None:
    """
    Extract features from URLs read from an input file and write them
    to an output CSV file.

    The function reads the input file in blocks. Each URL is processed
    concurrently using a ThreadPoolExecutor with the provided number
    of worker threads. The CSV header, obtained via `Features.schema()`, 
    is written first, followed by the processed feature strings.

    Args:
        inpth (pathlib.Path): Path to the input file containing URLs
        (one per line).

        outpth (pathlib.Path): Path to the output CSV file.
        block (int): Number of URLs to process per block.
        workers (int): Number of worker threads to use for parallel
        processing.
    """
    exc = concurrent.futures.ThreadPoolExecutor(max_workers=workers)
    try:
        with inpth.open(mode="r") as infile, outpth.open(mode="w") as outfile:
            outfile.write(features.Features.schema() + "\n")
            while True:
                lines = list(itertools.islice(infile, block))
                if not lines:
                    break

                res = exc.map(process_url, lines)
                outfile.write("\n".join(list(res)))

    except Exception as e:
        click.echo(f"Error: {e}", file=sys.stderr)

    finally:
        exc.shutdown()


@cli.command()
@click.option("--path"   , required=True)
@click.option("--out"    , default =_DEF_OUT_PATH)
@click.option("--block"  , default =_DEF_BLOCK  , type=int)
@click.option("--workers", default =_DEF_WORKERS, type=int)
def extract(path: str, out: str, block: int, workers: int) -> None:
    """
    Extract features from a file of URLs and write them to a 
    CSV file.

    Args:
        path (str): Path to the input file containing URLs.
        out (str): Path to the output CSV file.
        block (int): Number of URLs to process per block.
        workers (int): Number of worker threads for parallel
        processing.
    """

    outpth = pathlib.Path(out)
    inpth  = pathlib.Path(path)

    if inpth.exists() and inpth.is_file():
        parse_urls(inpth, outpth, block, workers)


if __name__ == "__main__":
    cli()
