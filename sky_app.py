import streamlit as st # pip install streamlit
import pandas as pd
import pydeck
import os

st.set_page_config(layout="wide")

# MAPBOX_API_KEY
# os.environ['MAPBOX_API_KEY'] = st.secrets["MAPBOX_API_KEY"]

# Data Load
@st.cache
def get_data():
    df_2019 = pd.read_feather('data_2019.feather')
    df_2020 = pd.read_feather('data_2020.feather')
    return df_2019, df_2020

df_2019, df_2020 = get_data()

df_2019_h = df_2019.query("int_change > 0")
df_2019_m = df_2019.query("int_change == 0")
df_2019_l = df_2019.query("int_change < 0")

df_2020_h = df_2020.query("int_change > 0")
df_2020_m = df_2020.query("int_change == 0")
df_2020_l = df_2020.query("int_change < 0")

# SIDE BAR
# dep = st.sidebar.selectbox("出発:", ['すべて'] + list(df_2020['dep'].unique()))

# arr = st.sidebar.selectbox("到着:", ['すべて'] + list(df_2020['arr'].unique()))

# if (dep == 'すべて') & (arr == 'すべて'):
#     df_data = df_sky
# elif (dep != 'すべて') & (arr == 'すべて'):
#     df_data = df_sky[df_sky['dep']==dep]
# elif (dep == 'すべて') & (arr != 'すべて'):
#     df_data = df_sky[df_sky['arr']==arr]
# else:
#     df_data = df_sky[(df_sky['dep']==dep) & (df_sky['arr']==arr)]

# BODY
## TITLE
st.title('居住都道府県別の延べ宿泊者数（日本人）')

## ArcLayer MAP
WHITE_RGB = (255, 255, 255, 10)
BLUE_RGB = (0, 255, 255, 80)
GREEN_RGB = (0, 255, 0, 80)
RED_RGB = [250, 50, 0, 80]
TOOLTIP_TEXT = {"html": "<b>{pref_name} => {opp_pref_name}</b><br>宿泊者数：{value}人（{year}）"}

def arc_layer(df, layer_RGB, width):
    return pydeck.Layer(
            "ArcLayer",
            data=df,
            get_width=f"{width}",
            get_source_position=["lon", "lat"],
            get_target_position=["opp_pref_lon", "opp_pref_lat"],
            get_tilt=15,
            get_source_color=WHITE_RGB,
            get_target_color=layer_RGB,
            pickable=True,
            auto_highlight=True,
        ),


col1, col2 = st.columns((1, 1))

with col1:
    st.write("２０１８～２０１９年")
    st.pydeck_chart(pydeck.Deck(
        initial_view_state = pydeck.ViewState(
            latitude=34.0,
            longitude=131.0,
            bearing=0,
            pitch=50,
            zoom=4,
        ),

        layers = [
            arc_layer(df_2019_h, RED_RGB, 6),
            arc_layer(df_2019_m, GREEN_RGB, 4),
            arc_layer(df_2019_l, BLUE_RGB, 2),
        ],

        tooltip = TOOLTIP_TEXT,
))
        
with col2:
    st.write("２０１９～２０２０年")
    st.pydeck_chart(pydeck.Deck(
        initial_view_state = pydeck.ViewState(
            latitude=34.0,
            longitude=131.0,
            bearing=0,
            pitch=50,
            zoom=4,
        ),

        layers = [
            arc_layer(df_2020_h, RED_RGB, 6),
            arc_layer(df_2020_m, GREEN_RGB, 4),
            arc_layer(df_2020_l, BLUE_RGB, 2),
        ],

        tooltip = TOOLTIP_TEXT,
))

## Table
col3, col4 = st.columns((1, 1))
with col3:
    df_2019.iloc[:, [1, 3, 5, 4]]
with col4:
    df_2020.iloc[:, [1, 3, 5, 4]]
