#!/bin/bash

THIS_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${THIS_DIR}/common.sh"

find "$SRC_DIR" -type f -name "*.py" -exec black --config "$PROJECT_CFG" {} + -exec isort --sp "$PROJECT_CFG" --src "$SRC_DIR" {} +
