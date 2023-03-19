from functools import partial, update_wrapper

from kedro.config import ConfigLoader
from kedro.pipeline import Pipeline, node, pipeline

from .nodes import download_competition_data, unzip_competition_data

config = ConfigLoader("conf").get("pipelines.yml")["data-fetch"]

_download_data = partial(download_competition_data, competition=config["competition"], directory=config["dir"])
_unzip_data = partial(unzip_competition_data, directory=config["dir"])


update_wrapper(_download_data, download_competition_data)
update_wrapper(_unzip_data, unzip_competition_data)


def create_pipeline() -> Pipeline:
    return pipeline(
        [
            node(
                func=_download_data,
                inputs=None,
                outputs="competition-zip-data-filepath",
            ),
            node(
                func=_unzip_data,
                inputs="competition-zip-data-filepath",
                outputs="competition-data-filepaths",
            ),
        ]
    )
