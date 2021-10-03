from psycopg2 import connect

table_name = "test"

conn = connect(
    dbname = "postgres",
    user = "postgres",
    host = "db",
    port = "5432",
    password = "123456"
)

cursor = conn.cursor()

cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id BIGINT, nom VARCHAR);")
cursor.close()
conn.close()