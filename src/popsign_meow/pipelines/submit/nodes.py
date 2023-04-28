from tempfile import NamedTemporaryFile
from zipfile import ZipFile
import shutil

from tensorflow import keras
import tensorflow as tf

from popsign_meow.pipelines.preprocess.features import FeatureGen


class FullModel(keras.Model):
    """
    TensorFlow model that takes input tensors and applies:
        – a preprocessing model
        – the ASL model
    """

    def __init__(self, model):
        """
        Initializes the TFLiteModel with the specified feature generation model and main model.
        """
        super(FullModel, self).__init__()

        # Load the feature generation and main models
        self.prep_inputs = FeatureGen()
        self._model = model

    @tf.function(input_signature=[tf.TensorSpec(shape=[None, 543, 3], dtype=tf.float32, name="inputs")])
    def call(self, inputs):
        """
        Applies the feature generation model and main model to the input tensors.

        Args:
            inputs: Input tensor with shape [batch_size, 543, 3].

        Returns:
            A dictionary with a single key 'outputs' and corresponding output tensor.
        """
        x = self.prep_inputs(tf.cast(inputs, dtype=tf.float32))
        outputs = self._model(x)[0, :]

        # Return a dictionary with the output tensor
        return {"outputs": outputs}


def create_submission(model: keras.Model):
    full_model = FullModel(model)
    tflite_model = tf.lite.TFLiteConverter.from_keras_model(full_model).convert()
    with NamedTemporaryFile("wb") as f:
        f.write(tflite_model)
        with ZipFile("submission.zip", "w") as z:
            z.write(f.name, arcname="model.tflite")
