# popsign-meow

## Overview

This is a Kedro project, for the "asl-signs" kaggle competition, which was built using `Kedro 0.18.6`. Take a look at the [Kedro documentation](https://kedro.readthedocs.io) to get started.

## Downloading the Data

### Manual

```bash
kaggle competitions download -c asl-signs -p data/01_raw/ && \
  unzip data/01_raw/asl_signs.zip -d data/01_raw/ && \
  rm data/01_raw/asl_signs.zip
```

### With the `data_fetch` pipeline

```bash
kedro run --pipeline data_fetch
```

## Development

### Creating development environment

This project depends on `conda`. To create a `conda` environment with the project and development dependencies, run:

```bash
make environment
```

### Creating a dependencies lockfile

To generate or update the dependency requirements for your project:

```bash
kedro build-reqs
```

This will `pip-compile` the contents of `src/requirements.txt` into a new file `src/requirements.lock`. You can see the output of the resolution by opening `src/requirements.lock`.

After this, if you'd like to update your project requirements, please update `src/requirements.txt` and re-run `kedro build-reqs`.

[Further information about project dependencies](https://kedro.readthedocs.io/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

### Running tests

Run the projects unit tests with:

```bash
kedro test
```

To configure the coverage threshold, go to the `.coveragerc` file.

### How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `context`, `catalog`, and `startup_error`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r src/requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter

You can start a local notebook server with:

```bash
kedro jupyter notebook
```

or if you prefer JupyterLab:

```bash
kedro jupyter lab
```

### IPython

And if you want to run an IPython session:

```bash
kedro ipython
```

### How to convert notebook cells to nodes

You can move notebook code over into a Kedro project structure using a mixture of [cell tagging](https://jupyter-notebook.readthedocs.io/en/stable/changelog.html#release-5-0-0) and Kedro CLI commands.

By adding the `node` tag to a cell and running the command below, the cell's source code will be copied over to a Python file within `src/<package_name>/nodes/`:

```bash
kedro jupyter convert <filepath_to_my_notebook>
```
> *Note:* The name of the Python file matches the name of the original notebook.

Alternatively, you may want to transform all your notebooks in one go. Run the following command to convert all notebook files found in the project root directory and under any of its sub-folders:

```bash
kedro jupyter convert --all
```

### How to ignore notebook output cells in `git`

To automatically strip out all output cell contents before committing to `git`, you can run `kedro activate-nbstripout`. This will add a hook in `.git/config` which will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

### Packaging

[Further information about building project documentation and packaging](https://kedro.readthedocs.io/en/stable/tutorial/package_a_project.html)
