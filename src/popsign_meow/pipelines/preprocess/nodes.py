from functools import partial
from typing import Callable, Dict, Tuple
import random

from numpy.typing import ArrayLike
import numpy as np
import pandas as pd

from popsign_meow.pipelines.preprocess import features
from popsign_meow.pipelines.util import landmarks_df_to_input_array


def landmarks_to_input_array(landmarks: Dict[str, Callable]) -> Dict[str, Callable]:
    def load_to_array(load):
        return landmarks_df_to_input_array(load())

    result = {key: partial(load_to_array, load) for key, load in landmarks.items()}

    return result


def signs_to_indexes(signs: pd.DataFrame, sign_to_index: Dict[str, int]) -> pd.DataFrame:
    signs = signs.assign(path=signs.path.str.removeprefix("train_landmark_files/"))
    signs = signs.assign(path=signs.path.str.removesuffix(".parquet"))
    signs = signs.assign(sign_idx=signs.sign.apply(lambda s: sign_to_index[s]))

    return signs


def generate_features_and_labels(
    landmarks_input_arrays: Dict[str, Callable], signs_indexes: pd.DataFrame
) -> Tuple[ArrayLike, ArrayLike]:
    generate_features = features.FeatureGen()
    X = np.concatenate([generate_features(landmarks_input_arrays[path]()) for path in signs_indexes.path])
    y = signs_indexes.sign_idx.to_numpy()

    return X, y


def split_train_val(X: ArrayLike, y: ArrayLike, val_split: float):
    n = len(y)
    n_train = int((1 - val_split) * n)
    random_idxs = random.sample(range(n), n)
    train_idxs, val_idxs = np.array(random_idxs[:n_train]), np.array(random_idxs[n_train:])

    val_X, val_y = X[val_idxs], y[val_idxs]
    train_X, train_y = X[train_idxs], y[train_idxs]

    return train_X, train_y, val_X, val_y
