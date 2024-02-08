import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import urllib.request


data = pd.read_csv('vehicles_us.csv')


st.title('Choose your car!')
st.subheader('Use this app to find cars based on your preferences.')


urllib.request.urlretrieve(
    'https://images.cars.com/cldstatic/wp-content/uploads/202301-lead-value-car-winners-scaled.jpg',
    "car_image.png")

img = Image.open("car_image.png")
st.image(img)
st.caption('Choose your parameters here.')


st.header('Filter your preferences')

model_options = data['model'].unique()

selected_models = st.multiselect("Select car models", options=model_options, default=model_options[:5])  

price_range = st.slider("What is your price range?", 1, 375000, (1000, 50000))
actual_range = list(range(price_range[0], price_range[1] + 1))


filtered_data = data[data['price'].isin(actual_range)]

excellent_condition = st.checkbox('Show only cars in excellent condition')
if excellent_condition:
    filtered_data = filtered_data[filtered_data['condition'] == 'excellent']


if not filtered_data.empty:
    st.write('Distribution of Model Years')
    fig = px.histogram(filtered_data, x='model_year')
    st.plotly_chart(fig)

    st.write('Car Price vs. Odometer Reading')
    fig2 = px.scatter(filtered_data, x='odometer', y='price', color='condition', title='Price vs. Odometer Reading')
    st.plotly_chart(fig2)

    st.write('Here is a list of cars matching your preferences')
    st.dataframe(filtered_data.sample(min(len(filtered_data), 20))) 
else:
    st.write("No cars match your preferences.")

 



