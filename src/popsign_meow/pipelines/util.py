import numpy as np
import pandas as pd


def landmarks_df_to_input_array(df: pd.DataFrame, rows_per_frame: int = 543) -> np.ndarray:
    data_columns = ["x", "y", "z"]
    df = df[data_columns]
    n_frames = int(len(df) / rows_per_frame)
    data = df.values.reshape(n_frames, rows_per_frame, len(data_columns))

    return data.astype(np.float32)
