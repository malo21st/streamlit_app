import streamlit as st # pip install streamlit
import pandas as pd
import pydeck as pdk
import os

st.set_page_config(layout="wide")

# MAPBOX_API_KEY
os.environ['MAPBOX_API_KEY'] = st.secrets["MAPBOX_API_KEY"]

# Data Load
@st.cache
def get_data():
    df = pd.read_csv('sky.csv')
    return df

df_sky = get_data()

# SIDE BAR
year = st.sidebar.selectbox("西暦:", ["2011", "2012", "2014"])

dep = st.sidebar.selectbox("出発:", ['すべて'] + list(df_sky['dep'].unique()))

arr = st.sidebar.selectbox("到着:", ['すべて'] + list(df_sky['arr'].unique()))

df_sky = df_sky[df_sky['year'] == int(year)]

if (dep == 'すべて') & (arr == 'すべて'):
    df_data = df_sky
elif (dep != 'すべて') & (arr == 'すべて'):
    df_data = df_sky[df_sky['dep']==dep]
elif (dep == 'すべて') & (arr != 'すべて'):
    df_data = df_sky[df_sky['arr']==arr]
else:
    df_data = df_sky[(df_sky['dep']==dep) & (df_sky['arr']==arr)]

# BODY
## TITLE
st.title('日本の空港間流通量')

## ArcLayer MAP
GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]
TOOLTIP_TEXT = {"html": "<b>{dep} => {arr}</b><br>旅客数：{pasN}人<br>貨物量：{crgN}トン<br>距　離：{dist}km<br>頻　度：{freq}本／週"}

col1, col2 = st.columns((1,1))

with col1:
    st.pydeck_chart(pdk.Deck(
        initial_view_state = pdk.ViewState(
            latitude=34.0,
            longitude=131.0,
            bearing=0,
            pitch=50,
            zoom=4,
        ),

        layers = [
            pdk.Layer(
                "ArcLayer",
                data=df_data,
                get_width="3",
                get_source_position=["dep_lon", "dep_lat"],
                get_target_position=["arr_lon", "arr_lat"],
                get_tilt=15,
                get_source_color=RED_RGB,
                get_target_color=GREEN_RGB,
                pickable=True,
                auto_highlight=True,
            ),      
        ],
        tooltip = TOOLTIP_TEXT,
    ))

with col2:
    st.pydeck_chart(pdk.Deck(
        initial_view_state = pdk.ViewState(
            latitude=34.0,
            longitude=131.0,
            bearing=0,
            pitch=50,
            zoom=4,
        ),

        layers = [
            pdk.Layer(
                "ArcLayer",
                data=df_data,
                get_width="3",
                get_source_position=["dep_lon", "dep_lat"],
                get_target_position=["arr_lon", "arr_lat"],
                get_tilt=15,
                get_source_color=RED_RGB,
                get_target_color=GREEN_RGB,
                pickable=True,
                auto_highlight=True,
            ),      
        ],
        tooltip = TOOLTIP_TEXT,
    ))

## Table
df_data
