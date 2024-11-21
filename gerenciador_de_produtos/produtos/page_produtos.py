import streamlit as st
from produtos import db

def display():
    if st.session_state.get('logged_in2', False):
        st.title('Gerenciador de produtos')

        id = st.number_input('ID do produto:', min_value=1, step=1, format='%d')
        name = st.text_input('Nome do produto:')
        price = st.number_input('Valor do produto:', min_value=0.01, format="%.2f")
        img = st.text_input('Link da imagem do produto:')

        col1, col2, col3 = st.columns([0.45, 0.44, 1.05])  # Ajuste os números para controlar os tamanhos e espaçamentos

        # Botão Adicionar
        with col1:
            if st.button('Adicionar Produto', key='add_button'):
                if len(name.strip()) >= 1:
                    if len(img.strip()) >= 1:
                        if price > 0:
                            st.session_state.pop('success_message', None)
                            st.session_state.pop('error_message', None)
                            message = db.add_product(id, name, price, img)
                            if message == "Produto adicionado com sucesso.":
                                st.session_state.success_message = message
                            else:
                                st.session_state.error_message = message
                        else:
                            st.session_state.error_message = "Adicione um preço para o produto."
                    else:
                        st.session_state.error_message = "Insira a URL da imagem do produto."
                else:
                    st.session_state.error_message = "Preencha o nome do produto."

        with col2:
            if st.button('Remover Produto', key='remove_button'):
                if id:  # Não precisa usar .strip() para um número
                    message = db.delete_product(id)
                    if message == f'Produto do ID: {id} removido com sucesso!':
                        st.session_state.success_message = message
                    elif message == f'Nenhum produto encontrado com o ID {id}.':
                        st.session_state.error_message = message
                    else:
                        st.session_state.error_message = message
                else:
                    st.session_state.error_message = "Preencha o ID do produto."

        # Botão Ver Produtos
        with col3:
            if st.button('Ver Produtos', key='view_button'):
                result = db.view_products()
                if result:
                    st.write("Lista de Produtos:")
                    # Converte o resultado para um formato mais adequado ao Streamlit
                    if isinstance(result, list):
                        st.dataframe(result)  # Se for uma lista de dicionários ou um DataFrame
                    else:
                        st.session_state.error_message = "Nenhum produto encontrado."
                else:
                    st.session_state.error_message = "Nenhum produto encontrado."

        # Mensagens
        if 'success_message' in st.session_state:
            st.success(st.session_state.success_message)
            st.session_state.pop('success_message', None)

        if 'error_message' in st.session_state:
            st.error(st.session_state.error_message)
            st.session_state.pop('error_message', None)
    else:
        st.error("Você precisa estar logado para acessar esta página.")
        st.stop()  # Interrompe a execução do código da página