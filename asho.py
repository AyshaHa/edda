from db_connect import connect_db   # 🔹 använder din befintliga databasanslutning
from psycopg2.extras import RealDictCursor
from math import sqrt

# 1) Hjälpfunktioner
def run_query(conn, sql, params=()):
    """Kör SQL och returnerar listan med rader som dict."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()

def build_where(start=None, end=None, currency=None):
    """Bygger WHERE-del och parameterlista utifrån filter."""
    parts, p = [], []
    if start:
        parts.append('"date" >= %s'); p.append(start)
    if end:
        parts.append('"date" < %s');  p.append(end)
    if currency:
        parts.append('"currency" = %s'); p.append(currency)
    return ("WHERE " + " AND ".join(parts)) if parts else "", p

def print_table(rows, cols):
    """Skriv ut enkel tabell i terminalen."""
    if not rows:
        print("(inga rader)\n"); return
    widths = [max(len(c), max(len(str(r.get(c, ""))) for r in rows)) for c in cols]
    header = " | ".join(c.ljust(widths[i]) for i, c in enumerate(cols))
    line   = "-+-".join("-" * w for w in widths)
    print(header); print(line)
    for r in rows:
        print(" | ".join(str(r.get(c, "")).ljust(widths[i]) for i, c in enumerate(cols)))
    print()

# 2) Bästsäljare 
def best_sellers(conn, limit=10, sort_by="qty", start=None, end=None, currency=None):
    """
    sort_by: 'qty' (på antal) eller 'revenue' (på intäkt)
    Returnerar rader: isbn, total_qty, revenue
    """
    where, p = build_where(start, end, currency)
    order = 'SUM(COALESCE("amount_units",0))' if sort_by == "qty" else 'SUM(COALESCE("amount_money",0))'
    sql = f'''
      SELECT
        "isbn",
        SUM(COALESCE("amount_units",0))::bigint   AS total_qty,
        SUM(COALESCE("amount_money",0))::numeric(18,2) AS revenue
      FROM "sales_estimate_and_forecast"
      {where}
      GROUP BY "isbn"
      ORDER BY {order} DESC
      LIMIT %s
    '''
    return run_query(conn, sql, (*p, limit))

# 3) Avvikelser per dag (z-score)
def anomalies_by_day(conn, start=None, end=None, currency=None, z_limit=2.0):
    """
    Räknar antal per dag och markerar dagar som sticker ut.
    Returnerar rader: period_start, value, z, kind
    """
    where, p = build_where(start, end, currency)
    sql = f'''
      SELECT "date"::timestamp AS period_start,
             SUM(COALESCE("amount_units",0))     AS value
      FROM "sales_estimate_and_forecast"
      {where}
      GROUP BY 1
      ORDER BY 1
    '''
    rows = run_query(conn, sql, p)
    if not rows:
        return []

    values = [float(r["value"] or 0) for r in rows]
    mean = sum(values) / len(values)
    var  = sum((v - mean) ** 2 for v in values) / len(values) if len(values) > 1 else 0.0
    std  = sqrt(var) if var > 0 else 0.0
    if std == 0:
        return []

    out = []
    for r in rows:
        z = (float(r["value"]) - mean) / std
        if abs(z) >= z_limit:
            out.append({
                "period_start": r["period_start"],
                "value": r["value"],
                "z": round(z, 2),
                "kind": "spike" if z > 0 else "dip",
            })
    return out

# 4) Total intäkt 
def total_revenue(conn, start=None, end=None, currency=None, isbn=None):
    """Returnerar ett tal (float) med total intäkt."""
    where, p = build_where(start, end, currency)
    if isbn:
        where += (" AND " if where else "WHERE ") + '"isbn" = %s'
        p.append(isbn)
    row = run_query(conn, f'''
      SELECT SUM(COALESCE("amount_money",0))::numeric(18,2) AS revenue
      FROM "sales_estimate_and_forecast" {where}
    ''', p)
    return float(row[0]["revenue"] or 0.0) if row else 0.0

# 5) Kör enkel rapport 
if __name__ == "__main__":
    conn = connect_db()   # 🔹 använd din gemensamma databasanslutning

    # Filter (kan ändras vid behov)
    START = None   # t.ex. '2024-01-01'
    END   = None   # t.ex. '2025-01-01'
    CURR  = None   # t.ex. 'SEK'

    print("Bästsäljare (antal)")
    print_table(best_sellers(conn, limit=10, sort_by="qty", start=START, end=END, currency=CURR),
                ["isbn", "total_qty", "revenue"])

    print("Bästsäljare (intäkt)")
    print_table(best_sellers(conn, limit=10, sort_by="revenue", start=START, end=END, currency=CURR),
                ["isbn", "total_qty", "revenue"])

    print("Avvikelser per dag (antal)")
    print_table(anomalies_by_day(conn, start=START, end=END, currency=CURR),
                ["period_start", "value", "z", "kind"])

    print("Total intäkt")
    print(f'{total_revenue(conn, start=START, end=END, currency=CURR):,.2f}'.replace(",", " "))

    conn.close()
