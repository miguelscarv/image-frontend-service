import streamlit as st
import shutil
import os 
from PIL import Image

INPUT_DIR = "./extracted_zip_files/"
OUTPUT_DIR = "./received_images/"
SHOW_NUMBER = 9

def show_images(current_time: str, dir: str) -> None:
    img_path = os.path.join(dir, current_time)
    img_list = []
    size = min(SHOW_NUMBER, len(os.listdir(img_path)))
    for i, path in enumerate(os.listdir(img_path)):
        img = Image.open(img_path+"/"+path)
        img_list.append(img)

        if i >= size-1:
            break
    
    col_n = min(3,size)
    cols = st.columns(col_n)
    for i,image in enumerate(img_list):
        cols[i%col_n].image(image, caption=f"Image {i+1}")

st.title("Delete Input and Output Directories")


st.header("Input")
with st.form("in", clear_on_submit=True):
    in_dirs = os.listdir(INPUT_DIR)
    in_dirs = [d for d in in_dirs if d[0] != "."]
    in_dirs.sort(reverse=True)

    option = st.selectbox(
    "Choose directory to delete",
    in_dirs
    )

    if option:
        show_images(option, INPUT_DIR)

    button = st.form_submit_button("Delete")

    if button and option:
        shutil.rmtree(INPUT_DIR+"/"+option)


st.header("Output")
with st.form("out", clear_on_submit=True):
    in_dirs = os.listdir(OUTPUT_DIR)
    in_dirs = [d for d in in_dirs if d[0] != "."]
    in_dirs.sort(reverse=True)

    option = st.selectbox(
    "Choose directory to delete",
    in_dirs
    )

    if option:
        show_images(option, OUTPUT_DIR)

    button = st.form_submit_button("Delete")

    if button and option:
        shutil.rmtree(OUTPUT_DIR+"/"+option)