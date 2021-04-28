import streamlit as st
import pandas as pd
import numpy as np
import os
from os.path import isfile, join
from PIL import Image
import time
from forStreamlit import longExposure



st.title('Long exposure application')

@st.cache
def videoProcessing(video, slider, hisEqual, rgb):
    return longExposure(video, slider, hisEqual, rgb)

# Checkbox Histogram feature
hisEqual = st.sidebar.checkbox("Histogram Equalization")
# Checkbox Change Color Channel feature
r = st.sidebar.number_input('Red channel', min_value=0, max_value=255)
g = st.sidebar.number_input('Green channel', min_value=0, max_value=255)
b = st.sidebar.number_input('Yellow channel', min_value=0, max_value=255)
# Slider frame rate feature
slider = st.sidebar.slider('Frame rate', 0, 50, 1)

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    file_details = {
        "File Name": uploaded_file.name,
        "File Type": uploaded_file.type,
        "Frame Rate": slider,
        "Histogram Equalization": hisEqual,
        "Change Color Channel(Plus)": {
            "Red": r,
            "Green": g,
            "Blue": b
        }
    }
    st.sidebar.write(file_details)
    with open(os.path.join("videoUploadFromUser",uploaded_file.name),"wb") as f: 
      f.write(uploaded_file.getbuffer())      
    st.sidebar.success("Upload successfully")

    button=st.sidebar.button('Create')
    if button:
        my_bar = st.progress(0)
        for percent in range(18):
            time.sleep(0.2)
            my_bar.progress(percent*5)
        re = videoProcessing('./videoUploadFromUser/{filename}'.format(filename=uploaded_file.name), slider, hisEqual, [r, g, b])
        my_bar.progress(100)
        st.write(re)
        image = Image.open(re)
        st.image(image)

path = './greatForUser/'
images = [f for f in os.listdir(path) if isfile(join(path, f))]

cols = st.beta_columns(3)
cols[0].image([Image.open(path+images[0]), Image.open(path+images[1]), Image.open(path+images[2])])
cols[1].image([Image.open(path+images[4]), Image.open(path+images[5]), Image.open(path+images[6])])
cols[2].image([Image.open(path+images[3]), Image.open(path+images[7]), Image.open(path+images[8])])