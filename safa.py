import matplotlib.pyplot as plt
from datetime import datetime
import random

# --- GENERATE TEXT INSIGHT ---
def generate_text_insight(trend_data, revenue, anomalies):
    """
    Skapar naturlig text som sammanfattar försäljningstrender, intäkt och avvikelser.
    """
    text = "Försäljningsrapport:\n\n"

    #  Trendinfo
    if "ökade" in trend_data:
        text += f"{trend_data.capitalize()} Detta tyder på en positiv utveckling.\n"
    elif "minskade" in trend_data:
        text += f"{trend_data.capitalize()} Det kan vara bra att undersöka orsaken till nedgången.\n"
    else:
        text += f"{trend_data}\n"

    #  Intäkter
    text += f"\nTotala intäkter under perioden: {revenue:,.0f} SEK.\n"

    #  Avvikelser
    if anomalies and len(anomalies) > 0:
        text += f"\nAntal dagar med avvikande försäljning: {len(anomalies)}.\n"
        text += "Exempel på toppar: " + ", ".join([a['period_start'].strftime("%Y-%m-%d") for a in anomalies[:3]]) + "...\n"
    else:
        text += "\nInga större avvikelser upptäckta.\n"

    return text


# --- SUGGEST ACTIONS ---
def suggest_actions(trend_data, revenue, anomalies):
    """
    Ger rekommendationer baserat på trend och avvikelser.
    """
    suggestions = []

    if "ökade" in trend_data:
        suggestions.append("Fortsätt marknadsföra boken på samma sätt – nuvarande strategi fungerar bra.")
    elif "minskade" in trend_data:
        suggestions.append("Överväg en kampanj eller rabatt för att öka intresset.")
    else:
        suggestions.append("Testa nya sätt att väcka intresse – exempelvis sociala medier eller samarbeten.")

    if revenue < 100000:
        suggestions.append("Försäljningen är låg – fokusera på synlighet online.")
    elif revenue > 1000000:
        suggestions.append("Storsäljare! Utöka lagret och överväg internationell marknadsföring.")

    if anomalies and len(anomalies) > 0:
        suggestions.append("Analysera vad som orsakade topparna – till exempel marknadsföring eller helger.")

    return suggestions


# --- PLOT SALES OVER TIME ---
def plot_sales_over_time(sales_data):
    """
    Skapar en graf över försäljning över tid.
    sales_data ska vara en lista av tuples: [(date, amount_units), ...]
    """
    if not sales_data:
        print("Ingen försäljningsdata tillgänglig för grafen.")
        return

    dates = [d[0] for d in sales_data]
    values = [float(d[1]) for d in sales_data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, values, marker='o', linestyle='-', linewidth=2)
    plt.title("Försäljning över tid")
    plt.xlabel("Datum")
    plt.ylabel("Antal sålda enheter")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# --- TESTA FUNKTIONER ---
if __name__ == "__main__":
    fake_trend = "Försäljningen ökade med 25% mellan perioderna."
    fake_revenue = 500000
    fake_anomalies = [
        {"period_start": datetime(2025, 5, 1), "value": 10000},
        {"period_start": datetime(2025, 6, 15), "value": 15000},
    ]
    fake_sales = [(datetime(2025, i, 1), random.randint(5000, 20000)) for i in range(1, 7)]

    print(generate_text_insight(fake_trend, fake_revenue, fake_anomalies))
    print("\nRekommendationer:")
    for s in suggest_actions(fake_trend, fake_revenue, fake_anomalies):
        print(" -", s)

    plot_sales_over_time(fake_sales)
