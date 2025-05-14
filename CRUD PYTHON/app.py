from flask import Flask, request, render_template
import re
import pyodbc
import pandas as pd

app = Flask(__name__)

dados_conexao = (
    "Driver={SQL Server};"
    "Server=DESKTOP-9U9NE65;"
    "Database=PythonSQL;"
)
conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()
print("Conexão com o Banco de Dados bem sucedida")

def validar_usuario(email, senha):
    padrao_email = r'^\d+$'
    senha_valida = senha == '123'
    email_valido = re.match(padrao_email, email)

    return email_valido and senha_valida

@app.route('/', methods=['GET', 'POST'])
def index_cpf():
    mensagem_login = None

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        comando_adicionar = f"""INSERT INTO Documento(CPF) VALUES (?)"""
        cursor.execute(comando_adicionar, (email,))
        conexao.commit()

        if validar_usuario(email, senha):
            mensagem_login = f'Login realizado com sucesso!'
        else:
            mensagem_login = 'Email ou senha inválidos'

    return render_template('cpf.html', mensagem_login=mensagem_login)

if __name__ == '__main__':
    app.run(debug=True)