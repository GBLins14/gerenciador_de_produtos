import sqlite3
import bcrypt

def connect_db():
    connection = sqlite3.connect('db/database.db')
    return connection

def add_sql(username, plan, password):
    connection = connect_db()
    sql = connection.cursor()

    # Criação da tabela se não existir
    sql.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        plan TEXT,
        password TEXT
    )
    """)

    # Verificação se o usuário já existe
    sql.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    existing_user = sql.fetchone()

    if existing_user:
        connection.close()  # Fecha a conexão se o usuário já existir
        return "Usuário já existe."

    # Criptografando a senha antes de inserir
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Inserção do novo usuário
    try:
        sql.execute("""
        INSERT INTO users (username, plan, password)
        VALUES (?, ?, ?)
        """, (username, plan, hashed_password))
        
        connection.commit()  # Commit após inserção
        return "Usuário Cadastrado."
    except sqlite3.Error as e:
        connection.rollback()  # Em caso de erro, faz o rollback da transação
        return f"Erro ao cadastrar o usuário: {e}"
    finally:
        connection.close()  # Fecha a conexão independentemente do resultado

def list_sql():
    connection = connect_db()
    sql = connection.cursor()
    sql.execute('SELECT * FROM users')
    result = sql.fetchall()
    connection.close()
    return result

def remove_sql(username):
    connection = connect_db()
    sql = connection.cursor()

    # Verifica se o usuário existe
    sql.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    existing_user = sql.fetchone()

    if not existing_user:
        connection.close()  # Fecha a conexão se o usuário não existir
        return "Usuário não encontrado."

    # Remove o usuário
    try:
        sql.execute("DELETE FROM users WHERE username = ?", (username,))
        connection.commit()  # Commit após a remoção
        return "Usuário removido com sucesso."
    except sqlite3.Error as e:
        connection.rollback()  # Em caso de erro, faz o rollback da transação
        return f"Erro ao remover o usuário: {e}"
    finally:
        connection.close()  # Fecha a conexão independentemente do resultado
