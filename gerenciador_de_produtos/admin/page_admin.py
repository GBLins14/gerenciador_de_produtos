import streamlit as st
from db import database
from configs import plans

def display():
    if st.session_state.get('logged_in', False):
        st.title('Admin')

        plan = st.selectbox('Escolha um Plano', plans)
        user = st.text_input('Usuario:')
        password = st.text_input('Senha', type='password', key='admin_password_' + str(st.session_state.get('logged_in', False)))  # Chave única baseada no estado de login
      

        col1, col2, col3 = st.columns([0.23, 0.35, 1])  # Ajuste os números para controlar os tamanhos e espaçamentos

        # Botão Adicionar
        with col1:
            if st.button('Adicionar', key='add_button'):
                if len(user.strip()) >= 1:
                    if len(password.strip()) >= 1:
                        st.session_state.pop('success_message', None)
                        st.session_state.pop('error_message', None)
                        message = database.add_sql(user, plan, password)
                        if message == "Usuário Cadastrado.":
                            st.session_state.success_message = message
                        else:
                            st.session_state.error_message = message
                    else:
                        st.session_state.error_message = "Insira uma senha de autenticação."
                else:
                    st.session_state.error_message = "Preencha o campo de usuário."

        with col2:
            if st.button('Remover Usuário', key='remove_button'):
                if len(user.strip()) >= 1:
                    message = database.remove_sql(user)
                    if message == 'Usuário removido com sucesso.':
                        st.session_state.success_message = message
                    elif message == 'Usuário não encontrado.':
                        st.session_state.error_message = message
                    else:
                        st.session_state.error_message = message
                else:
                    st.session_state.error_message = "Preencha o campo de usuário."

        # Botão Ver Usuários
        with col3:
            if st.button('Ver Usuários', key='view_button'):
                result = database.list_sql()
                if result:
                    st.write("Lista de Usuários:")
                    st.dataframe(result)
                else:
                    st.session_state.error_message = "Nenhum usuário encontrado."

        # Mensagens
        if 'success_message' in st.session_state:
            st.success(st.session_state.success_message)
            st.session_state.pop('success_message', None)

        if 'error_message' in st.session_state:
            st.error(st.session_state.error_message)
            st.session_state.pop('error_message', None)
    else:
        st.error("Você precisa estar logado para acessar esta página.")
        st.stop()  # Interrompe a execução do código da página admin
