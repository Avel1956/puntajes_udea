import streamlit as st
from puntajes_udea import show_puntajes_udea_page
from saber_pro_udea import show_saberpro_udea_page
from accesibilidad import pagina_acceso

st.set_page_config(
    page_title="UdeA Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    menu_items={
        'Get Help': 'http://tinyurl.com/puntudea',
        'Report a bug': None,
        'About': "# Tablero de visualizacion de datos de la UdeA"
    }
)

# Define the color palette
primary_color = "#34A853"  
secondary_color = "#FFFFFF"  
background_color = "#F5F5F5"  
text_color = "#262730"  


website_url = "https://www.nataliarectora.com/"


image_path = "https://github.com/Avel1956/puntajes_udea/blob/main/images/nrect.png"


link = f'<a href="{website_url}" target="_blank"><img src="{image_path}" alt="Natalia rectoría" style="width:100%;"></a>'



def main():
    st.sidebar.markdown(link, unsafe_allow_html=True)
    st.sidebar.title("Navegación")
    page = st.sidebar.selectbox("Seleccione página", ["Puntajes UDEA", "Saber Pro UdeA", "Accesibilidad UdeA"])

    if page == "Puntajes UDEA":
        show_puntajes_udea_page()
    elif page == "Saber Pro UdeA":
        show_saberpro_udea_page()
    elif page == "Accesibilidad UdeA":
        pagina_acceso()
        # Call other page functions
        pass

if __name__ == "__main__":
    main()