import streamlit as st
import pandas as pd
import plotly.express as px
from plotly import graph_objs as go

# Load your data
@st.cache_data
def load_data():
    # Adjust the path to your file
    df = pd.read_excel('output/consolidated_data.xlsx', sheet_name='Sheet1')
    # Convert 'Periodo' to a format that distinguishes semesters
    df['Periodo'] = df['Periodo'].apply(lambda x: '{}-{}'.format(x.split('-')[0], '01' if x.endswith('1') else '06'))
    # Ensure 'Periodo' is treated as a datetime
    df['Periodo'] = pd.to_datetime(df['Periodo'])
    return df

data = load_data()

# Sidebar for filters
st.sidebar.header('Filtros')
# Select SEDE first
selected_campus = st.sidebar.selectbox('Selecciona la Sede', ['TODOS'] + data['SEDE'].unique().tolist())

# Based on SEDE selection, present PROGRAMA options
if selected_campus == 'TODOS':
    selected_program = st.sidebar.selectbox('Selecciona el Programa', ['TODOS'])
else:
    programs = ['TODOS'] + data[data['SEDE'] == selected_campus]['NOMBRE PROGRAMA'].unique().tolist()
    selected_program = st.sidebar.selectbox('Selecciona el Programa', programs)

# Filtering the data
if selected_campus == 'TODOS' and selected_program == 'TODOS':
    filtered_data = data.copy()
elif selected_campus != 'TODOS' and selected_program == 'TODOS':
    filtered_data = data[data['SEDE'] == selected_campus]
else:
    filtered_data = data[(data['NOMBRE PROGRAMA'] == selected_program) & (data['SEDE'] == selected_campus)]

# Aggregate data if "TODOS" is selected
if selected_program == 'TODOS':
    filtered_data = filtered_data.groupby('Periodo').agg({'TOTAL INSCRITOS 1 Y 2 OPCIÓN': 'sum',
                                                          'TOTAL ADMITIDOS': 'sum',
                                                          'PUNTAJE DE CORTE': 'mean'}).reset_index()

# Sort the filtered data by 'Periodo'
filtered_data = filtered_data.sort_values('Periodo')

def calculate_variations(df, column_name):
    non_null_data = df[df[column_name].notna()]
    if non_null_data.empty:
        return None, None, None, None
    initial_value = non_null_data[column_name].iloc[0]
    final_value = non_null_data[column_name].iloc[-1]
    absolute_variation = final_value - initial_value
    percentage_variation = ((final_value - initial_value) / initial_value) * 100 if initial_value else 0
    return initial_value, final_value, absolute_variation, percentage_variation

# Main page
st.title('Tablero de Evolución del Programa')
st.write('Datos de inscritos para examen de admisión (primera y segunda opción), admitidos y puntajes de corte, por sede y por programa')
st.write('Fuente de los datos: http://tinyurl.com/puntudea')
# Check if there is data to display
if not filtered_data.empty:
    col1, col2, col3 = st.columns(3)
    statistics = {}

    for parameter in ['TOTAL INSCRITOS 1 Y 2 OPCIÓN', 'TOTAL ADMITIDOS', 'PUNTAJE DE CORTE']:
        initial, final, abs_variation, perc_variation = calculate_variations(filtered_data, parameter)
        if initial is not None:
            statistics[parameter] = {
                "initial": initial,
                "final": final,
                "abs_variation": abs_variation,
                "perc_variation": perc_variation
            }

    if statistics:
        with col1:
            st.metric(label="Inscritos Inicial", value=statistics['TOTAL INSCRITOS 1 Y 2 OPCIÓN']['initial'])
            st.metric(label="Inscritos Final", value=statistics['TOTAL INSCRITOS 1 Y 2 OPCIÓN']['final'])
        with col2:
            st.metric(label="Admitidos Inicial", value=statistics['TOTAL ADMITIDOS']['initial'])
            st.metric(label="Admitidos Final", value=statistics['TOTAL ADMITIDOS']['final'])
        with col3:
            st.metric(label="Puntaje Corte Inicial", value=f"{statistics['PUNTAJE DE CORTE']['initial']:.2f}")
            st.metric(label="Puntaje Corte Final", value=f"{statistics['PUNTAJE DE CORTE']['final']:.2f}")

    # Plot for Total Applicants as a bar plot
    fig_applicants = px.bar(filtered_data, x='Periodo', y='TOTAL INSCRITOS 1 Y 2 OPCIÓN', title='Total de Inscritos a lo Largo del Tiempo')
    st.plotly_chart(fig_applicants)

    # Plot for Total Admitted as a bar plot
    fig_admitted = px.bar(filtered_data, x='Periodo', y='TOTAL ADMITIDOS', title='Total de Admitidos a lo Largo del Tiempo')
    st.plotly_chart(fig_admitted)

    # Plot for Cut-off Score as a bar plot
    fig_cutoff = px.bar(filtered_data, x='Periodo', y='PUNTAJE DE CORTE', title='Puntaje de Corte Promedio a lo Largo del Tiempo')
    st.plotly_chart(fig_cutoff)

else:
    st.write("No hay datos disponibles para el programa y sede seleccionados.")
