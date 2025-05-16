from flask import Flask, request, render_template, redirect, url_for
import re
import pyodbc
import pandas as pd

app = Flask(__name__)

dados_conexao = (
    "Driver={SQL Server};"
    "Server=DESKTOP-9U9NE65;"
    "Database=WEBPythonSQL;"
)
conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()
print("Conexão com o Banco de Dados bem sucedida")

def criar_usuario(nome, email, senha):
    padrao_nome = r'^[A-Za-zÀ-ÿ ]+$'
    nome_valido = re.match(padrao_nome, nome)

    padrao_email = r'^.+@.+$'
    email_valido = re.match(padrao_email, email)

    padrao_senha = r'^.+$'
    senha_valida = re.match(padrao_senha, senha)
    
    return bool(nome_valido) and bool(email_valido) and bool(senha_valida)

##def validar_usuario(email, senha):
   ##mudarpadrao_email = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    ##email_validar = re.match(padrao_email, email)

    ##mudarcomando_senha = mudarsenha = f"""SELECT Senha FROM Usuarios WHERE Email = {padrao_email}"""
    ##mudarcursor.execute(comando_senha, (email,))
    
@app.route('/cadastro', methods=['GET', 'POST'])
def index_cadastro():
    mensagem_create = None

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        if criar_usuario(nome, email, senha):
            comando_criar = """INSERT INTO Usuarios(Nome, Email, Senha) VALUES (?, ?, ?)"""
            cursor.execute(comando_criar, (nome, email, senha))
            conexao.commit()
            mensagem_create = 'Usuário criado com sucesso'
        else:
            mensagem_create = 'ERRO'

    return render_template('create.html', mensagem_create=mensagem_create)

@app.route('/', methods=['GET', 'POST'])
def index_login():
    mensagem_login = None

    #if request.method == 'GET':
        #email = request.form['email']
        #senha = request.form['senha']

        #if validar_usuario(email, senha):
        #    mensagem_login = 'Login realizado com sucesso!'
        #else:
        #   mensagem_login = 'Email ou senha inválidos'

    return render_template('login.html', mensagem_login=mensagem_login)

if __name__ == '__main__':
    app.run(debug=True)