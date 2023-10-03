import streamlit as st
from zipfile import ZipFile
import os
import time
from PIL import Image
from io import BytesIO
import shutil

EXTRACTED_ZIP_DIR = "./extracted_zip_files/"
ZIP_DIR = "./zip_files/"
SHOW_NUMBER = 3

def extract_zip(zip: BytesIO, current_time: str) -> None:
    new_path = os.path.join(EXTRACTED_ZIP_DIR, current_time)
    os.mkdir(new_path)
    with ZipFile(zip, "r") as f:
        f.extractall(new_path)

    #st.write(os.listdir(new_path))

    for path in os.listdir(new_path):
        temp = new_path+"/"+path
        if os.path.isdir(temp):
            shutil.rmtree(temp)
        elif os.path.isfile(temp) and not temp.lower().endswith(('.png', '.jpg', '.jpeg', '.json')):
            os.remove(temp)

    #st.write(len(os.listdir(new_path)))

def save_zip(zip: BytesIO, current_time: str) -> None:
    with open(f"{ZIP_DIR}{current_time}.zip", "wb") as f:
        f.write(zip.getvalue())

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
    print(col_n)
    cols = st.columns(col_n)
    for i,image in enumerate(img_list):
        cols[i%col_n].image(image, caption=f"Image {i+1}")


st.title("ZIP File Uploader")
#st.warning("Make sure the ZIP file only contains images! (PNG, JPG or JPEG)")

with st.form("my-form", clear_on_submit=True):
    zip = st.file_uploader("Choose ZIP file", type="zip")
    button = st.form_submit_button("Submit")

    if button:
        if zip is not None:
            current_time = str(time.time()).replace(".", "")[:13]
            extract_zip(zip, current_time)
            #save_zip(zip, current_time)

            st.write(f"Submitted {zip.name}")

        else:
            st.error("No ZIP file was uploaded...")

if SHOW_NUMBER > 0 and zip is not None:
    st.header("Images in ZIP")
    show_images(current_time)