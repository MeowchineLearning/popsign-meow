from functools import partial

from kedro.config import ConfigLoader
from kedro.pipeline import Pipeline, node, pipeline

from .nodes import get_model, model_to_json, plot_model, summarize_model, train_model

params = ConfigLoader("conf").get("parameters/train.yml")


def create_pipeline() -> Pipeline:
    return pipeline(
        [
            node(func=partial(get_model, params=params), name="build_model", inputs=None, outputs="model"),
            node(func=summarize_model, inputs="model", outputs="model_summary"),
            # node(func=plot_model, inputs="model", outputs="model_plot"),
            node(func=model_to_json, inputs="model", outputs="model_json"),
            node(
                func=partial(train_model, params=params),
                name="train_model",
                inputs=["model", "train_X", "train_y", "val_X", "val_y"],
                outputs="trained_model",
            ),
        ]
    )
