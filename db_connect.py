import psycopg2
import os
from dotenv import load_dotenv

# Ladda miljövariablerna från .env
load_dotenv()

def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )

if __name__ == "__main__":
    try:
        conn = connect_db()
        print(" Anslutning till databasen lyckades!")
        conn.close()
    except Exception as e:
        print(" Fel vid anslutning:", e)
