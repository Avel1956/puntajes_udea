import streamlit as st
import pandas as pd
import plotly.express as px
from plotly import graph_objs as go

def load_data():
    df = pd.read_excel('output/saber_pro_udea.xlsx')
    # Additional data cleaning can be added here if needed
    return df

def show_saber_pro_udea_page():
    st.title('Evolución de Saber Pro en el tiempo')

    df = load_data()

    # Extract year from PERIODO and create a new column 'Year'
    df['Year'] = df['PERIODO'].astype(str).str[:4]

    # Filters
    st.sidebar.header('Filters')
    all_institutions = ['Todos'] + list(df['INST_NOMBRE_INSTITUCION'].unique())
    selected_institution = st.sidebar.selectbox('Select Institution', all_institutions)

    if selected_institution != 'Todos':
        df = df[df['INST_NOMBRE_INSTITUCION'] == selected_institution]
        programs = list(df['ESTU_PRGM_ACADEMICO'].unique())
    else:
        programs = ['Todos'] + list(df['ESTU_PRGM_ACADEMICO'].unique())

    selected_program = st.sidebar.selectbox('Select Program', programs)

    if selected_program != 'Todos':
        df = df[df['ESTU_PRGM_ACADEMICO'] == selected_program]

    # Group by Year and calculate mean score
    df_grouped = df.groupby('Year')['MOD_RAZONA_CUANTITAT_PUNT'].mean().reset_index()

    # Plotting
    if not df.empty:
        # Create bar plot
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_grouped['Year'], y=df_grouped['MOD_RAZONA_CUANTITAT_PUNT'], name='Average Score'))
        
        # Add line plot for variation
        fig.add_trace(go.Scatter(x=df_grouped['Year'], y=df_grouped['MOD_RAZONA_CUANTITAT_PUNT'], 
                                 mode='lines+markers', name='Trend'))

        fig.update_layout(title='Evolution of Scores Over Time', xaxis_title='Year', yaxis_title='Average Score')
        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected filters.")

# Remove the main check if this script is not intended to be run as a standalone Streamlit app
