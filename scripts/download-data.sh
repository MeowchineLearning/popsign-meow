#!/bin/bash

THIS_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${THIS_DIR}/common.sh"

RAW_DATA_DIR=${PROJECT_DIR}/data/01_raw

kaggle competitions download -c asl-signs -p "$RAW_DATA_DIR"
unzip "${RAW_DATA_DIR}/asl_signs.zip" -d "$RAW_DATA_DIR"
rm "${RAW_DATA_DIR}/asl_signs.zip"
