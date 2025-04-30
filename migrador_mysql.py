import mysql.connector
import pandas as pd
import os

MYSQL_HOST = "localhost"
MYSQL_USER = "root"  
MYSQL_PASSWORD = "1234"  
DATABASE_NAME = "temp_db"  

SQL_DUMP_FILE = "mysql.sql"

EXCEL_FILE = "excel_mysql.xlsx"

def executar_script_sql(cursor, arquivo_sql):
    with open(arquivo_sql, "r", encoding="utf-8") as f:
        comandos = f.read().split(";")  
        for comando in comandos:
            comando = comando.strip()
            if comando:
                cursor.execute(comando)

def exportar_para_excel(conn, nome_arquivo):
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tabelas = [t[0] for t in cursor.fetchall()]

    with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
        for tabela in tabelas:
            df = pd.read_sql(f"SELECT * FROM {tabela}", conn)
            df.to_excel(writer, sheet_name=tabela, index=False)
            print(f"Tabela '{tabela}' exportada.")

def main():
    try:
        conn = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD)
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
        print(f"Banco de dados '{DATABASE_NAME}' criado.")

        conn.database = DATABASE_NAME

        executar_script_sql(cursor, SQL_DUMP_FILE)
        conn.commit()
        print("Banco de dados populado.")

        exportar_para_excel(conn, EXCEL_FILE)
        print(f"Dados exportados para '{EXCEL_FILE}'.")

    except mysql.connector.Error as err:
        print(f"Erro: {err}")

    finally:
        if "conn" in locals():
            conn.close()

        conn = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD)
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE {DATABASE_NAME}")
        conn.commit()
        print(f"Banco de dados '{DATABASE_NAME}' excluído.")

if __name__ == "__main__":
    main()
