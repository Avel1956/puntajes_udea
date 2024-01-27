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

# The URL of the website you want to link to
website_url = "https://www.nataliarectora.com/"

# The path to your image (this can also be a URL)
image_path = "images/nrect.png"

# Use HTML to create the hyperlink with an image
link = f'<a href="{website_url}" target="_blank"><img src="{image_path}" alt="Natalia rectoría" style="width:100%;"></a>'

# Place the link with the image in the sidebar

def main():
    st.sidebar.markdown(link, unsafe_allow_html=True)
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