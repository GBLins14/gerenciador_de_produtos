import streamlit as st
import bcrypt
from admin import page_admin
import configs

# Senha criptografada para comparação
hashed_password = configs.password

def display():
    # Verificar se o usuário está logado
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.title('Login')

        username = st.text_input('Username', key='username')
        password = st.text_input('Password', type='password', key='login_password')  # Para a tela de login


        if st.button('Login'):
            if username == configs.username and bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                st.session_state.logged_in = True
                st.success('Login bem-sucedido!')
                # Limpa os campos de login
                st.session_state.pop('username', None)
                st.session_state.pop('password', None)
                page_admin.display()  # Chama a página de admin depois de logar
            else:
                st.error('Credenciais inválidas.')
    else:
        # Se já estiver logado, exibe a página de administração
        page_admin.display()
