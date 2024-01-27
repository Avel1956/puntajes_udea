import streamlit as st
import pandas as pd
import plotly.express as px
from plotly import graph_objs as go

def load_data():
    df = pd.read_excel('output/saber_pro_udea.xlsx')
    return df

def show_saberpro_udea_page():
    st.title('Evolución de Saber Pro en el tiempo')

    df = load_data()

    df['Year'] = df['PERIODO'].astype(str).str[:4]

    # Filters
    st.sidebar.header('Filters')
    all_institutions = ['Todos'] + list(df['INST_NOMBRE_INSTITUCION'].unique())
    selected_institution = st.sidebar.selectbox('Seleccione institución', all_institutions)

    if selected_institution != 'Todos':
        df = df[df['INST_NOMBRE_INSTITUCION'] == selected_institution]
        programs = list(df['ESTU_PRGM_ACADEMICO'].unique())
    else:
        programs = ['Todos'] + list(df['ESTU_PRGM_ACADEMICO'].unique())

    selected_program = st.sidebar.selectbox('Seleccionar programa', programs)

    if selected_program != 'Todos':
        df = df[df['ESTU_PRGM_ACADEMICO'] == selected_program]

    # Explicitly specify MOD columns
    mod_columns = [
        'MOD_RAZONA_CUANTITAT_PUNT', 'MOD_COMUNI_ESCRITA_PUNT', 'MOD_COMUNI_ESCRITA_DESEM',
        'MOD_LECTURA_CRITICA_PUNT', 'MOD_INGLES_PUNT', 'MOD_COMPETEN_CIUDADA_PUNT'
    ]

    # Group by year and calculate mean for each MOD column
    df_grouped = df.groupby('Year')[mod_columns].mean().reset_index()

    # Plotting
    if not df.empty:
        # Create figure
        fig = go.Figure()

        # Add a trace for each MOD column
        for col in mod_columns:
            fig.add_trace(go.Scatter(x=df_grouped['Year'], y=df_grouped[col], 
                                     mode='lines+markers', name=col))

        fig.update_layout(title='Evolución de puntajes', xaxis_title='Año', yaxis_title='Promedio')
        st.plotly_chart(fig)

        # Display statistics for categorical data
        categorical_stats = df.describe(include=['O'])
        st.write("EStadísticas para datos categóricos:")
        st.dataframe(categorical_stats)

    else:
        st.write("Ningún dato satisface los filtros seleccionados.")

# ... [rest of your code, if any] ...
