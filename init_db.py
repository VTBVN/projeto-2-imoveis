from database import connect_db

conn = connect_db()
if not conn:
    print("Erro: Falha na conexao com o banco de dados. Verifique o arquivo .env")
    exit(1)

try:
    cursor = conn.cursor()
    with open('schema.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    for comando in sql.split(';'):
        if comando.strip():
            cursor.execute(comando)
    conn.commit()
    print("Sucesso: Tabela imoveis criada e populada no Aiven com sucesso.")
except Exception as e:
    print(f"Erro ao executar o schema: {e}")
finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if conn and conn.is_connected():
        conn.close()
