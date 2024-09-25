import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import re
import sqlite3
import tkinter.messagebox as messagebox
import os
import tkinter as tk
from PIL import Image, ImageTk


def create_database():
    conn = sqlite3.connect('cadastro.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cadastros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        data_nascimento TEXT,
        cpf TEXT,
        telefone TEXT,
        bairro TEXT,
        cidade TEXT,
        estado TEXT,
        sexo TEXT,
        escolaridade TEXT,
        bpc BOOLEAN,
        loas BOOLEAN,
        cid TEXT
    )
    ''')
 
    conn.commit()
    conn.close()
    
def cadastrar_alterar():
    nome = entries[0].get()
    data_nascimento = entries[1].get()
    cpf = entries[2].get()
    telefone = entries[3].get()
    bairro = entries[4].get()
    cidade = entries[5].get()
    estado = estado_var.get()
    sexo = sexo_var.get()
    escolaridade = escolaridade_var.get()
    beneficio_bpc = bpc_var.get()
    beneficio_loas = bolsa_var.get()
    cid = cid_var.get()

    if not cpf or len(cpf) < 11:
        messagebox.showwarning("Atenção", "Preencha os campos obrigatórios: CPF")
        return

    # Conectando ao banco de dados para verificar se o CPF já existe
    conn = sqlite3.connect('cadastro.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT cpf FROM cadastros WHERE cpf = ?
    ''', (cpf,))
    resultado = cursor.fetchone()

    if resultado:
        messagebox.showerror("Erro", "Não foi possível concluir a operação. CPF já cadastrado.")
        conn.close()
        return

    # Caso o CPF não esteja cadastrado, realiza o cadastro
    cursor.execute('''
    INSERT INTO cadastros (nome, data_nascimento, cpf, telefone, bairro, cidade, estado, sexo, escolaridade, bpc, loas, cid)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, data_nascimento, cpf, telefone, bairro, cidade, estado, sexo, escolaridade, beneficio_bpc, beneficio_loas, cid))

    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
    limpar()  # Limpa os campos após o cadastro
    atualizar_tabela()  # Atualiza a tabela após o cadastro

def alterar_dados():
    cpf = entries[2].get()
    
    if not cpf or len(cpf) < 11:
        messagebox.showwarning("Atenção", "Preencha os campos obrigatórios: CPF")
        return

    # Verificando se o CPF existe no banco de dados
    conn = sqlite3.connect('cadastro.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM cadastros WHERE cpf = ?''', (cpf,))
    resultado = cursor.fetchone()

    if not resultado:
        messagebox.showwarning("Aviso", "Nenhum cadastro encontrado com esse nome ou CPF.")
        conn.close()
        return

    # Pergunta de segurança
    resposta = messagebox.askquestion("Confirmação", "Os dados desse cadastro serão alterados. Confirma operação?")
    
    if resposta == 'yes':
        # Se confirmado, altera os dados
        nome = entries[0].get()
        data_nascimento = entries[1].get()
        telefone = entries[3].get()
        bairro = entries[4].get()
        cidade = entries[5].get()
        estado = estado_var.get()
        sexo = sexo_var.get()
        escolaridade = escolaridade_var.get()
        beneficio_bpc = bpc_var.get()
        beneficio_loas = bolsa_var.get()
        cid = cid_var.get()

        cursor.execute('''UPDATE cadastros SET nome = ?, data_nascimento = ?, telefone = ?, bairro = ?, cidade = ?, estado = ?, sexo = ?, escolaridade = ?, bpc = ?, loas = ?, cid = ? WHERE cpf = ?''',
                       (nome, data_nascimento, telefone, bairro, cidade, estado, sexo, escolaridade, beneficio_bpc, beneficio_loas, cid, cpf))

        conn.commit()
        messagebox.showinfo("Sucesso", "Dados alterados com sucesso!")
        atualizar_tabela()  # Atualiza a tabela após a alteração
    conn.close()

