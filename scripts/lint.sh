#!/bin/bash

THIS_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${THIS_DIR}/common.sh"

files=$(find "$SRC_DIR" -type f -name "*.py" | sort)
# shellcheck disable=SC2068
pylint --rcfile "$PROJECT_CFG" ${files[@]} && echo "Success"
