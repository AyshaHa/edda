def connect_db():

    return psycopg2.connect(

        host="eddapay-demo.c3oi0qmss74m.eu-north-1.rds.amazonaws.com",

        dbname="postgres",

        user="postgres",

        password="Projekt2024!",

        port="5432"

    )
 
 
# --- FUNKTION FÖR ATT HÄMTA FÖRSÄLJNINGSDATA ---

def get_sales_data(book_isbn=None):

    conn = connect_db()

    cur = conn.cursor()

    if book_isbn:

        cur.execute("""

            SELECT id, date, isbn, amount_units, amount_money, currency

            FROM public.sales_estimate_and_forecast

            WHERE isbn = %s;

        """, (book_isbn,))

    else:

        cur.execute("""

            SELECT id, date, isbn, amount_units, amount_money, currency

            FROM public.sales_estimate_and_forecast

            LIMIT 10;

        """)

    rows = cur.fetchall()

    conn.close()

    return rows
 
 
# --- HÄMTA ALLA BOKTITLAR ---

def get_all_books():

    conn = connect_db()

    cur = conn.cursor()

    cur.execute("SELECT DISTINCT isbn, title FROM public.book_metadata;")

    books = cur.fetchall()

    conn.close()

    return books
 
 
# --- RÄKNA TOTAL FÖRSÄLJNING AV EN BOK ---

def get_total_sales(book_isbn):

    conn = connect_db()

    cur = conn.cursor()

    cur.execute("""

        SELECT SUM(amount_units)

        FROM public.sales_estimate_and_forecast

        WHERE isbn = %s;

    """, (book_isbn,))

    total = cur.fetchone()[0]

    conn.close()

    return total
 
 
# --- TESTA ANALYSFUNKTIONERNA ---

print("\n===  FÖRSÄLJNINGSANALYS ===")
 
# 1. Hämta alla böcker

books = get_all_books()

print(f"\nTotalt antal böcker: {len(books)}")

print("Exempel på böcker:")

for isbn, title in books[:5]:

    print(f"  - {isbn} | {title}")
 
# 2. Hämta försäljningsdata (snyggt utskrivet)

print("\nFörsäljningsdata (5 rader):")

sales = get_sales_data()

print(f"{'ID':<4} {'Datum':<12} {'ISBN':<15} {'Antal':<7} {'Belopp (SEK)':<15} {'Valuta'}")

print("-" * 65)

for row in sales[:5]:

    id, date, isbn, amount_units, amount_money, currency = row

    print(f"{id:<4} {date} {isbn:<15} {amount_units:<7} {amount_money:<15} {currency}")
 
# 3. Räkna total försäljning för en specifik bok

book_isbn = books[0][0]  # hämtar ISBN för första boken

total_sales = get_total_sales(book_isbn)

print(f"\nTotal försäljning för ISBN {book_isbn}: {total_sales}\n")
 
 