def excluir():
    cpf = entries[2].get()  # Obter o CPF do campo correspondente
    if cpf:
        conn = sqlite3.connect('cadastro.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        DELETE FROM cadastros WHERE cpf = ?
        ''', (cpf,))
        
        if cursor.rowcount > 0:
            conn.commit()
            messagebox.showinfo("Sucesso", "Cadastro excluído com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhum cadastro encontrado com esse nome ou CPF.")

        conn.close()
        limpar()  # Limpa os campos após a exclusão
        atualizar_tabela()  # Atualiza a tabela após a exclusão
    else:
        messagebox.showwarning("Aviso", "Por favor, insira um CPF para excluir")
        
def consultar():
    consulta_window = tk.Toplevel(app)
    consulta_window.title("Consulta")
    consulta_window.geometry("300x300")

    # Centralizando a janela
    x = app.winfo_x() + (app.winfo_width() // 2) - (300 // 2)
    y = app.winfo_y() + (app.winfo_height() // 2) - (300 // 2)
    consulta_window.geometry(f"300x300+{x}+{y}")

    lbl = tk.Label(consulta_window, text="Digite o nome ou CPF:")
    lbl.pack(pady=10)

    entrada_consulta = tk.Entry(consulta_window)
    entrada_consulta.pack(pady=5)
    entrada_consulta.focus_set()  # Seleciona automaticamente o campo de entrada

    listbox = tk.Listbox(consulta_window)
    listbox.pack(fill=tk.BOTH, expand=True, pady=10)

    def realizar_consulta(event=None): 
        valor = entrada_consulta.get()
        conn = sqlite3.connect('cadastro.db')
        cursor = conn.cursor()

        if re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', valor):  # Verifica se é um CPF no formato correto
            cursor.execute("SELECT * FROM cadastros WHERE cpf = ?", (valor,))
            resultado = cursor.fetchone()
            if resultado:
                messagebox.showinfo("Resultado", f"Dados encontrados:\nNome: {resultado[1]}\nData de Nascimento: {resultado[2]}\nCPF: {resultado[3]}\nTelefone: {resultado[4]}\nBairro: {resultado[5]}\nCidade: {resultado[6]}\nEstado: {resultado[7]}\nSexo: {resultado[8]}\nEscolaridade: {resultado[9]}\nBenefício Social: {resultado[10]}\nCID: {resultado[11]}")
            else:
                messagebox.showwarning("Aviso", "Nenhum cadastro encontrado com esse nome ou CPF.")
        else:  # Consulta por nome
            cursor.execute("SELECT nome FROM cadastros WHERE nome LIKE ?", (f"{valor}%",))
            resultados = cursor.fetchall()
            listbox.delete(0, tk.END)  # Limpa a lista
            if resultados:
                for r in resultados:
                    listbox.insert(tk.END, r[0])  # Adiciona os nomes à lista
            else:
                messagebox.showwarning("Aviso", "Nenhum cadastro encontrado com esse nome ou CPF.")

        conn.close()

    btn_consultar = tk.Button(consulta_window, text="Consultar", command=realizar_consulta)
    btn_consultar.pack(pady=10)

    entrada_consulta.bind("<Return>", realizar_consulta)  # Permite o uso do Enter para enviar


    def selecionar_nome(event):
        selecionado = listbox.curselection()
        if selecionado:
            nome_selecionado = listbox.get(selecionado)
            conn = sqlite3.connect('cadastro.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cadastros WHERE nome = ?", (nome_selecionado,))
            resultado = cursor.fetchone()
            if resultado:
                messagebox.showinfo("Resultado", f"Dados encontrados:\nNome: {resultado[1]}\nData de Nascimento: {resultado[2]}\nCPF: {resultado[3]}\nTelefone: {resultado[4]}\nBairro: {resultado[5]}\nCidade: {resultado[6]}\nEstado: {resultado[7]}\nSexo: {resultado[8]}\nEscolaridade: {resultado[9]}\nBenefício Social: {resultado[10]}\nCID: {resultado[11]}")
            conn.close()

    listbox.bind('<Double-1>', selecionar_nome)  


def limpar():
    for entry in entries:
        entry.delete(0, tk.END)
    for icon in icons:
        icon.config(text="")  # Limpa os ícones

def atualizar_tabela():
    # Limpa a tabela existente
    for row in tree.get_children():
        tree.delete(row)
    
    # Conecta ao banco de dados e busca os dados
    conn = sqlite3.connect('cadastro.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome, data_nascimento, cpf, telefone, bairro, cidade, estado, sexo, escolaridade, bpc, loas, cid FROM cadastros")
    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert('', tk.END, values=row)

    conn.close()

def format_date(event):
    value = re.sub(r'\D', '', event.widget.get())
    if len(value) > 8:
        value = value[:8]

    if len(value) >= 8:
        formatted = f"{value[:2]}/{value[2:4]}/{value[4:]}"
        icons[1].config(text="")  # Limpa o ícone se a data estiver completa
    else:
        formatted = value
        icons[1].config(text="X", fg="red")  # Exibe ícone vermelho se incompleto

    event.widget.delete(0, tk.END)
    event.widget.insert(0, formatted)

def format_cpf(event):
    value = re.sub(r'\D', '', event.widget.get())
    if len(value) > 11:
        value = value[:11]

    if len(value) >= 11:
        formatted = f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"
        icons[2].config(text="")  # Limpa o ícone se o CPF estiver completo
    else:
        formatted = value
        icons[2].config(text="X", fg="red")  # Exibe ícone vermelho se incompleto

    event.widget.delete(0, tk.END)
    event.widget.insert(0, formatted)

def format_phone(event):
    value = re.sub(r'\D', '', event.widget.get())
    if len(value) > 11:
        value = value[:11]

    if len(value) == 11:
        formatted = f"({value[:2]}){value[2:7]}-{value[7:]}"
        icons[3].config(text="")  # Limpa o ícone se o telefone estiver completo
    else:
        formatted = value
        icons[3].config(text="X", fg="red")  # Exibe ícone vermelho se incompleto

    event.widget.delete(0, tk.END)
    event.widget.insert(0, formatted)

def on_item_double_click(event):
    selected_item = tree.selection()[0]
    item_values = tree.item(selected_item, 'values')

    # Preenche os campos com os valores do item selecionado
    entries[0].delete(0, tk.END)
    entries[0].insert(0, item_values[0])
    entries[1].delete(0, tk.END)
    entries[1].insert(0, item_values[1])
    entries[2].delete(0, tk.END)
    entries[2].insert(0, item_values[2])
    entries[3].delete(0, tk.END)
    entries[3].insert(0, item_values[3])
    entries[4].delete(0, tk.END)
    entries[4].insert(0, item_values[4])
    entries[5].delete(0, tk.END)
    entries[5].insert(0, item_values[5])
    estado_var.set(item_values[6])  # Estado
    sexo_var.set(item_values[7])  # Sexo
    escolaridade_var.set(item_values[8])  # Escolaridade
    bpc_var.set(item_values[9])  # BPC
    bolsa_var.set(item_values[10])  # LOAS
    cid_var.set(item_values[11])  # CID
    # Aqui você deve preencher os outros campos (bairro, cidade, etc.) com base no CPF ou nome

app = tk.Tk()
app.title("Formulário de Cadastro - APAE TERESINA")

# Adicionando o ícone da janela
icon = tk.PhotoImage(file="usericon.png")
app.iconphoto(True, icon)

# ccentralização da janela
window_width = 800  
window_height = 650  

# largura e a altura da tela
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calculando a posição X e Y
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)


app.geometry(f"{window_width}x{window_height}+{x}+{y}")


# Labels e Entradas
labels = ["Nome", "Data de Nascimento", "CPF", "Telefone Celular", "Bairro", "Cidade"]
entries = []
icons = []

for label in labels:
    frame = tk.Frame(app)
    frame.pack(fill=tk.X, padx=5, pady=5)
    
    lbl = tk.Label(frame, text=label, width=20)
    lbl.pack(side=tk.LEFT)
    
    entry = tk.Entry(frame)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    entries.append(entry)

    icon = tk.Label(frame, text="", fg="red", width=2)
    icon.pack(side=tk.LEFT)
    icons.append(icon)


# Opções de Estado
frame_estado = tk.Frame(app)
frame_estado.pack(fill=tk.X, padx=5, pady=5)
lbl_estado = tk.Label(frame_estado, text="Estado", width=20)
lbl_estado.pack(side=tk.LEFT)
estado_var = tk.StringVar()
estado_options = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
estado_menu = ttk.Combobox(frame_estado, textvariable=estado_var, values=estado_options, state='readonly')
estado_menu.pack(fill=tk.X, expand=True)

# Opções de Sexo
frame_sexo = tk.Frame(app)
frame_sexo.pack(fill=tk.X, padx=5, pady=5)
lbl_sexo = tk.Label(frame_sexo, text="Sexo", width=20)
lbl_sexo.pack(side=tk.LEFT)
sexo_var = tk.StringVar()
sexo_m = tk.Radiobutton(frame_sexo, text="Masculino", variable=sexo_var, value="Masculino")
sexo_f = tk.Radiobutton(frame_sexo, text="Feminino", variable=sexo_var, value="Feminino")
sexo_m.pack(side=tk.LEFT)
sexo_f.pack(side=tk.LEFT)

# Opções de Escolaridade
frame_escolaridade = tk.Frame(app)
frame_escolaridade.pack(fill=tk.X, padx=5, pady=5)
lbl_escolaridade = tk.Label(frame_escolaridade, text="Escolaridade", width=20)
lbl_escolaridade.pack(side=tk.LEFT)
escolaridade_var = tk.StringVar()
escolaridade_options = ["Ensino Infantil", "Ensino Fundamental", "Ensino Médio", "Ensino Superior"]
escolaridade_menu = ttk.Combobox(frame_escolaridade, textvariable=escolaridade_var, values=escolaridade_options, state='readonly')
escolaridade_menu.pack(fill=tk.X, expand=True)


# Campo de CID
frame_cid = tk.Frame(app)
frame_cid.pack(fill=tk.X, padx=5, pady=5)
lbl_cid = tk.Label(frame_cid, text="CID", width=20)
lbl_cid.pack(side=tk.LEFT)
cid_var = tk.StringVar()
cid_options = [
    "F70 - Retardo Mental Leve",
    "F71 - Retardo Mental Moderado",
    "F72 - Retardo Mental Grave",
    "F84 - Transtorno Espectro Autista"
]
cid_menu = ttk.Combobox(frame_cid, textvariable=cid_var, values=cid_options, state='readonly')
cid_menu.pack(fill=tk.X, expand=True)

# Campos de Benefício
frame_beneficio = tk.Frame(app)
frame_beneficio.pack(fill=tk.X, padx=5, pady=5)
bpc_var = tk.BooleanVar()
bolsa_var = tk.BooleanVar()
bpc_check = tk.Checkbutton(frame_beneficio, text="Recebe BPC", variable=bpc_var)
loas_check = tk.Checkbutton(frame_beneficio, text="Recebe LOAS", variable=bolsa_var)
bpc_check.pack(side=tk.LEFT)
loas_check.pack(side=tk.LEFT)

# Formatando campos
entries[1].bind("<KeyRelease>", format_date)
entries[2].bind("<KeyRelease>", format_cpf)
entries[3].bind("<KeyRelease>", format_phone)

# Criando o campo de visualização de dados
frame_tabela = tk.Frame(app)
frame_tabela.pack(fill=tk.BOTH, padx=5, pady=5)

tree = ttk.Treeview(frame_tabela, columns=("Nome", "Data de Nascimento", "CPF", "Telefone", "Bairro"), show='headings')
tree.heading("Nome", text="Nome")
tree.heading("Data de Nascimento", text="Data de Nascimento")
tree.heading("CPF", text="CPF")
tree.heading("Telefone", text="Telefone")
tree.heading("Bairro", text="Bairro")
tree.pack(fill=tk.BOTH, expand=True)

# Bind para clique duplo
tree.bind("<Double-1>", on_item_double_click)

# Botões
frame_buttons = tk.Frame(app)
frame_buttons.pack(fill=tk.X, padx=5, pady=5)
btn_cadastrar = tk.Button(frame_buttons, text="Cadastrar", command=cadastrar_alterar)
btn_alterar = tk.Button(frame_buttons, text="Alterar", command=alterar_dados)
btn_excluir = tk.Button(frame_buttons, text="Excluir", command=excluir)
btn_limpar = tk.Button(frame_buttons, text="Limpar", command=limpar)
btn_consultar = tk.Button(frame_buttons, text="Consultar", command=consultar)
btn_cadastrar.pack(side=tk.LEFT, padx=5)
btn_alterar.pack(side=tk.LEFT, padx=5)
btn_excluir.pack(side=tk.LEFT, padx=5)
btn_limpar.pack(side=tk.LEFT, padx=5)
btn_consultar.pack(side=tk.LEFT, padx=5)


# Criando um frame para a logo
logo_frame = tk.Frame(app, width=70, height=70)  # Ajuste o tamanho conforme necessário
logo_frame.pack_propagate(False)
logo_frame.place(relx=1.0, rely=1.0, anchor="se")

# logo redimensionamento
original_image = Image.open("apaeteresinalogo2.png")
width, height = original_image.size
aspect_ratio = width / height
new_width = 40  # Ajuste conforme necessário
new_height = int(new_width / aspect_ratio)

resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
logo_image = ImageTk.PhotoImage(resized_image)

# Criando um label para a imagem
logo_label = tk.Label(logo_frame, image=logo_image, bg=app.cget('bg'))
logo_label.image = logo_image  # Mantém uma referência
logo_label.pack(fill=tk.BOTH, expand=True)

# Criação do banco de dados
create_database()
# Atualiza a tabela ao iniciar
atualizar_tabela()

app.mainloop()
