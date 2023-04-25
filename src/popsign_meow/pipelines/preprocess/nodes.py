from typing import Callable, Dict

from sklearn.util import resample
import pandas as pd

from popsign_meow.pipelines.util import landmarks_df_to_input_array


def preprocess_landmarks(landmarks: Dict[str, Callable]) -> Dict[str, Callable]:
    result = {key: lambda: landmarks_df_to_input_array(load()) for key, load in landmarks.items()}

    return result


def preprocess_signs(signs: pd.DataFrame, sign_to_index: Dict[str, int]) -> Dict[str, str]:
    signs = signs.assign(path=signs.path.str.removeprefix("train_landmark_files"))
    signs = signs.assign(path=signs.path.str.removesuffix(".parquet"))
    signs = signs.assign(sign=signs.sign.apply(lambda s: sign_to_index[s]))

    return dict(zip(signs.path, signs.sign))


def train_test_split(signs: Dict[str, int], landmarks: Dict[str, Callable]):
    X = np.stack
