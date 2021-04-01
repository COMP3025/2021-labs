import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from PIL import Image

uploaded_file = st.sidebar.file_uploader("Escolha a imagem", type=['png', 'jpg'])

image = None

if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    file_extension = uploaded_file.name.split('.')[-1]
    image = Image.open(uploaded_file)
    st.markdown(f'### Imagem original')
    st.image(bytes_data, width=512)

option = st.sidebar.radio(
    'Escolha a transformação',
    ('Tons de cinza', 'Negativo', 'Sub', 'Log', 'Gamma', 
    'Alongamento', 'Corte')
)

st.markdown(f'### {option}')

if image is not None:
    img_gray = np.asarray(image).mean(axis=2)
    if option == 'Tons de cinza':
        st.image(Image.fromarray(img_gray).convert('L'))
    elif option == 'Negativo':
        img_gray = 255 - img_gray
        st.image(Image.fromarray(img_gray).convert('L'))
    elif option == 'Sub':
        value = st.sidebar.slider('Valor', 0, 255, 255)
        img_gray = value - img_gray
        st.image(Image.fromarray(img_gray).convert('L'))
    elif option == 'Log':
        st.sidebar.latex(r'''
            s = c * log(1 + r)
        ''')
        
        c = st.sidebar.slider('Valor de c', 0, 200, 1)
        img_gray = c * (np.log(img_gray + 1))
        st.image(Image.fromarray(img_gray).convert('L'))

        # plotly -- ficou pesado!
        # hist_data = img_gray.flatten()
        # fig = ff.create_distplot([hist_data], ['image'], bin_size=[.25])
        # st.plotly_chart(fig, use_container_width=True)

        # matplot
        # fig, ax = plt.subplots()
        # ax.hist(img_gray.flatten(), bins=25)
        # st.sidebar.pyplot(fig)
    elif option == 'Gamma':
        st.sidebar.latex(r'''
            s = c * r^\gamma
        ''')
        c = st.sidebar.slider('Valor de c', 0., 20., 1., 0.2)
        gamma = st.sidebar.slider('Valor de gamma', 0.0, 30.0, 1.0, 0.02)

        img_gray = c * (img_gray ** gamma)
        st.image(Image.fromarray(img_gray).convert('L'))

        # fig, ax = plt.subplots()
        # ax.hist(img_gray.flatten(), bins=25)
        # st.sidebar.pyplot(fig)

    elif option == 'Alongamento':
        up = st.sidebar.slider('up', 0, 255, 255)
        down = st.sidebar.slider('down', 0, 255, 0)
        intervals = st.sidebar.slider('Intervalo', 0, 255, (0, 255))
        st.write(f'up: {up}, down: {down}, {intervals} ')
        img_gray[img_gray < intervals[0]] = down
        img_gray[img_gray > intervals[1]] = down
        img_gray[(img_gray >= intervals[0]) & (img_gray <= intervals[1])] = up
        neg = 255 - img_gray
        st.image(Image.fromarray(img_gray).convert('L'), width = 256)
        st.image(Image.fromarray(neg).convert('L'), width = 256)

    elif option == 'Corte':
        up = st.sidebar.slider('up', 0, 255, 255)
        intervals = st.sidebar.slider('Intervalo', 0, 255, (0, 255))

        img_gray[(img_gray >= intervals[0]) & (img_gray <= intervals[1])] = up

        neg = 255 - img_gray
        st.image(Image.fromarray(img_gray).convert('L'))
        st.image(Image.fromarray(neg).convert('L'))