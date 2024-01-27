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

def show_puntajes_udea_page():


    # Load  data
    @st.cache_data
    def load_data():
        # Adjust the path to  file
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

    def calculate_variations(df, column_name, last_period_with_data=None):
        non_null_data = df[df[column_name].notna()]
        if last_period_with_data:
            non_null_data = non_null_data[non_null_data['Periodo'] <= last_period_with_data]
        if non_null_data.empty:
            return None, None, None, None
        initial_value = non_null_data[column_name].iloc[0]
        final_value = non_null_data[column_name].iloc[-1]
        absolute_variation = final_value - initial_value
        percentage_variation = ((final_value - initial_value) / initial_value) * 100 if initial_value else 0
        return initial_value, final_value, absolute_variation, percentage_variation

    def calculate_program_variations(df, sede):
        # Filter the data for the given SEDE
        sede_data = df[df['SEDE'] == sede]
        # Calculate the first and last Puntaje de Corte for each program within the SEDE
        program_variations = sede_data.groupby('NOMBRE PROGRAMA')['PUNTAJE DE CORTE'].agg(['first', 'last'])
        # Calculate the variation and sort the programs
        program_variations['Variation'] = program_variations['last'] - program_variations['first']
        program_variations = program_variations.sort_values(by='Variation', ascending=False)
        return program_variations

    # Último periodo con datos para inscritos y admitidos
    last_period_with_data = pd.to_datetime('2022-06')  # Assuming '2022-2' corresponds to June 2022

    # Main page
    st.markdown(f"<h1 style='color: {primary_color};'>Tablero de Evolución del Programa</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color: {text_color};'>Datos de inscritos para examen de admisión (primera y segunda opción), admitidos y puntajes de corte, por sede y por programa</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {text_color};'>Fuente de los datos: <a href='http://tinyurl.com/puntudea' target='_blank'>UdeA Data Source</a></p>", unsafe_allow_html=True)

    # Check if there is data to display
    if not filtered_data.empty:
        col1, col2, col3 = st.columns(3)
        statistics = {}

        parameters = {
            'TOTAL INSCRITOS 1 Y 2 OPCIÓN': last_period_with_data,
            'TOTAL ADMITIDOS': last_period_with_data,
            'PUNTAJE DE CORTE': None  # Assuming we have all data for 'PUNTAJE DE CORTE'
        }

        for parameter, last_period in parameters.items():
            initial, final, abs_variation, perc_variation = calculate_variations(filtered_data, parameter, last_period)
            if initial is not None:
                statistics[parameter] = {
                    "initial": initial,
                    "final": final,
                    "abs_variation": abs_variation,
                    "perc_variation": perc_variation
                }

        if statistics:
            with col1:
                st.metric(label="Inscritos periodo 2019-1", value=statistics['TOTAL INSCRITOS 1 Y 2 OPCIÓN']['initial'])
                st.metric(label="Inscritos periodo 2022-2", value=statistics['TOTAL INSCRITOS 1 Y 2 OPCIÓN']['final'])
                st.metric(label="Variación Inscritos", value=f"{statistics['TOTAL INSCRITOS 1 Y 2 OPCIÓN']['perc_variation']:.2f}%", delta_color="off")
            with col2:
                st.metric(label="Admitidos periodo 2019-1", value=statistics['TOTAL ADMITIDOS']['initial'])
                st.metric(label="Admitidos periodo 2022-2", value=statistics['TOTAL ADMITIDOS']['final'])
                st.metric(label="Variación Admitidos", value=f"{statistics['TOTAL ADMITIDOS']['perc_variation']:.2f}%", delta_color="off")
            with col3:
                st.metric(label="Puntaje Corte periodo 2019-1", value=f"{statistics['PUNTAJE DE CORTE']['initial']:.2f}")
                st.metric(label="Puntaje Corte periodo 2024-1", value=f"{statistics['PUNTAJE DE CORTE']['final']:.2f}")
                st.metric(label="Variación Puntaje", value=f"{statistics['PUNTAJE DE CORTE']['perc_variation']:.2f}%", delta_color="off")

        if selected_campus != 'TODOS':
            program_variations = calculate_program_variations(data, selected_campus)
            top_five = program_variations.nlargest(5, 'Variation')
            bottom_five = program_variations.nsmallest(5, 'Variation')

            st.markdown("## Ranking de Programas por Variación de Puntaje de Corte en " + selected_campus)
            st.markdown("### Top 5 Programas con Mayor Aumento")
            for program in top_five.index:
                st.markdown(f"- {program}: {top_five.loc[program, 'Variation']:.2f} puntos")

            st.markdown("### Bottom 5 Programas con Mayor Disminución")
            for program in bottom_five.index:
                st.markdown(f"- {program}: {bottom_five.loc[program, 'Variation']:.2f} puntos")

        # Plot for Total Applicants as a bar plot
        fig_applicants = customize_chart(px.bar(filtered_data, x='Periodo', y='TOTAL INSCRITOS 1 Y 2 OPCIÓN', title='Total de Inscritos por Periodo'))
        st.plotly_chart(fig_applicants)

        fig_admitted = customize_chart(px.bar(filtered_data, x='Periodo', y='TOTAL ADMITIDOS', title='Total de Admitidos por Periodo'))
        st.plotly_chart(fig_admitted)

        fig_cutoff = customize_chart(px.bar(filtered_data, x='Periodo', y='PUNTAJE DE CORTE', title='Puntaje de Corte Promedio por Periodo'))
        st.plotly_chart(fig_cutoff)

    else:
        st.write("No hay datos disponibles para el programa y sede seleccionados.")
