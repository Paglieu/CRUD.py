from flask import Flask, request, render_template, redirect, url_for, flash, get_flashed_messages
import re
import pyodbc
import pandas as pd

app = Flask(__name__)
app.secret_key = 'chave_secreta'

dados_conexao = (
    "Driver={SQL Server};"
    "Server=DESKTOP-9U9NE65;"
    "Database=WEBPythonSQL;"
)
conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()
print("Conexão com o Banco de Dados bem sucedida")

def criar_usuario(nome, email, senha):
    padrao_nome = r'^[A-Za-zÀ-ÿ]+$'
    nome_valido = re.match(padrao_nome, nome)

    padrao_email = r'^.+@.+$'
    email_valido = re.match(padrao_email, email)

    padrao_senha = r'^.+$'
    senha_valida = re.match(padrao_senha, senha)
    
    return bool(nome_valido) and bool(email_valido) and bool(senha_valida)

# def validar_usuario(email, senha):
    # email_valido = """SELECT * FROM Usuarios WHERE Email = ? """
    # validar_email = re.match(email_valido, email)

    # senha_valida = """SELECT * FROM Usuarios WHERE Senha = ?"""
    # validar_senha = re.match(senha_valida, senha)

    # return(validar_email, validar_senha)
    
@app.route('/cadastro', methods=['GET', 'POST'])
def index_cadastro():
    mensagem_create = None

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if criar_usuario(nome, email, senha):
            cursor.execute("SELECT * FROM Usuarios WHERE Email = ?", (email))
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                mensagem_create = 'Email já cadastrado'
            else:
                comando_criar = """INSERT INTO Usuarios(Nome, Email, Senha) VALUES (?, ?, ?)"""
                cursor.execute(comando_criar, (nome, email, senha))
                conexao.commit()
                return redirect(url_for('index_login'))
                
        else:
            mensagem_create = 'ERRO'

    return render_template('create.html', mensagem_create=mensagem_create)

@app.route('/', methods=['GET', 'POST'])
def index_login():
    mensagem_login = None

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cursor.execute("SELECT * FROM Usuarios WHERE Email = ? AND Senha = ?", (email, senha))
        validar_usuario = cursor.fetchone()

        if validar_usuario:
            mensagem_login = 'Login realizado com sucesso'
            return redirect(url_for('index_home'))
        else:
            mensagem_login = 'Email ou senha incorretos'

    return render_template('login.html', mensagem_login=mensagem_login)

@app.route('/home')
def index_home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)