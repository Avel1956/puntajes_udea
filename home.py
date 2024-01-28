import streamlit as st
import base64
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

def imagen_sidebar():
    with open("images/nrect.png", "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

        st.sidebar.markdown(
            f"""
            <div style="display:flex;justify-content:center;">
                <img src="data:image/png;base64,{data}" style="width:100%;">
            </div>
            """,
            unsafe_allow_html=True,
        )



def main():
    imagen_sidebar()
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