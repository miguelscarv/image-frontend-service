# Feed and Vizualization Component

## Overview

This component launches a Streamlit frontend to vizualise ZIPed inputs (images) and outputs (images as well). Alongside the frontend it also launches a gRPC server that acts like a source and sink, to feed a pipeline with images and to receive images from the end of the pipeline. The it starts in `main.py` where it lauches the gRPC serves and the Streamlit component.

The Streamlit components saves the input extracted images to `extracted_zip_files` and the gRPC server saves the output images to `received_images`. Both the input and output images are saved under a directory corresponding to the current time using unix time stamps. 

When providing a `.json` file with camera intrinsics and other parameters name the images with the camera ID at the end of the file name and separate any other indentifiers with an underscore (`_`). Example: for an image namde `6609_14.jpg`, the gRPC server will look for the key `14` in the `json` file, if it exists and stringify the value corresponding to that key.

## Usage

The asset can be built with the following command:
```shell
$ docker build .
```
and it can be deployed using the command:
```
$ docker run -p 8061:8061 -p 8080:8080 IMAGE
```
The first `-p` is used to expose the 8061 docker port according to AI4EU specs and the second one is for the Streamlit frontend component.

## Creating ZIP files

Depending on the operating system being used you may need create the input zip files differently. This is to avoid creating extra directories inside a zip file - the extraction method used here assumes files are just bellow the parent directory. To create this type of zip file on MACOS you can use the following command:
```shell
$ zip -j NAME.zip NAME/*
```
This is only needed for larger directories.

### Change the following command in `src/main.py` to change max file upload size:
`--server.maxUploadSize SIZE_WANTED`
