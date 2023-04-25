import tensorflow as tf


class PrepInputs(tf.keras.layers.Layer):
    def __init__(self, face_idx_range=(0, 468), lh_idx_range=(468, 489), pose_idx_range=(489, 522), rh_idx_range=(522, 543)):
        super(PrepInputs, self).__init__()
        self.idx_ranges = [face_idx_range, lh_idx_range, pose_idx_range, rh_idx_range]
        self.flat_feat_lens = [3 * (stop - start) for start, stop in self.idx_ranges]

    def call(self, X_in):
        # Split the single vector into 4
        X_split = [X_in[:, start:stop, :] for start, stop in self.idx_ranges]

        # Reshape based on specific number of keypoints
        X_split = [tf.reshape(_X, (-1, flat_feat_len)) for _X, flat_feat_len in zip(X_split, self.flat_feat_lens)]

        # Drop empty rows - Empty rows are present in
        #   --> pose, lh, rh
        #   --> so we don't have to for face
        X_split[1:] = [tf.boolean_mask(_X, tf.reduce_all(tf.logical_not(tf.math.is_nan(_X)), axis=1), axis=0) for _X in X_split[1:]]

        X_means = [tf.math.reduce_mean(_X, axis=0) for _X in X_split]
        X_stds = [tf.math.reduce_std(_X, axis=0) for _X in X_split]

        X_out = tf.concat([*X_means, *X_stds], axis=0)
        X_out = tf.where(tf.math.is_finite(X_out), X_out, tf.zeros_like(X_out))

        return tf.expand_dims(X_out, axis=0)


class TFLiteModel(tf.Module):
    """
    TensorFlow Lite model that takes input tensors and applies:
        – a preprocessing model
        – the ISLR model
    """

    def __init__(self, islr_model):
        """
        Initializes the TFLiteModel with the specified preprocessing model and ISLR model.
        """
        super(TFLiteModel, self).__init__()

        # Load the feature generation and main models
        self.prep_inputs = PrepInputs()
        self.islr_model = islr_model

    @tf.function(input_signature=[tf.TensorSpec(shape=[None, 543, 3], dtype=tf.float32, name="inputs")])
    def __call__(self, inputs):
        """
        Applies the feature generation model and main model to the input tensors.

        Args:
            inputs: Input tensor with shape [batch_size, 543, 3].

        Returns:
            A dictionary with a single key 'outputs' and corresponding output tensor.
        """
        x = self.prep_inputs(tf.cast(inputs, dtype=tf.float32))
        outputs = self.islr_model(x)[0, :]

        # Return a dictionary with the output tensor
        return {"outputs": outputs}
