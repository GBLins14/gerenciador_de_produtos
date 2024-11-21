import streamlit as st
import bcrypt
import db.database  # Ajuste da importação
from produtos import page_produtos  # Página de administração após login

# Função para verificar as credenciais do usuário
def check_credentials(username, password):
    connection = db.database.connect_db()  # Usando a função de conexão do banco de dados
    sql = connection.cursor()
    
    # Verificar se o usuário existe na tabela
    sql.execute("SELECT password, plan FROM users WHERE username = ?", (username,))
    user = sql.fetchone()
    
    connection.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')) and user[1] == 'Admin':
        return True
    return False

def display():
    # Verificar se o usuário está logado
    if 'logged_in2' not in st.session_state or not st.session_state.logged_in2:
        st.title('Login')

        username = st.text_input('Username', key='username')
        password = st.text_input('Password', type='password', key='password')

        if st.button('Login'):
            # Verifica no banco de dados se as credenciais são válidas
            if check_credentials(username, password):
                st.session_state.logged_in2 = True
                st.success('Login bem-sucedido!')
                # Limpa os campos de login
                st.session_state.pop('username', None)
                st.session_state.pop('password', None)
                page_produtos.display()  # Chama a página de administração depois de logar
            else:
                st.error('Credenciais inválidas.')
    else:
        # Se já estiver logado, exibe a página de administração
        page_produtos.display()
