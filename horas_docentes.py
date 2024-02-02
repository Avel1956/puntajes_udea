import streamlit as st
import pandas as pd
import plotly.express as px
from plotly import graph_objs as go


# Define the color palette
primary_color = "#34A853"  
secondary_color = "#FFFFFF"  
background_color = "#F5F5F5"  
text_color = "#262730"  


# Custom styles for Plotly charts
def customize_chart(fig):
    fig.update_layout(
        paper_bgcolor=background_color,
        plot_bgcolor=background_color,
        font_color=text_color
    )
    return fig

def show_horas_docente_page():
    st.title("Horas de docencia")
    