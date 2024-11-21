import streamlit as st
from login import login_admin
from login import login_produtos  # Outra página qualquer, se você tiver
from home import page_home

def main():
    # Obtém os parâmetros da URL
    page = st.sidebar.selectbox("Escolha a página", ["Inicio", "Admin", "Gerenciador de produtos"])

    if page == 'Inicio':
        page_home.display()
    elif page == 'Admin':
        login_admin.display()  # Chama a função de exibição da página Admin
    elif page == 'Gerenciador de produtos':
        login_produtos.display()
    else:
        st.error("Página não encontrada!")  # Se o parâmetro for inválido

if __name__ == "__main__":
    main()