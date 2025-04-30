import psycopg2
import pandas as pd
import os

PG_HOST = "localhost"
PG_USER = "postgres"
PG_PASSWORD = "1234"
PG_PORT = "5432"
DATABASE_NAME = "temp_db"

SQL_DUMP_FILE = "postgre.sql"

EXCEL_FILE = "excel_postgre.xlsx"

def criar_banco_de_dados():
    conn = psycopg2.connect(host=PG_HOST, user=PG_USER, password=PG_PASSWORD, port=PG_PORT)
    conn.autocommit = True  
    cursor = conn.cursor()
    
    cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
    print(f"Banco de dados '{DATABASE_NAME}' criado.")
    
    cursor.close()
    conn.close()

def restaurar_banco_de_dados():
    conn = psycopg2.connect(host=PG_HOST, user=PG_USER, password=PG_PASSWORD, dbname=DATABASE_NAME, port=PG_PORT)
    cursor = conn.cursor()
    
    with open(SQL_DUMP_FILE, "r", encoding="utf-8") as file:
        sql_script = file.read()
    
    cursor.execute(sql_script)
    conn.commit()
    print(f"Banco de dados restaurado a partir de '{SQL_DUMP_FILE}'.")
    
    cursor.close()
    conn.close()

def exportar_para_excel():
    conn = psycopg2.connect(host=PG_HOST, user=PG_USER, password=PG_PASSWORD, dbname=DATABASE_NAME, port=PG_PORT)
    cursor = conn.cursor()
    
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tabelas = [t[0] for t in cursor.fetchall()]
    
    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
        for tabela in tabelas:
            df = pd.read_sql(f"SELECT * FROM {tabela}", conn)
            df.to_excel(writer, sheet_name=tabela, index=False)
            print(f"Tabela '{tabela}' exportada para o Excel.")
    
    cursor.close()
    conn.close()

def excluir_banco_de_dados():
    conn = psycopg2.connect(host=PG_HOST, user=PG_USER, password=PG_PASSWORD, port=PG_PORT)
    conn.autocommit = True  
    cursor = conn.cursor()
    
    cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME}")
    print(f"Banco de dados '{DATABASE_NAME}' excluído.")
    
    cursor.close()
    conn.close()

def main():
    try:
        criar_banco_de_dados()
        
        restaurar_banco_de_dados()
        
        exportar_para_excel()

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        excluir_banco_de_dados()

if __name__ == "__main__":
    main()
