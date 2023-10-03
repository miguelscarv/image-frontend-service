import streamlit as st
import os
from PIL import Image
import tempfile
import zipfile

OUTPUT_DIR = "./received_images/"
ZIP_OUTPUT_DIR = "./zip_received_images/"
SHOW_NUMBER = 9

def show_images(current_time: str) -> None:
    img_path = os.path.join(OUTPUT_DIR, current_time)
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
    
    zip_files = os.listdir(ZIP_OUTPUT_DIR)

    if option+".zip" in zip_files:
        #st.write(f"{option} was already computed")

        with open(f"{ZIP_OUTPUT_DIR}/{option}.zip", "rb") as f:
             btn = st.download_button(
                label="Download ZIP",
                data=f,
                file_name=option+".zip",
                mime="application/zip"
            )

    else:
        p = os.path.join(OUTPUT_DIR,option)
        imgs = os.listdir(p)

        with zipfile.ZipFile(f"{ZIP_OUTPUT_DIR}/{option}.zip", "w") as z:
            #st.write(f"Computing ZIP for {option}")
            for img in imgs:
                with open(p+"/"+img, "rb") as f:
                    img_bytes = f.read()
                z.writestr(img, img_bytes)

        with open(f"{ZIP_OUTPUT_DIR}/{option}.zip", "rb") as f:
            btn = st.download_button(
                label="Download ZIP",
                data=f,
                file_name=option+".zip",
                mime="application/zip"
            )

    if btn:
        #st.write(f"Removed {option}")
        os.remove(f"{ZIP_OUTPUT_DIR}/{option}.zip")
    

