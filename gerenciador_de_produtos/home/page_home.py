import streamlit as st
from produtos.db import view_products  # Importando a função de visualização dos produtos

def display():
    # Título da página
    st.title('Loja de Produtos')

    # Chama a função para exibir os produtos
    products = view_products()

    # Exibe os produtos se existirem
    if isinstance(products, list) and len(products) > 0:
        for product in products:
            st.image(product["image"], width=100)
            st.markdown(f"<h3 style='font-size: 30px;'>{product['name']}</h3>", unsafe_allow_html=True)
            st.write(f"R$ {product['price']}")
    else:
        st.write("Nenhum produto disponível.")
