import customtkinter as ctk
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

pagina = 0
itens_por_pagina = 10

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
        
        ctk.messagebox.showinfo("Sucesso", "Contato salvo")
    else:
        ctk.messagebox.showerror("Erro", "Falta nome ou contato")

def update_table():
    for widget in tabela.winfo_children():
        widget.destroy()

    conn = sqlite3.connect('contatos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome, contato, habilidade, email FROM Contato")
    dados_contatos = cursor.fetchall()
    conn.close()

    global pagina, itens_por_pagina
    start_index = pagina * itens_por_pagina
    end_index = start_index + itens_por_pagina
    page_data = dados_contatos[start_index:end_index]

    for i, dados in enumerate(page_data):
        for j, dado in enumerate(dados):
            ctk_label = ctk.CTkLabel(tabela, text=dado)
            ctk_label.grid(row=i, column=j, padx=5, pady=5)

    button_previous_page.configure(state=ctk.NORMAL if pagina > 0 else ctk.DISABLED)
    button_next_page.configure(state=ctk.NORMAL if end_index < len(dados_contatos) else ctk.DISABLED)

def previous_page():
    global pagina
    if pagina > 0:
        pagina -= 1
        update_table()

def next_page():
    global pagina
    pagina += 1
    update_table()

def abrir_janela_email():
    janela_email = ctk.CTkToplevel()
    janela_email.title("Envio de Emails em Massa")

    label_assunto = ctk.CTkLabel(janela_email, text="Assunto:")
    label_assunto.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="w")
    entry_assunto = ctk.CTkEntry(janela_email)
    entry_assunto.grid(row=0, column=1, padx=10, pady=(20, 5))

    label_mensagem = ctk.CTkLabel(janela_email, text="Mensagem:")
    label_mensagem.grid(row=1, column=0, padx=10, pady=5, sticky="nw")
    text_mensagem = ctk.CTkText(janela_email, height=10, width=50)
    text_mensagem.grid(row=1, column=1, padx=10, pady=5)

    button_enviar = ctk.CTkButton(janela_email, text="Enviar", command=lambda: enviar_emails(entry_assunto.get(), text_mensagem.get("1.0", ctk.END)))
    button_enviar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

def enviar_emails(assunto, mensagem):
    conn = sqlite3.connect('contatos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM Contato")
    emails = cursor.fetchall()
    conn.close()

    emails = [email[0] for email in emails]

    smtp_server = ""
    smtp_port = 587 
    sender_email = ""
    sender_password = ""
 ## lembrar de preencher e terminar configuração para envio de emails em massa
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        for email in emails:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = assunto

            msg.attach(MIMEText(mensagem, 'plain'))

            server.sendmail(sender_email, email, msg.as_string())

        server.quit()

        ctk.messagebox.showinfo("Sucesso", "Emails enviados com sucesso")
    except Exception as e:
        ctk.messagebox.showerror("Erro", f"Erro ao enviar emails: {e}")

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

button_enviar_email = ctk.CTkButton(app, text="Enviar Emails em Massa", command=abrir_janela_email)
button_enviar_email.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

tabela = ctk.CTkFrame(app)
tabela.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

button_previous_page = ctk.CTkButton(app, text="Página Anterior", command=previous_page)
button_previous_page.grid(row=7, column=0, padx=10, pady=10, sticky="w")

button_next_page = ctk.CTkButton(app, text="Próxima Página", command=next_page)
button_next_page.grid(row=7, column=1, padx=10, pady=10, sticky="e")

for i in range(6):
    app.grid_rowconfigure(i, weight=1)
app.grid_rowconfigure(6, weight=10)
app.grid_rowconfigure(7, weight=1)
for i in range(2):
    app.grid_columnconfigure(i, weight=1)

update_table()

app.mainloop()
