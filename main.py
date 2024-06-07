import customtkinter as ctk
import sqlite3
from contexto import create_table_sql

def salvar_contato():
    nome = entry_nome.get()
    contato = entry_contato.get()
    habilidade = entry_habilidade.get()
    email = entry_email.get()

    if nome and contato:
        conn = sqlite3.connect('contatos.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Contato (nome, contato, habilidade, email) VALUES (?, ?, ?, ?)",
                       (nome, contato, habilidade, email))
        
        conn.commit()
        conn.close()

        entry_nome.delete(0, ctk.END)
        entry_contato.delete(0, ctk.END)
        entry_habilidade.delete(0, ctk.END)
        entry_email.delete(0, ctk.END)

        update_table()
        
        ctk.messagebox.showinfo("Sucesso", "Contato salvo com sucesso!")
    else:
        ctk.messagebox.showerror("Erro", "Por favor, preencha o nome e o contato.")

def update_table():
    for widget in tabela.winfo_children():
        widget.destroy()

    conn = sqlite3.connect('contatos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome, contato, habilidade, email FROM Contato")
    dados_contatos = cursor.fetchall()
    conn.close()

    for i, dados in enumerate(dados_contatos):
        for j, dado in enumerate(dados):
            ctk_label = ctk.CTkLabel(tabela, text=dado)
            ctk_label.grid(row=i, column=j, padx=5, pady=5)

app = ctk.CTk()
app.title("Aplicativo de Contatos")

label_nome = ctk.CTkLabel(app, text="Nome:")
label_nome.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="w")
entry_nome = ctk.CTkEntry(app)
entry_nome.grid(row=0, column=1, padx=10, pady=(20, 5))

label_contato = ctk.CTkLabel(app, text="Contato:")
label_contato.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_contato = ctk.CTkEntry(app)
entry_contato.grid(row=1, column=1, padx=10, pady=5)

label_habilidade = ctk.CTkLabel(app, text="Habilidade:")
label_habilidade.grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_habilidade = ctk.CTkEntry(app)
entry_habilidade.grid(row=2, column=1, padx=10, pady=5)

label_email = ctk.CTkLabel(app, text="Email:")
label_email.grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_email = ctk.CTkEntry(app)
entry_email.grid(row=3, column=1, padx=10, pady=5)

button_salvar = ctk.CTkButton(app, text="Salvar", command=salvar_contato)
button_salvar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

tabela = ctk.CTkFrame(app)
tabela.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

for i in range(5):
    app.grid_rowconfigure(i, weight=1)
app.grid_rowconfigure(5, weight=10)
for i in range(2):
    app.grid_columnconfigure(i, weight=1)

app.mainloop()
