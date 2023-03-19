#!/bin/bash

set -eu

SCRIPTS_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PROJECT_DIR=$(readlink -f "${SCRIPTS_DIR}/..")
# shellcheck disable=SC2034
PROJECT_NAME=popsign-meow
# shellcheck disable=SC2034
PROJECT_CFG="${PROJECT_DIR}/pyproject.toml"
# shellcheck disable=SC2034
SRC_DIR="${PROJECT_DIR}/src"
