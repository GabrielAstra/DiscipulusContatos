import sqlite3

conn = sqlite3.connect('contatos.db')
cursor = conn.cursor()

create_table_sql = '''
CREATE TABLE IF NOT EXISTS Contato (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    contato TEXT NOT NULL,
    habilidade TEXT,
    email TEXT
);
'''

cursor.execute(create_table_sql)

conn.commit()
conn.close()
