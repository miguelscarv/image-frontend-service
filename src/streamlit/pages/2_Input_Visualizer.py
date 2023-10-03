import streamlit as st
import os
from PIL import Image

EXTRACTED_ZIP_DIR = "./extracted_zip_files/"
SHOW_NUMBER = 9

def show_images(current_time: str) -> None:
    img_path = os.path.join(EXTRACTED_ZIP_DIR, current_time)
    img_list = []
    size = min(SHOW_NUMBER, len(os.listdir(img_path)))
    for i, path in enumerate(os.listdir(img_path)):
        if path.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = Image.open(img_path+"/"+path)
            img_list.append(img)

            if i >= size-1:
                break
    
    col_n = min(3,size)
    cols = st.columns(col_n)
    for i,image in enumerate(img_list):
        cols[i%col_n].image(image, caption=f"Image {i+1}")

st.title("Input Visualizer")

dirs = os.listdir(EXTRACTED_ZIP_DIR)
dirs = [d for d in dirs if d[0] != "."]
dirs.sort(reverse=True)

option = st.selectbox(
    "Choose directory to visualize",
    dirs
)
if option:
    show_images(option)

