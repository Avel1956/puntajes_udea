import streamlit as st
import pandas as pd
import plotly.express as px

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

# Main page
st.title('Tablero de Evolución del Programa')
st.write('Datos de inscritos para examen de admisión (primera y segunda opción), admitidos y puntajes de corte, por sede y por programa')
st.write('Fuente de los datos: http://tinyurl.com/puntudea')
# Check if there is data to display
if not filtered_data.empty:
   # Plot for Total Applicants as a bar plot with a trend line
    fig_applicants = px.bar(filtered_data, x='Periodo', y='TOTAL INSCRITOS 1 Y 2 OPCIÓN', title='Total de Inscritos a lo Largo del Tiempo')
    # Add a trend line
    fig_applicants.add_traces(go.Scatter(x=filtered_data['Periodo'], y=filtered_data['TOTAL INSCRITOS 1 Y 2 OPCIÓN'].rolling(window=2).mean(), mode='lines', name='Trend'))
    st.plotly_chart(fig_applicants)

    # Plot for Total Admitted as a bar plot with a trend line
    fig_admitted = px.bar(filtered_data, x='Periodo', y='TOTAL ADMITIDOS', title='Total de Admitidos a lo Largo del Tiempo')
    # Add a trend line
    fig_admitted.add_traces(go.Scatter(x=filtered_data['Periodo'], y=filtered_data['TOTAL ADMITIDOS'].rolling(window=2).mean(), mode='lines', name='Trend'))
    st.plotly_chart(fig_admitted)

    # Plot for Cut-off Score as a bar plot with a trend line
    fig_cutoff = px.bar(filtered_data, x='Periodo', y='PUNTAJE DE CORTE', title='Puntaje de Corte Promedio a lo Largo del Tiempo')
    # Add a trend line
    fig_cutoff.add_traces(go.Scatter(x=filtered_data['Periodo'], y=filtered_data['PUNTAJE DE CORTE'].rolling(window=2).mean(), mode='lines', name='Trend'))
    st.plotly_chart(fig_cutoff)

else:
    st.write("No hay datos disponibles para el programa y sede seleccionados.")
