import streamlit as st
from io import BytesIO

st.sidebar.markdown('# Binarização')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # st.write(bytes_data)
    st.image(bytes_data, width=512)
   
    
x = st.sidebar.slider('x', min_value=2, max_value=256, value=2, step=2)  # 👈 this is a widget

if uploaded_file is not None:
    st.image(bytes_data, width=512)