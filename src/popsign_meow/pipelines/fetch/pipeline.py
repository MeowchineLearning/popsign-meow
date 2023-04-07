from kedro.pipeline import Pipeline, node, pipeline

from .nodes import download_competition_data, unzip_competition_data


def create_pipeline() -> Pipeline:
    return pipeline(
        [
            node(
                func=download_competition_data,
                inputs={
                    "competition": "params:competition",
                },
                outputs="competition-zip-data-filepath",
            ),
            node(
                func=unzip_competition_data,
                inputs="competition-zip-data-filepath",
                outputs="competition-data-filepaths",
            ),
        ]
    )
