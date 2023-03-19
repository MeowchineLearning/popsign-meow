#!/bin/bash

THIS_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${THIS_DIR}/common.sh"

conda create --name "$PROJECT_NAME" python=3.10 pip
conda activate "$PROJECT_NAME"
pip install -r "${SRC_DIR}/requirements.txt"
pip install -r "${SRC_DIR}/requirements.dev"
