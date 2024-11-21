import bcrypt
password = b"sua senha para encript"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print(hashed)

# python a.py    no cmd para encriptar sua senha, coloque no configs.py (Senha para logar no painel Admin)