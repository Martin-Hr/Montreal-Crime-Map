import streamlit as st
import pandas as pd
import pydeck as pdk

# Load the dataset
@st.cache
def load_data():
    data = pd.read_csv("montreal_crime_data.csv")
    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    return data

data = load_data()

# Streamlit app title and description
st.title("Montreal Crime Data Map")
st.markdown("""
This app visualizes crime data in Montreal.
You can filter the data by category, year, city, and neighbourhood.
""")

# Sidebar for filtering options
category = st.sidebar.multiselect('Select Category', data['category'].unique(), default=data['category'].unique())
year = st.sidebar.multiselect('Select Year', data['year'].unique(), default=data['year'].unique())
city = st.sidebar.multiselect('Select City', data['city'].unique(), default=data['city'].unique())
neighbourhood = st.sidebar.multiselect('Select Neighbourhood', data['neighbourhood'].unique(), default=data['neighbourhood'].unique())

# Filter data based on selections
filtered_data = data[(data['category'].isin(category)) & 
                     (data['year'].isin(year)) &
                     (data['city'].isin(city)) & 
                     (data['neighbourhood'].isin(neighbourhood))]

# Define colors for different categories
color_map = {
    'Motor vehicle theft': [255, 0, 0],
    'Home Invasion': [0, 255, 0],
    'Mischief': [0, 0, 255],
    'Theft in / from a motor vehicle': [255, 255, 0],
    'Confirmed Theft': [0, 255, 255],
    'Offenses resulting in death': [255, 0, 255],
}

# Assign colors to categories
filtered_data['color'] = filtered_data['category'].apply(lambda x: color_map.get(x, [255, 255, 255]))

# Define the map layers
layer = pdk.Layer(
    'ScatterplotLayer',
    data=filtered_data,
    get_position='[longitude, latitude]',
    get_fill_color='color',
    get_radius=80,
    pickable=True
)

# Create the map with a different style
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/streets-v11',  # Change map style here
    initial_view_state=pdk.ViewState(
        latitude=filtered_data['latitude'].mean(),
        longitude=filtered_data['longitude'].mean(),
        zoom=11,
        pitch=50,
    ),
    layers=[layer],
))

# Display raw data if checkbox is selected
if st.sidebar.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(filtered_data)
