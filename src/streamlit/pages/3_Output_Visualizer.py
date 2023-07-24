import streamlit as st
import os
from PIL import Image

OUTPUT_DIR = "./received_images/"
SHOW_NUMBER = 9

def show_images(current_time: str) -> None:
    img_path = os.path.join(OUTPUT_DIR, current_time)
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

#count = st_autorefresh(interval=2000, limit=100, key="output")
st.title("Output Visualizer")

dirs = os.listdir(OUTPUT_DIR)
dirs = [d for d in dirs if d[0] != "."]
dirs.sort(reverse=True)

option = st.selectbox(
    "Choose directory to visualize",
    dirs
)
if option:
    show_images(option)

