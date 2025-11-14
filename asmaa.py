from db_connect import connect_db
from datetime import datetime

# --- FUNKTION FÖR ATT DETEKTERA TRENDER ---
def detect_trend(isbn, start_period_1, end_period_1, start_period_2, end_period_2):
    conn = connect_db()      # anslut till databasen
    cur = conn.cursor()

    cur.execute("SELECT isbn, amount_units, date FROM sales_estimate_and_forecast;")
    rows = cur.fetchall()

    start_period_1 = datetime.strptime(start_period_1, "%Y-%m-%d").date()
    end_period_1   = datetime.strptime(end_period_1, "%Y-%m-%d").date()
    start_period_2 = datetime.strptime(start_period_2, "%Y-%m-%d").date()
    end_period_2   = datetime.strptime(end_period_2, "%Y-%m-%d").date()

    first_period = 0
    second_period = 0

    for row in rows:
        if start_period_1 <= row[2] <= end_period_1 and row[0] == isbn:
            first_period += float(row[1])

        if start_period_2 <= row[2] <= end_period_2 and row[0] == isbn:
            second_period += float(row[1])

    first_and_second = first_period + second_period
    if first_and_second == 0:
        cur.close()
        conn.close()
        return "Ingen försäljning registrerad under dessa perioder."

    andel_first_period = first_period / first_and_second
    andel_second_period = second_period / first_and_second

    cur.close()
    conn.close()

    if andel_first_period > andel_second_period:
        skillnad = andel_first_period - andel_second_period
        return f"Försäljningen minskade med {skillnad*100:.2f}% mellan perioderna."
    elif andel_second_period > andel_first_period:
        skillnad = andel_second_period - andel_first_period
        return f"Försäljningen ökade med {skillnad*100:.2f}% mellan perioderna."
    else:
        return "Försäljningen var oförändrad mellan perioderna."


# --- FUNKTION FÖR ATT DETEKTERA FÖRSÄLJNINGSAVVIKELSER ---
def detect_sales_anomalies(isbn, window_size=7, threshold=2):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT isbn, amount_units, date 
        FROM sales_estimate_and_forecast 
        WHERE isbn = %s 
        ORDER BY date
    """, (isbn,))
    rows = cur.fetchall()

    antal_fors = []

    for row in rows:
        dagens_forsaljning = float(row[1])
        dagens_datum = row[2]

        antal_fors.append(dagens_forsaljning)

        if len(antal_fors) > window_size:
            antal_fors.pop(0)

        if len(antal_fors) == window_size:
            medelvarde = sum(antal_fors) / len(antal_fors)

            if dagens_forsaljning > medelvarde * threshold:
                print(f" Spike {dagens_datum}: {dagens_forsaljning} vs {medelvarde:.2f}")
            elif dagens_forsaljning < medelvarde / threshold:
                print(f" Dip {dagens_datum}: {dagens_forsaljning} vs {medelvarde:.2f}")

    cur.close()
    conn.close()


# --- FUNKTION FÖR ATT BERÄKNA GLIDANDE MEDELVÄRDE ---
def calculate_moving_average(isbn, window_size=7):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT date, amount_units
        FROM sales_estimate_and_forecast
        WHERE isbn = %s
        ORDER BY date
    """, (isbn,))

    rows = cur.fetchall()

    sales_values = []
    dates = []
    moving_averages = []

    for row in rows:
        datum = row[0]
        antal = float(row[1])
        dates.append(datum)
        sales_values.append(antal)

    for i in range(len(sales_values)):
        if i + 1 >= window_size:
            window = sales_values[i + 1 - window_size : i + 1]
            avg = sum(window) / len(window)
            moving_averages.append((dates[i], avg))

    cur.close()
    conn.close()

    return moving_averages


# --- TESTKÖRNING (ta bort om du importerar funktionen i annan fil) ---
if __name__ == "__main__":
    isbn_test = "9780000000000"  # exempel ISBN
    print(detect_trend(isbn_test, "2024-01-01", "2024-03-31", "2024-04-01", "2024-06-30"))
    detect_sales_anomalies(isbn_test)
    print(calculate_moving_average(isbn_test))
