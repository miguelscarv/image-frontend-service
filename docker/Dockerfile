# Define workdir folder for all stages
# Must be renewed in the beggining of each stage
ARG WORKSPACE=/workspace
ARG PROTO_FILE=feed.proto

# --------------------------------------
# Builder stage to generate .proto files
# --------------------------------------

FROM python:3.8.7-slim-buster as builder
# Renew build args
ARG WORKSPACE
ARG PROTO_FILE

COPY requirements-build.txt ${WORKSPACE}/

WORKDIR ${WORKSPACE}

RUN pip install --upgrade pip && \
    pip install -r requirements-build.txt && \
    rm requirements-build.txt

# Path for the protos folder to copy
ARG PROTOS_FOLDER_DIR=protos

COPY ${PROTOS_FOLDER_DIR} ${WORKSPACE}/

# Compile proto file and remove it
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ${PROTO_FILE}
