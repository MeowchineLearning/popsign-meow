from contextlib import redirect_stdout
from io import StringIO

from numpy.typing import ArrayLike
from tensorflow.keras import callbacks, layers, utils
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam


def get_model(params):
    n_inputs = params["n_inputs"]
    n_layers = params["n_layers"]
    n_labels = params["n_labels"]
    dropouts = params["dropouts"]
    starting_layer_size = params["starting_layer_size"]

    inputs = layers.Input(shape=(n_inputs,))

    def fc_block(inputs, output_channels, dropout):
        x = layers.Dense(output_channels)(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.Activation("gelu")(x)
        x = layers.Dropout(dropout)(x)
        return x

    x = inputs
    for i in range(n_layers):
        x = fc_block(x, output_channels=starting_layer_size // (2**i), dropout=dropouts[i])

    outputs = layers.Dense(n_labels, activation="softmax")(x)

    model = Model(inputs=inputs, outputs=outputs)

    return model


def train_model(model: Model, train_X: ArrayLike, train_y: ArrayLike, val_X: ArrayLike, val_y: ArrayLike, params):
    model.compile(Adam(params["learning_rate"]), "sparse_categorical_crossentropy", metrics="acc")
    cb_list = [
        callbacks.EarlyStopping(patience=params["es_patience"], restore_best_weights=True, verbose=1),
        callbacks.ReduceLROnPlateau(patience=params["rp_patience"], factor=params["rp_reduction_factor"], verbose=1),
    ]
    model.fit(
        train_X,
        train_y,
        validation_data=(val_X, val_y),
        epochs=params["epochs"],
        callbacks=cb_list,
        batch_size=params["batch_size"],
    )

    return model


def summarize_model(model: Model):
    s = StringIO()
    with redirect_stdout(s):
        model.summary()
    s.seek(0)
    return s.read()


def model_to_json(model: Model):
    return model.to_json()


def plot_model(model: Model):
    return utils.plot_model(model)
