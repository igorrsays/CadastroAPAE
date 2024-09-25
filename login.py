import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def show_login():
    login_success = False
    
# Função para verificar o login
def verificar_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuario == "admin" and senha == "123":
        iniciar_aplicacao_principal()
    else:
        messagebox.showerror("Erro", "Login falhou. Entre em contato com o setor responsável.")

# Função para iniciar a aplicação principal
def iniciar_aplicacao_principal():
    login_window.destroy()  # Fecha a janela de login
    subprocess.run(["python", "PythonApplication1.py"]) 

# janela de login
login_window = tk.Tk()
login_window.title("Tela de Login")

# ícone da janela
icon = tk.PhotoImage(file="usericon.png")
login_window.iconphoto(True, icon)

# tamanho da janela
largura_janela = 300
altura_janela = 150

# dimensões da tela
largura_tela = login_window.winfo_screenwidth()
altura_tela = login_window.winfo_screenheight()

# centralizar a janela
x = (largura_tela // 2) - (largura_janela // 2)
y = (altura_tela // 2) - (altura_janela // 2)

login_window.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

# Frame para centralizar os elementos
frame = tk.Frame(login_window)
frame.pack(expand=True)

# Criando os campos de entrada
tk.Label(frame, text="Usuário:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
entry_usuario = tk.Entry(frame)
entry_usuario.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Senha:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
entry_senha = tk.Entry(frame, show="*")
entry_senha.grid(row=1, column=1, padx=10, pady=5)

# Botão de Login
botao_login = tk.Button(frame, text="Login", command=verificar_login)
botao_login.grid(row=2, columnspan=2, pady=10)

# Vincula a tecla "Enter" para chamar a função de login
entry_senha.bind('<Return>', lambda event: verificar_login())

# Quando a janela for fechada, encerra o programa
login_window.protocol("WM_DELETE_WINDOW", sys.exit)

# Inicia a janela de login
login_window.mainloop()
