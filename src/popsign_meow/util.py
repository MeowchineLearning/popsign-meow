import os
import random

import numpy as np
import tensorflow as tf


def seed_it_all(seed=7):
    """Attempt to be Reproducible"""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
