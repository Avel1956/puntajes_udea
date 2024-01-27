import streamlit as st
from puntajes_udea import show_puntajes_udea_page
from saber_pro_udea import show_saberpro_udea_page

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

def main():
    st.sidebar.title("Navegación")
    page = st.sidebar.selectbox("Seleccione página", ["Puntajes UDEA", "Saber Pro UdeA"])

    if page == "Puntajes UDEA":
        show_puntajes_udea_page()
    elif page == "Saber Pro UdeA":
        show_saberpro_udea_page()
        # Call other page functions
        pass

if __name__ == "__main__":
    main()