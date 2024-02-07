import streamlit as st
import pandas as pd
import plotly.express as px
from plotly import graph_objs as go

# Definir la paleta de colores
primary_color = "#34A853"
secondary_color = "#FFFFFF"
background_color = "#F5F5F5"
text_color = "#262730"

# Estilos personalizados para los gráficos de Plotly
def customize_chart(fig):
    fig.update_layout(
        paper_bgcolor=background_color,
        plot_bgcolor=background_color,
        font_color=text_color
    )
    return fig

def show_horas_docente_page():
    st.title("Horas de docencia")

    # Cargar y preprocesar los datos
    def cargar_preprocesar_datos():
        catedra_df = pd.read_excel("output/Horas_catedra.xlsx")
        regulares_ocasionales_df = pd.read_excel("output/Horas_regulares_ocasionales.xlsx")

        # Preprocesar datos de cátedra
        # Asumiendo que 1 es para el primer semestre y 2 para el segundo
        catedra_df['Fecha'] = pd.to_datetime(catedra_df['año'].astype(str) + catedra_df['periodo'].map({1: '-01-01', 2: '-07-01'}))
        catedra_df = catedra_df[['Fecha', 'Nombre fac', 'Nro contratos', 'Total horas']]

        # Preprocesar datos de regulares y ocasionales
        # Asumiendo que el dígito de las decenas del semestre es el año y el de las unidades es el número del semestre
        regulares_ocasionales_df['Fecha'] = pd.to_datetime(regulares_ocasionales_df['Semestre'].floordiv(10).astype(str) + regulares_ocasionales_df['Semestre'].mod(10).map({1: '-01-01', 2: '-07-01'}))
        regulares_ocasionales_df = regulares_ocasionales_df[['Fecha', 'Nombre fac', 'Nro planes', 'Total horas']]

        return catedra_df, regulares_ocasionales_df


    catedra_df, regulares_ocasionales_df = cargar_preprocesar_datos()

    # Seleccionar facultad para filtrar
    nombres_facultades = ['Todas'] + sorted(set(catedra_df['Nombre fac'].unique().tolist() + regulares_ocasionales_df['Nombre fac'].unique().tolist()))
    facultad_seleccionada = st.selectbox('Selecciona una facultad', nombres_facultades)

    # Filtrar datos basados en la selección
    if facultad_seleccionada != 'Todas':
        catedra_filtrado = catedra_df[catedra_df['Nombre fac'] == facultad_seleccionada]
        regulares_ocasionales_filtrado = regulares_ocasionales_df[regulares_ocasionales_df['Nombre fac'] == facultad_seleccionada]
    else:
        catedra_filtrado = catedra_df
        regulares_ocasionales_filtrado = regulares_ocasionales_df

    # Graficar la evolución del número de contratos y planes, y las horas totales
    def graficar_evolucion(df, columna, titulo):
        fig = px.line(df, x='Fecha', y=columna, title=f"{titulo} - {columna}", labels={"Fecha": "Fecha", columna: columna}, markers=True)
        fig = customize_chart(fig)
        st.plotly_chart(fig)

    # Calcular y mostrar estadísticas
    def mostrar_estadisticas(df, columna):
        if not df.empty:
            df['Tasa de cambio'] = df[columna].pct_change()
            tasa_cambio_promedio = df['Tasa de cambio'].mean() * 100
            st.write(f"Tasa media de cambio para {columna}: {tasa_cambio_promedio:.2f}%")

    # Evolución para cátedra
    graficar_evolucion(catedra_filtrado, 'Nro contratos', f"Evolución del número de contratos (Cátedra) - {facultad_seleccionada}")
    graficar_evolucion(catedra_filtrado, 'Total horas', f"Evolución de las horas totales (Cátedra) - {facultad_seleccionada}")
    mostrar_estadisticas(catedra_filtrado, 'Nro contratos')
    mostrar_estadisticas(catedra_filtrado, 'Total horas')

    # Evolución para regulares y ocasionales
    graficar_evolucion(regulares_ocasionales_filtrado, 'Nro planes', f"Evolución del número de planes (Regulares y Ocasionales) - {facultad_seleccionada}")
    graficar_evolucion(regulares_ocasionales_filtrado, 'Total horas', f"Evolución de las horas totales (Regulares y Ocasionales) - {facultad_seleccionada}")
    mostrar_estadisticas(regulares_ocasionales_filtrado, 'Nro planes')
    mostrar_estadisticas(regulares_ocasionales_filtrado, 'Total horas')


