from locale import DAY_2
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


@st.experimental_memo
def getBatches():
    return querySqlData("SELECT _batch, batch_date FROM preview_meta ORDER BY batch_date DESC")


@st.experimental_memo
def getMaxOf(column: str):
    return querySqlData(f"SELECT MAX({column}) FROM preview").values[0][0]


def getData(batch: int):
    df = querySqlData(
        f"""
    SELECT 
        price_suggestion_amount AS priceEstimate,
        price_total_amount AS priceTotal,
        coordinates_lon AS lon,
        coordinates_lat AS lat,
        CAST(area_range_size_from AS INT) AS size,
        area_range_unit AS sizeUnit,
        heading AS title,
        location AS address,
        image_url AS image
    FROM 
        preview 
    WHERE 
        _batch = {batch} AND
        price_total_amount IS NOT NULL AND
        price_total_amount > 100000 AND
        type = 'realestate' AND
        size IS NOT NULL
    """
    )

    df["priceEstimateStr"] = df["priceEstimate"].apply(lambda x: "{:,.0f} NOK".format(x))
    df["priceTotalStr"] = df["priceTotal"].apply(lambda x: "{:,.0f} NOK".format(x))
    return df


def app():
    st.markdown("# Visualisering av scrapet boligdata")
    batchData = getBatches()
    batchChoice = st.selectbox(
        "Select batch",
        batchData["_batch"],
        index=0,
        format_func=lambda batch: f"{batch}  ({batchData.batch_date.values[-batch - 1]})",
    )

    df = getData(batchChoice)
    st.write(df.describe())

    st.markdown("## Visualization")
    with st.expander("Filters"):
        col1, col2 = st.columns(2)
        with col1:
            minTotPrice = st.number_input(
                "Minimum total price",
                min_value=0,
                max_value=int(getMaxOf("price_total_amount")),
                value=0,
                step=int(getMaxOf("price_total_amount")) // 1000,
            )
        with col2:
            maxTotPrice = st.number_input(
                "Maximum total price",
                min_value=int(minTotPrice),
                max_value=int(getMaxOf("price_total_amount")),
                value=int(getMaxOf("price_total_amount")),
                step=int(getMaxOf("price_total_amount")) // 1000,
            )
        totalPriceRange = (minTotPrice, maxTotPrice)

        col1, col2 = st.columns(2)
        with col1:
            minSize = st.number_input(
                "Minimum size",
                min_value=0,
                max_value=int(df["size"].max()),
                value=0,
                step=int(df["size"].max()) // 1000,
            )
        with col2:
            maxSize = st.number_input(
                "Maximum size",
                min_value=int(minSize),
                max_value=int(df["size"].max()),
                value=int(df["size"].max()),
                step=int(df["size"].max()) // 1000,
            )
        sizeRange = (minSize, maxSize)

    elevationScale = st.number_input("Elevation scale", value=100000, step=10000, min_value=1000)
    radius = st.slider("Column radius", min_value=10, max_value=500, value=200)

    view = pdk.data_utils.compute_view(df[["lon", "lat"]])
    view.pitch = 40
    view.bearing = 0
    view.zoom = 4

    tooltip_html = """
    <div style="max-width: 22rem; font-size: 14px">
        <h1 style="font-size: 1rem; padding: 0;">{address}</h1>
        <div>Price estimate: <b>{priceEstimateStr}</b></div> 
        <div>Price total: <b>{priceTotalStr}</b></div> 
        <div style="margin-bottom: 1rem">Size: <b>{size}{sizeUnit}</b></div> 
        <div>{title}</div> 
        <img style="width: 100%" src={image}/>
    <div>
    """

    df_viz = df.query(
        f"{totalPriceRange[0]} < priceTotal < {totalPriceRange[1]} & {sizeRange[0]} < size < {sizeRange[1]}"
    ).copy()
    df_viz["elevation"] = (df_viz["priceTotal"] - totalPriceRange[0]) / totalPriceRange[1]

    d = pdk.Deck(
        layers=[
            pdk.Layer(
                type="ColumnLayer",
                data=df_viz,
                get_position=["lon", "lat"],
                get_elevation="elevation",
                elevation_scale=elevationScale,
                auto_highlight=True,
                pickable=True,
                radius=radius,
                get_color=[255, 255, 255, 100],
            )
        ],
        initial_view_state=view,
        tooltip={"html": tooltip_html},
        map_provider="mapbox",
    )
    d.deck_widget.on_click(lambda: print("Haha"))
    st.pydeck_chart(d)

    d2 = pdk.Deck(
        layers=[
            pdk.Layer(
                type="HeatmapLayer",
                data=df_viz,
                get_position=["lon", "lat"],
                get_weight="elevation",
                radius_pixels=20,
            )
        ],
        initial_view_state=view,
        tooltip={"html": tooltip_html},
        map_provider="mapbox",
    )
    st.pydeck_chart(d2)


if __name__ == "__main__":
    app()

    st.markdown(
        """
    <style>
        #MainMenu {
            visibility: hidden
        }

        footer {
            visibility: hidden
        }
        
        .mapboxgl-control-container {
            visibility: hidden
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
