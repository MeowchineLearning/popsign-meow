from pathlib import Path
from typing import List
import os
import zipfile

import kaggle


def download_competition_data(competition: str, directory: str = "data/01_raw") -> Path:
    """Downloads data for a Kaggle competition using the Kaggle API.

    Args:
        data_catalog: An instance of Kedro's `DataCatalog`.
        competition: The name of the Kaggle competition to download data for.
        directory: Directory to download to.

    Returns:
        None.

    Raises:
        kaggle.KaggleApiError: If there is an error downloading the competition data.

    """

    # Download the competition data to the data_path directory and unzip it
    filepath = competition + ".zip"
    kaggle.api.competition_download_files(competition, path=directory)

    return Path(directory) / filepath


def unzip_competition_data(filepath: str, directory: str, cleanup: bool = False) -> List[str]:
    directory = directory or str(Path(filepath).parent)
    with zipfile.ZipFile(filepath, "r") as zf:
        filepaths = zf.namelist()
        # Extract all the files in the zip archive
        zf.extractall(path=directory)

    if cleanup:
        # Delete the original zip file
        os.remove(filepath)

    return filepaths
