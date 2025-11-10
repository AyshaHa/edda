import psycopg2




# Anslutning till databasen
def connect_db():
    return psycopg2.connect(
        host="eddapay-demo.c3oi0qmss74m.eu-north-1.rds.amazonaws.com",
        dbname="postgres",
        user="postgres",
        password="Projekt2024!",
        port="5432"
    )




# Hämta försäljningsdata (kan filtreras)
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




# Hämta alla boktitlar
def get_all_books():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT isbn, title FROM public.book_metadata;")
    books = cur.fetchall()
    conn.close()
    return books




# Räkna totala försäljningen av en bok
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




# Testa funktionerna
print(" Alla böcker:", get_all_books()[:5])
print("\nTotal försäljning:", get_total_sales("Your Book Title"))
print("\nExempel på försäljningsdata:", get_sales_data("Your Book Title")[:3])
