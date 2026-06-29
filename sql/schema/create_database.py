from db_connection import get_connection

conn = get_connection()

conn.autocommit = True

cur = conn.cursor()

db_name = "warehouse_db"   # ya os.getenv("DB_NAME")

cur.execute(
    "SELECT 1 FROM pg_database WHERE datname = %s",
    (db_name,)
)

exists = cur.fetchone()

if exists:
    print(f"Database '{db_name}' already exists.")
else:
    cur.execute(f'CREATE DATABASE "{db_name}"')
    print(f"Database '{db_name}' created successfully.")

cur.close()
conn.close()