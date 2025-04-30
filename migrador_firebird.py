import fdb
import pandas as pd

def conectar_banco(fdb_file):
    try:
        con = fdb.connect(dsn=f"localhost:{fdb_file}", user="SYSDBA", password="1234",charset='WIN1252')
        return con
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def obter_tabelas(con):
    try:
        cur = con.cursor()
        cur.execute("SELECT RDB$RELATION_NAME FROM RDB$RELATIONS WHERE RDB$SYSTEM_FLAG = 0")
        tabelas = [row[0].strip() for row in cur.fetchall()]
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

fdb_file = "C:\Program Files\Firebird\Firebird_5_0\databases\GERCOM_RESTAURADO.FDB"

con = conectar_banco(fdb_file)

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
