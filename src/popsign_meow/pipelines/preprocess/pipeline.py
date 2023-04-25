"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.6
"""

from kedro.config import ConfigLoader
from kedro.pipeline import Pipeline, node, pipeline

from .nodes import preprocess_landmarks, preprocess_signs

config = ConfigLoader("conf").get("parameters/data_processing.yml")


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(func=preprocess_landmarks, inputs="landmarks", outputs="preprocessed_landmarks"),
            node(func=preprocess_signs, inputs="signs", outputs="preprocessed_signs"),
        ]
    )
