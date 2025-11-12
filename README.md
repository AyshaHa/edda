Projekt: Bokförsäljningsanalys med AI

Detta projekt analyserar försäljningsdata för böcker, hittar trender och avvikelser, pseudonymiserar data och genererar AI-baserade textinsikter och rekommendationer.
Syftet är att skapa ett system som kan ge tydliga rapporter och beslutsunderlag för bokförsäljning.
Gruppmedlemmar och ansvar

Isra – Datahantering och grundlogik
Ansvarar för att hämta, sammanställa och räkna ut försäljningsdata.

Asmaa – Trend- och tillväxtanalys
Jämför perioder och identifierar förändringar i försäljningen.

Aysha – Avvikelser och mönster
Upptäcker toppar, dippar och räknar ut intäkter.

Weronika – AI-förberedelse
Pseudonymiserar data för att skydda känslig information.

Safa – AI-analys och rekommendationer
Skapar textinsikter, förslag och grafer baserade på analysresultaten.

Filstruktur och beskrivning

db_connect.py
Hanterar anslutningen till PostgreSQL-databasen via psycopg2. Använder miljövariabler från .env-filen för att skydda känslig information.

isra_funktioner.py
Innehåller grundfunktioner för att hämta försäljningsdata, lista alla böcker och beräkna total försäljning per bok.

asmaa.py
Analyserar försäljningstrender mellan olika tidsperioder, hittar förändringar i försäljning och beräknar glidande medelvärden.

asho.py
Identifierar avvikelser och mönster i försäljningsdata. Tar fram bästsäljare, räknar ut total intäkt och markerar dagar med ovanliga försäljningsnivåer.

weronika.py
Pseudonymiserar bokdata genom att ersätta ISBN och titlar med tillfälliga namn, samt kan återöversätta dessa till original.

safa.py
Skapar textbaserade analyser och rekommendationer baserat på data från de andra modulerna. Kan även generera en graf över försäljning över tid.

main_test.py
Huvudfilen som kopplar ihop alla funktioner. Testar alla moduler i följd, skriver ut resultat och kör den fullständiga analysen.

Hur man kör projektet

Klona eller ladda ner projektet från GitHub.

Öppna mappen i Visual Studio Code.

Installera nödvändiga paket:
pip install psycopg2 python-dotenv matplotlib

Skapa en .env-fil i projektets rotmapp med följande variabler:
DB_HOST=eddapay-demo.c3oi0qmss74m.eu-north-1.rds.amazonaws.com
DB_NAME=postgres
DB_USER=postgres
DB_PASS=Projekt2024!
DB_PORT=5432
kör programmet :
python main_test.py

Funktioner i projektet

Hämtar och visar försäljningsdata från databas

Identifierar trender och tillväxt mellan olika perioder

Upptäcker avvikelser och räknar ut intäkter

Pseudonymiserar bokdata för säker AI-användning

Skapar textbaserade analyser och rekommendationer

(Valfritt) Genererar grafer över försäljning över tid