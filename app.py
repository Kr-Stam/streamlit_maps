import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from utils import mkd_y, mkd_x, generate_data

st.set_page_config(page_title='Heat map', layout='centered')

df = generate_data()


def geo_with_border():

    tmp=[]
    for i in range(0,10):
        tmp.append(df.query('Time == @i'))
    fig = go.Figure(
        data=[
            go.Scattergeo(
                lon=tmp[0].Longitude,
                lat=tmp[0].Latitude,
                mode='markers',
                showlegend=False
            ),

        ],
        layout=go.Layout(
            title="Frame 0",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])])]
        ),
        frames=[go.Frame(data=[
            go.Scattergeo(
                lon=tmp[i].Longitude,
                lat=tmp[i].Latitude,
                mode='markers',
                showlegend=False
            )
        ],
                         layout=go.Layout(title_text=f"Frame {i}"))
                for i in range(0, 10)]
    )

    fig.add_trace(
        go.Scattergeo(
            lat=mkd_y,
            lon=mkd_x,
            mode='lines',
            line_color='white',
            showlegend=False,
            hoverinfo='skip'
        )
    )
    fig.update_layout(
        dragmode=False,
        geo=dict(
            resolution=50,
            lonaxis_range=[20.3, 23.1],
            lataxis_range=[40.7, 42.5],
            landcolor='rgb(29, 29, 29)',
        )
    )
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    st.plotly_chart(fig)


def density():
    fig = px.density_mapbox(
        data_frame=df,
        lat='Latitude',
        lon='Longitude',
        mapbox_style='carto-darkmatter',
        zoom=6.7,
        radius=20,
        animation_frame='Time'
    )

    fig.update_layout(
        dragmode=False,
        mapbox=dict(
            bounds=dict(
                east=24,
                west=20,
                north=44,
                south=40
            )
        )
    )

    st.plotly_chart(fig)

def st_map():
    tmp=pd.DataFrame(
        {
            'lat' : df.Latitude,
            'lon' : df.Longitude
        }
    )
    st.map(
        tmp
    )

with st.container():
    # st.title="Heat Map Macedonia"
    st.header("Heat Map Macedonia")

    uploaded_file = st.file_uploader('Upload data')

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

    option = st.selectbox(
        'Choose a type of map:',
        ('Plotly Express Density Map', 'Scatter Geo with custom borders', 'Streamlit Map'))

    if option == 'Scatter Geo with custom borders':
        geo_with_border()
    elif option == 'Plotly Express Density Map':
        density()
    elif option == 'Streamlit Map':
        st_map()
