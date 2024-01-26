import streamlit as st
from puntajes_udea import show_puntajes_udea_page
from saber_pro_udea import show_saberpro_udea_page

# Other imports and page definitions

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