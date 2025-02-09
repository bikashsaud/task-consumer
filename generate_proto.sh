#!/bin/bash

# Set the base directory
BASE_DIR=$(dirname "$(realpath "$0")")
GRPC_DIR="${BASE_DIR}"
SRC_DIR="${GRPC_DIR}/proto"
PY_GEN_PACKAGE_DIR="${GRPC_DIR}/taskconsumerservice/taskpb"

# Ensure the output directory exists
mkdir -p "${PY_GEN_PACKAGE_DIR}"

# Check if the source directory exists
if [ ! -d "${SRC_DIR}" ]; then
  echo "Error: src directory not found at ${SRC_DIR}!"
  exit 1
fi

# Find all .proto files
PROTO_FILES=$(find "${SRC_DIR}" -name '*.proto')

# Check if any .proto files were found
if [ -z "$PROTO_FILES" ]; then
  echo "Error: No .proto files found in ${SRC_DIR}!"
  exit 1
fi

# Generate Python protos and gRPC code
echo "Generating Python protos and RPCs"
python3 -m grpc_tools.protoc \
  --proto_path="${SRC_DIR}" \
  --python_out="${PY_GEN_PACKAGE_DIR}" \
  --grpc_python_out="${PY_GEN_PACKAGE_DIR}" \
  --mypy_out="${PY_GEN_PACKAGE_DIR}" \
  --mypy_grpc_out="${PY_GEN_PACKAGE_DIR}" \
  ${PROTO_FILES}

# Check if the generation was successful
if [ $? -ne 0 ]; then
  echo "Error: Failed to generate Python protos."
  exit 1
fi

# Fix import paths in generated files
echo "Fixing import paths in generated files"
find "${PY_GEN_PACKAGE_DIR}" -name '*.py' -exec sed -i 's/from task import/from taskconsumerservice.taskpb.task import/g' {} +
#find "${PY_GEN_PACKAGE_DIR}" -name '*.py' -exec sed -i 's/import task_pb2/import taskconsumerservice.taskpb.task.task_pb2/g' {} +
echo "Proto generation completed successfully!"