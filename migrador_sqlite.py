import sqlite3
import pandas as pd

def conectar_banco(sqlite_file):
    try:
        con = sqlite3.connect(sqlite_file)
        return con
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def obter_tabelas(con):
    try:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = [row[0] for row in cur.fetchall()]
        return tabelas
    except Exception as e:
        print(f"Erro ao obter tabelas: {e}")
        return []

def exportar_para_excel(con, tabelas, arquivo_excel):
    try:
        dados_tabelas = {}
        
        for tabela in tabelas:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {tabela}")
            
            dados = cur.fetchall()

            df = pd.DataFrame(dados, columns=[desc[0] for desc in cur.description])
            dados_tabelas[tabela] = df

        with pd.ExcelWriter(arquivo_excel, engine='openpyxl') as writer:
            for tabela, df in dados_tabelas.items():
                df.to_excel(writer, sheet_name=tabela, index=False)

        print(f"Dados exportados com sucesso para {arquivo_excel}")
    except Exception as e:
        print(f"Erro ao exportar dados: {e}")

sqlite_file = "sqlite.db"

con = conectar_banco(sqlite_file)

if con:
    tabelas = obter_tabelas(con)

    if tabelas:
        arquivo_excel = "banco_exportado.xlsx"
        
        exportar_para_excel(con, tabelas, arquivo_excel)
    else:
        print("Nenhuma tabela encontrada no banco de dados.")
    
    con.close()
else:
    print("Não foi possível conectar ao banco de dados.")
