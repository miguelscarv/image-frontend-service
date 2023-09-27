# Feed and Vizualization Component

## Overview

This component launches a Streamlit frontend to vizualise ZIPed inputs (images) and outputs (images as well). Alongside the frontend it also launches a gRPC server that acts like a source and sink, to feed a pipeline with images and to receive images from the end of the pipeline. The it starts in `main.py` where it lauches the gRPC serves and the Streamlit component.

The Streamlit components saves the input extracted images to `extracted_zip_files` and the gRPC server saves the output images to `received_images`. Both the input and output images are saved under a directory corresponding to the current time using unix time stamps. 

## Usage

The asset can be built with the following command:
```shell
$ docker build .
```
and it can be deployed using the command:
```
$  docker run -p 8061:8061 -p 8080:8080 IMAGE
```
The first `-p` is used to expose the 8061 docker port according to AI4EU specs and the second one is for the Streamlit frontend component.

### Change the following command in `src/main.py` to change max file upload size:
`--server.maxUploadSize SIZE_WANTED`