import streamlit as st
import numpy as np
import pandas as pd
import sqlalchemy as sa
import classes
import config
from sqlalchemy import orm
import pydeck as pdk


@st.experimental_singleton
def getSqlEngine():
    return sa.create_engine(config.SQL_ADDRESS, echo=False, future=True)


@st.experimental_memo
def querySqlData(query):
    engine = getSqlEngine()
    with engine.connect() as conn:
        return pd.read_sql(sa.text(query), con=conn)


df = querySqlData(
    """
SELECT 
    price_suggestion_amount, 
    coordinates_lon as lon,
    coordinates_lat as lat     
FROM preview
"""
).dropna(axis=0)

st.write(df)

view = pdk.data_utils.compute_view(df[["lon", "lat"]])
view.pitch = 40
view.bearing = 0

st.pydeck_chart(
    pdk.Deck(
        layers=[
            pdk.Layer(
                type="ColumnLayer",
                data=df,
                get_position=["lon", "lat"],
                get_elevation="price_suggestion_amount",
                elevation_scale=0.01,
                auto_highlight=True,
                pickable=True,
                radius=200,
            )
        ],
        initial_view_state=view,
        tooltip={"html": "<div>Price: {price_suggestion_amount}</div>"},
        map_provider="mapbox",
    )
)
