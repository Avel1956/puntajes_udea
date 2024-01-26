import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    # Load and preprocess the data
    df = pd.read_excel('output/saber_pro_udea.xlsx')
    # Consider adding data cleaning and aggregation logic here
    return df

def show_saber_pro_udea_page():
    st.title('Evolución de Saber Pro en el tiempo')

    df = load_data()

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

    # Assuming 'MOD_RAZONA_CUANTITAT_PUNT' as the score to visualize
    if not df.empty:
        df_grouped = df.groupby('PERIODO')['MOD_RAZONA_CUANTITAT_PUNT'].mean().reset_index()
        fig = px.line(df_grouped, x='PERIODO', y='MOD_RAZONA_CUANTITAT_PUNT', title='Evolution of Scores Over Time')
        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected filters.")


