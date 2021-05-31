import streamlit as st
import pandas as pd
import numpy as np
import os
import cv2
from os.path import isfile, join
from PIL import Image
import time
from long_exposure_for_streamlit import longExposure
from features import warmImage, coldImage, brightnessControl, changeContrastHSV
@st.cache
def createFolder():
    # Create folder
    MYDIRS = ("imageUpload", "videoUpload", "outputImage")
    for d in MYDIRS:
        CHECK_FOLDER = os.path.isdir(d)
        # If folder doesn't exist, then create it.
        if not CHECK_FOLDER:
            os.makedirs(d)
            print("Created folder : ", d)
        else:
            print(d, "folder already exists.")


@st.cache
def videoProcessing(video, slider=1, hisEqual=False, rgb=[0, 0, 0]):
    return longExposure(video, slider, hisEqual, rgb)

@st.cache
def imageProcessing(image, hisEqual=False, warn=False, cold=False, brightness=0):
    image = cv2.imread(image)
    if hisEqual:
        image = changeContrastHSV(image)
    if warm:
        image = warmImage(image)
    if cold:
        image = coldImage(image)
    re = brightnessControl(image, brightness)
    cv2.imwrite('./outputImage/imageFilter.png', re)
    return './outputImage/imageFilter.png'


# Checkbox Histogram feature
def hisEqual():
    hisEqual = st.sidebar.checkbox("Histogram Equalization ⚖️")
    return hisEqual

# Checkbox Change Color Channel feature
def rgb():
    r = st.sidebar.number_input('Red channel 🔴', min_value=-255, max_value=255, value=0)
    g = st.sidebar.number_input('Green channel 🟩', min_value=-255, max_value=255, value=0)
    b = st.sidebar.number_input('Blue channel 💙', min_value=-255, max_value=255, value=0)
    return r, g, b
def frameRate():
    # Slider frame rate feature
    slider = st.sidebar.slider('Frame rate', 1, 50, 1)
    return slider
def warnAndColdFilter():
    warm = st.sidebar.checkbox('Warm filter 🥵')
    cold = st.sidebar.checkbox('Cold filter 🥶')
    return warm, cold
def brightnessSlider():
    brightness = st.sidebar.slider('Brightness', -50, 50, 0)
    return brightness
def createLongExposure(slider, hisEqual, r, g, b):
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=['.AVI', '.MP4', '.MOV', '.MKV'])
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
        with open(os.path.join("videoUpload", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())      
        st.sidebar.success("Upload successfully")

        button=st.sidebar.button('Create long exposure image')
        if button:
            my_bar = st.progress(0)
            for percent in range(9):
                time.sleep(0.1)
                my_bar.progress(percent*10)
            re = videoProcessing('./videoUpload/{filename}'.format(filename=uploaded_file.name), slider, hisEqual, [r, g, b])
            my_bar.progress(100)
            image = Image.open(re)
            st.image(image)

def imageFilter(hisEqual, warm, cold, brightness):
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=['.PNG', '.JPG', '.JPEG'])
    if uploaded_file is not None:
        file_details = {
            "File Name": uploaded_file.name,
            "File Type": uploaded_file.type,
            "Histogram Equalization": hisEqual,
            "Warm": warm,
            "Cold": cold,
            "Brightness": brightness
        }
        st.sidebar.write(file_details)
        with open(os.path.join("imageUpload", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())      
        st.sidebar.success("Upload successfully")
        button=st.sidebar.button('Image Process')
        if button:
            my_bar = st.progress(0)
            for percent in range(9):
                time.sleep(0.1)
                my_bar.progress(percent*10)
            re = imageProcessing('./imageUpload/{filename}'.format(filename=uploaded_file.name), hisEqual, warm, cold, brightness)
            my_bar.progress(100)
            st.write(re)
            image = Image.open(re)
            st.image(image)

if __name__=="__main__":
    createFolder()
    st.title('Long exposure application 📸')
    option = st.sidebar.selectbox(
        'What do you want me to do?',
        ('Create long exposure image', 'Image filter')
    )
    if option == 'Create long exposure image':
        hisEqual = hisEqual()
        r, g, b = rgb()
        frameRate = frameRate()
        createLongExposure(frameRate, hisEqual, r, g, b)
    elif option == 'Image filter':
        st.sidebar.header('Choose ☝ for best results')
        hisEqual = hisEqual()
        warm, cold = warnAndColdFilter()
        brightness = brightnessSlider()
        imageFilter(hisEqual, warm, cold, brightness)


    path = './greatImage/'
    images = [f for f in os.listdir(path) if isfile(join(path, f))]

    cols = st.beta_columns(3)
    cols[0].image([Image.open(path+images[0]), Image.open(path+images[1]), Image.open(path+images[2])])
    cols[1].image([Image.open(path+images[3]), Image.open(path+images[4]), Image.open(path+images[5])])
    cols[2].image([Image.open(path+images[6]), Image.open(path+images[7]), Image.open(path+images[8])])