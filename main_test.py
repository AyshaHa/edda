from safa import generate_text_insight, suggest_actions, plot_sales_over_time
from db_connect import connect_db
from isra_funktioner import get_all_books, get_sales_data, get_total_sales
from asmaa import detect_trend, detect_sales_anomalies, calculate_moving_average
from asho import best_sellers, anomalies_by_day, total_revenue
from samina import pseudonymize_data, translate_pseudonyms_back


def main():
    print("=== TEST AV HELA PROJEKTET ===")

    #  Databasanslutning
    conn = connect_db()
    if not conn:
        print("Kunde inte ansluta till databasen")
        return
    print(" Ansluten till databasen\n")

    # 2 Isra – Datahantering
    print("=== Isra – Datahantering ===")
    books = get_all_books()
    print("Antal böcker:", len(books))
    print("Exempel:", books[:3])

    print("\nTotal försäljning av testbok:")
    print(get_total_sales("9780000000000"))

    print("\nFörsäljningsdata (exempel):")
    print(get_sales_data("9780000000000")[:3])

    #  Asmaa – Trend & tillväxt
    print("\n=== Asmaa – Trend & tillväxt ===")
    print(detect_trend("9780000000000", "2024-01-01", "2024-03-31", "2024-04-01", "2024-06-30"))
    detect_sales_anomalies("9780000000000")
    print(calculate_moving_average("9780000000000")[:5])

    #  Aysha – Avvikelser & mönster
    print("\n=== Aysha – Avvikelser & mönster ===")
    print("Bästsäljare:")
    print(best_sellers(conn, limit=5))
    print("\nAvvikelser per dag:")
    print(anomalies_by_day(conn, z_limit=2.0))
    print("\nTotal intäkt:", total_revenue(conn))

    # Weronika – AI-förberedelse
    print("\n=== Weronika – Pseudonymisering ===")
    pseudonymize_data()
    translate_pseudonyms_back()

    #  Avslut
    conn.close()
    print("\n Allt klart!")


if __name__ == "__main__":
    main()
    print("\n=== Safa – AI-analys & rekommendationer ===")
    text = generate_text_insight("Försäljningen ökade med 25% mellan perioderna.", 4406390851.59, [])
    print(text)
    for s in suggest_actions("Försäljningen ökade med 25% mellan perioderna.", 4406390851.59, []):
        print("-", s)

    # (Valfritt) Visa graf
    # plot_sales_over_time(fake_sales_data)
