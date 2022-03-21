import streamlit as st
import numpy as np
import pandas as pd
import sqlalchemy as sa
import classes
import config
from sqlalchemy import orm
import pydeck as pdk

st.set_page_config(page_title="Apartment Science", layout="centered")

st.markdown("# Apartment Science")
st.markdown("### A story about the Norwegian housing market")


@st.experimental_singleton
def getSqlEngine():
    return sa.create_engine(config.SQL_ADDRESS, echo=False, future=True)


@st.experimental_memo
def querySqlData(query):
    engine = getSqlEngine()
    with engine.connect() as conn:
        return pd.read_sql(sa.text(query), con=conn)


@st.experimental_memo
def getUniqueBatches():
    return querySqlData("SELECT DISTINCT(_batch) FROM preview")


batch_choice = st.selectbox("Select batch", getUniqueBatches())
st.write("Available features")
st.write(querySqlData("PRAGMA table_info(preview)")[["name", "type"]])

st.write("First 50 data points")
df = querySqlData(
    f"""
SELECT 
    price_suggestion_amount, 
    coordinates_lon as lon,
    coordinates_lat as lat,
    heading,
    image_url
FROM 
    preview 
WHERE 
    _batch = {batch_choice} AND
    price_suggestion_amount IS NOT NULL AND
    price_suggestion_amount > 100000
"""
)

df["price_estimate"] = df["price_suggestion_amount"].apply(lambda x: "{:,.0f} NOK".format(x))

st.write(df.head(50))

view = pdk.data_utils.compute_view(df[["lon", "lat"]])
view.pitch = 40
view.bearing = 0
view.zoom = 4

radius = st.slider(
    "Column radius",
    min_value=10,
    max_value=400,
)

st.pydeck_chart(
    pdk.Deck(
        layers=[
            pdk.Layer(
                type="ColumnLayer",
                data=df,
                get_position=["lon", "lat"],
                get_elevation="price_suggestion_amount",
                elevation_scale=0.005,
                auto_highlight=True,
                pickable=True,
                radius=radius,
                get_color=[255, 255, 255, 100],
            )
        ],
        initial_view_state=view,
        tooltip={
            "html": """
            <div style="max-width: 20rem; font-size: 14px">
                <div>Price suggestion: {price_estimate}</div> 
                <div>{heading}</div> 
                <img style="width: 100%" src={image_url}/>
            <div>"""
        },
        map_provider="mapbox",
    )
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .mapboxgl-control-container {visibility: hidden}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
