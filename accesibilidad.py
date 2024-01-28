import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def cargar_datos():
    # Carga aquí tus datos
    data = pd.read_excel('output/access.xlsx')
    return data

def personalizar_grafico(fig):
    # Personalizaciones adicionales aquí
    return fig

def calcular_estadisticas(data):
    # Calculando estadísticas clave
    estadisticas = []
    for columna in data.columns[1:-1]:  # Excluyendo 'SEMESTRE' y 'TOTAL'
        total_inicial = data[columna].iloc[0]
        total_final = data[columna].iloc[-1]
        cambio = ((total_final - total_inicial) / total_inicial) * 100

        estadisticas.append({
            'Discapacidad': columna,
            'Total Inicial': total_inicial,
            'Total Final': total_final,
            'Cambio (%)': round(cambio, 2)
        })

    total_estudiantes_inicial = data['TOTAL de Estudiantes matriculados con discapacidad'].iloc[0]
    total_estudiantes_final = data['TOTAL de Estudiantes matriculados con discapacidad'].iloc[-1]
    cambio_total = ((total_estudiantes_final - total_estudiantes_inicial) / total_estudiantes_inicial) * 100

    estadisticas.append({
        'Discapacidad': 'Total Estudiantes con Discapacidad',
        'Total Inicial': total_estudiantes_inicial,
        'Total Final': total_estudiantes_final,
        'Cambio (%)': round(cambio_total, 2)
    })

    return pd.DataFrame(estadisticas)

def analisis_datos(data):
    st.write("""
    ## Análisis de los Datos de Discapacidad Estudiantil

    En la Universidad de Antioquia, estamos comprometidos con la inclusión y el apoyo a todos nuestros estudiantes. El análisis de los datos de matriculación de estudiantes con discapacidades a lo largo de los años nos ofrece una visión valiosa sobre nuestro progreso y las áreas en las que aún podemos mejorar.

    A continuación, se presenta un resumen de los cambios en la matrícula de estudiantes con diferentes tipos de discapacidad a lo largo de los años:
    """)

    estadisticas = calcular_estadisticas(data)
    st.table(estadisticas)

    st.write("""
    ### Nuestro Compromiso Continuo
    A pesar de estos avances, reconocemos que aún hay trabajo por hacer. Nos enfocamos en mejorar nuestras políticas y programas para asegurar que cada estudiante, sin importar sus desafíos individuales, tenga acceso a una educación de calidad y un entorno de aprendizaje enriquecedor.

    ### Llamado a la Acción
    Te invitamos a unirte a nosotros en este esfuerzo. Tu apoyo y participación son cruciales para construir una comunidad académica más inclusiva.
    """)

def pagina_acceso():
    data = cargar_datos()
    st.title("Tablero de Datos de Discapacidad Estudiantil")

    analisis_datos(data)

def crear_grafico_baja_vision(data):
    # Gráfico de alta contraste para 'Baja Visión'
    fig = px.bar(data, x='SEMESTRE', y='BAJA VISIÓN', color='BAJA VISIÓN', color_continuous_scale=px.colors.sequential.Viridis)
    return personalizar_grafico(fig)

def crear_grafico_miembros_superiores(data):
    # Gráfico de barras horizontales para 'Compromiso Miembros Superiores'
    fig = px.bar(data, x='COMPROMISO MIEMBROS SUPERIORES', y='SEMESTRE', orientation='h')
    return personalizar_grafico(fig)

def crear_grafico_miembros_inferiores(data):
    # Gráfico escalonado para 'Compromiso Miembros Inferiores'
    fig = go.Figure(go.Bar(x=data['SEMESTRE'], y=data['COMPROMISO MIEMBROS INFERIORES'], marker=dict(color=data['COMPROMISO MIEMBROS INFERIORES'], coloraxis="coloraxis")))
    fig.update_traces(marker_line_width=2, marker_line_color="rgb(8,48,107)")
    return personalizar_grafico(fig)

def crear_grafico_sordo(data):
    # Gráfico circular para 'Sordo'
    fig = px.pie(data, values='SORDO', names='SEMESTRE')
    return personalizar_grafico(fig)

def crear_grafico_sordo_oralizado(data):
    # Gráfico radial para 'Sordo Oralizado'
    fig = px.line_polar(data, r='SORDO ORALIZADO', theta='SEMESTRE', line_close=True)
    return personalizar_grafico(fig)

def crear_grafico_sordoceguera(data):
    # Gráfico con marcadores destacados para 'Sordoceguera'
    fig = px.scatter(data, x='SEMESTRE', y='SORDOCEGUERA', size='SORDOCEGUERA', size_max=15)
    return personalizar_grafico(fig)

def crear_grafico_talla_baja(data):
    # Gráfico de líneas con marcadores para 'Talla Baja'
    fig = px.line(data, x='SEMESTRE', y='TALLA BAJA', markers=True)
    return personalizar_grafico(fig)

def crear_grafico_hipoacusia(data):
    # Gráfico de área para 'Con Hipoacusia'
    fig = px.area(data, x='SEMESTRE', y='CON HIPOACUSIA')
    return personalizar_grafico(fig)

def crear_grafico_usuario_silla_ruedas(data):
    # Gráfico de barras con curvas suaves para 'Usuario de Silla de Ruedas'
    fig = go.Figure(go.Bar(x=data['SEMESTRE'], y=data['USUARIO DE SILLA DE RUEDAS']))
    fig.update_traces(marker_line_width=2, marker_line_color="navy")
    return personalizar_grafico(fig)

def crear_grafico_ciego(data):
    # Gráfico con patrón de textura para 'Ciego'
    fig = go.Figure(data=[go.Bar(x=data['SEMESTRE'], y=data['CIEGO'])])
    fig.update_traces(marker_pattern_shape="x", marker_pattern_fillmode="replace")
    return personalizar_grafico(fig)

def pagina_acceso():
    data = cargar_datos()
    st.title("Tablero de Datos de Discapacidad Estudiantil")
    analisis_datos(data)
    # Llamadas a las funciones para mostrar los gráficos
    st.subheader("Baja Visión")
    st.plotly_chart(crear_grafico_baja_vision(data), use_container_width=True)

    st.subheader("Compromiso de Miembros Superiores")
    st.plotly_chart(crear_grafico_miembros_superiores(data), use_container_width=True)

    st.subheader("Compromiso de Miembros Inferiores")
    st.plotly_chart(crear_grafico_miembros_inferiores(data), use_container_width=True)

    st.subheader("Sordo")
    st.plotly_chart(crear_grafico_sordo(data), use_container_width=True)

    st.subheader("Sordo Oralizado")
    st.plotly_chart(crear_grafico_sordo_oralizado(data), use_container_width=True)

    st.subheader("Sordoceguera")
    st.plotly_chart(crear_grafico_sordoceguera(data), use_container_width=True)

    st.subheader("Talla Baja")
    st.plotly_chart(crear_grafico_talla_baja(data), use_container_width=True)

    st.subheader("Con Hipoacusia")
    st.plotly_chart(crear_grafico_hipoacusia(data), use_container_width=True)

    st.subheader("Usuario de Silla de Ruedas")
    st.plotly_chart(crear_grafico_usuario_silla_ruedas(data), use_container_width=True)

    st.subheader("Ciego")
    st.plotly_chart(crear_grafico_ciego(data), use_container_width=True)



