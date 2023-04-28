from kedro.pipeline import Pipeline, node, pipeline

from .nodes import build_full_model, create_submission


def create_pipeline() -> Pipeline:
    return pipeline(
        [
            node(create_submission, inputs="trained_model", outputs=None),
        ]
    )
