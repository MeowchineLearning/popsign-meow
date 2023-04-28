import tensorflow as tf

DROP_Z = False
NUM_FRAMES = 15
SEGMENTS = 3

LEFT_HAND_OFFSET = 468
POSE_OFFSET = LEFT_HAND_OFFSET + 21
RIGHT_HAND_OFFSET = POSE_OFFSET + 33

## average over the entire face, and the entire 'pose'
AVERAGING_SETS = [[0, 468], [POSE_OFFSET, 33]]

# fmt: off
LIP_LANDMARKS = [
    61, 185, 40, 39, 37, 0, 267, 269, 270, 409,
    291, 146, 91, 181, 84, 17, 314, 405, 321, 375,
    78, 191, 80, 81, 82, 13, 312, 311, 310, 415,
    95, 88, 178, 87, 14, 317, 402, 318, 324, 308
]
# fmt: on
LEFT_HAND_LANDMARKS = list(range(LEFT_HAND_OFFSET, LEFT_HAND_OFFSET + 21))
RIGHT_HAND_LANDMARKS = list(range(RIGHT_HAND_OFFSET, RIGHT_HAND_OFFSET + 21))

POINT_LANDMARKS = [item for sublist in [LIP_LANDMARKS, LEFT_HAND_LANDMARKS, RIGHT_HAND_LANDMARKS] for item in sublist]

LANDMARKS = len(POINT_LANDMARKS) + len(AVERAGING_SETS)

if DROP_Z:
    INPUT_SHAPE = (NUM_FRAMES, LANDMARKS * 2)
else:
    INPUT_SHAPE = (NUM_FRAMES, LANDMARKS * 3)

FLAT_INPUT_SHAPE = (INPUT_SHAPE[0] + 2 * (SEGMENTS + 1)) * INPUT_SHAPE[1]


def tf_nan_mean(x, axis=0):
    return tf.reduce_sum(tf.where(tf.math.is_nan(x), tf.zeros_like(x), x), axis=axis) / tf.reduce_sum(
        tf.where(tf.math.is_nan(x), tf.zeros_like(x), tf.ones_like(x)), axis=axis
    )


def tf_nan_std(x, axis=0):
    d = x - tf_nan_mean(x, axis=axis)
    return tf.math.sqrt(tf_nan_mean(d * d, axis=axis))


def flatten_means_and_stds(x, axis=0):
    # Get means and stds
    x_mean = tf_nan_mean(x, axis=axis)
    x_std = tf_nan_std(x, axis=axis)

    x_out = tf.concat([x_mean, x_std], axis=axis)
    x_out = tf.reshape(x_out, (1, INPUT_SHAPE[1] * 2))
    x_out = tf.where(tf.math.is_finite(x_out), x_out, tf.zeros_like(x_out))
    return x_out


class FeatureGen(tf.keras.layers.Layer):
    def __init__(self):
        super(FeatureGen, self).__init__()

    def call(self, x_in):
        if DROP_Z:
            x_in = x_in[:, :, 0:2]

        x_list = [
            tf.expand_dims(tf_nan_mean(x_in[:, av_set[0] : av_set[0] + av_set[1], :], axis=1), axis=1) for av_set in AVERAGING_SETS
        ]
        x_list.append(tf.gather(x_in, POINT_LANDMARKS, axis=1))
        x = tf.concat(x_list, 1)

        x_padded = x
        for i in range(SEGMENTS):
            p0 = tf.where(((tf.shape(x_padded)[0] % SEGMENTS) > 0) & ((i % 2) != 0), 1, 0)
            p1 = tf.where(((tf.shape(x_padded)[0] % SEGMENTS) > 0) & ((i % 2) == 0), 1, 0)
            paddings = [[p0, p1], [0, 0], [0, 0]]
            x_padded = tf.pad(x_padded, paddings, mode="SYMMETRIC")
        x_list = tf.split(x_padded, SEGMENTS)
        x_list = [flatten_means_and_stds(_x, axis=0) for _x in x_list]

        x_list.append(flatten_means_and_stds(x, axis=0))

        ## Resize only dimension 0. Resize can't handle nan, so replace nan with that dimension's avg value to reduce impact.
        x = tf.image.resize(tf.where(tf.math.is_finite(x), x, tf_nan_mean(x, axis=0)), [NUM_FRAMES, LANDMARKS])
        x = tf.reshape(x, (1, INPUT_SHAPE[0] * INPUT_SHAPE[1]))
        x = tf.where(tf.math.is_nan(x), tf.zeros_like(x), x)
        x_list.append(x)
        x = tf.concat(x_list, axis=1)

        return x
