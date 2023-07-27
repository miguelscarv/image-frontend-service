import streamlit as st
import shutil
import os 
from PIL import Image

INPUT_DIR = "./extracted_zip_files/"
OUTPUT_DIR = "./received_images/"
ZIP_OUTPUT_DIR = "./zip_received_images/"
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


st.title("Delete Output Directories")

out_dirs = os.listdir(OUTPUT_DIR)
out_dirs = [d for d in out_dirs if d[0] != "."]
out_dirs.sort(reverse=True)

out_option = st.selectbox(
"Choose directory to delete",
out_dirs
)

if out_option:
    show_images(out_option, OUTPUT_DIR)

out_button = st.button("Delete", key="out")

if out_button and out_option:
    os.remove(f"{ZIP_OUTPUT_DIR}/{out_option}.zip")
    shutil.rmtree(OUTPUT_DIR+"/"+out_option)
    st.experimental_rerun()