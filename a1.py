import psycopg2
import json
import random

# --- ANSLUTNINGSTEST ---
try:
    conn = psycopg2.connect(
        host="eddapay-demo.c3oi0qmss74m.eu-north-1.rds.amazonaws.com",
        dbname="postgres",
        user="postgres",
        password="Projekt2024!",
        port="5432"
    )
    print("\n Anslutningen fungerar!")
except Exception as e:
    print("Något gick fel:", e)


# --- FUNKTION FÖR PSEUDONYMISERING ---
def pseudonymize_data():
    conn = psycopg2.connect(
        host="eddapay-demo.c3oi0qmss74m.eu-north-1.rds.amazonaws.com",
        dbname="postgres",
        user="postgres",
        password="Projekt2024!",
        port="5432"
    )
    cur = conn.cursor()

    cur.execute('SELECT isbn, title FROM public."book_metadata" LIMIT 5;')
    rows = cur.fetchall()
    mapping = {}
    pseudonymized = []

    for isbn, title in rows:
        fake_isbn = f"BOOK_{random.randint(1000,9999)}"
        fake_title = f"Title_{random.randint(1000,9999)}"
        mapping[fake_isbn] = {"isbn": isbn, "title": title}
        pseudonymized.append((fake_isbn, fake_title))

    with open("mapping.json", "w") as f:
        json.dump(mapping, f)

    print("\n===  PSEUDONYMISERAD DATA ===")
    for fake_isbn, fake_title in pseudonymized:
        print(f"  - {fake_isbn} | {fake_title}")

    cur.close()
    conn.close()


# --- FUNKTION FÖR ATT ÅTERÖVERSÄTTA DATA ---
def translate_pseudonyms_back():
    with open("mapping.json", "r") as f:
        mapping = json.load(f)

    result = []
    for fake_isbn, real_data in mapping.items():
        result.append((real_data["isbn"], real_data["title"]))

    print("\n===  ÅTERÖVERSATT DATA ===")
    for real_isbn, real_title in result:
        print(f"  - {real_isbn} | {real_title}")
    print()  # extra rad för mellanrum


# --- KÖR FUNKTIONERNA ---
pseudonymize_data()
translate_pseudonyms_back()


