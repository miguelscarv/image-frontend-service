#!/bin/bash

cd protos
python3 -m grpc_tools.protoc -I.  --python_out=. --grpc_python_out=. image.proto
mv *.py ../src