from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    generate_features_and_labels,
    landmarks_to_input_array,
    signs_to_indexes,
    split_train_val,
)


def create_pipeline() -> Pipeline:
    return pipeline(
        [
            node(func=landmarks_to_input_array, inputs="landmarks", outputs="landmarks_input_arrays"),
            node(func=signs_to_indexes, inputs=["signs", "sign_to_index"], outputs="signs_indexes"),
            node(
                func=generate_features_and_labels,
                inputs=["landmarks_input_arrays", "signs_indexes"],
                outputs=["feature_data", "feature_labels"],
            ),
            node(
                func=split_train_val,
                inputs=["feature_data", "feature_labels", "params:val_split"],
                outputs=["train_X", "train_y", "val_X", "val_y"],
            ),
        ]
    )
