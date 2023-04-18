import requests as req
import psycopg2
from flask import Flask, jsonify
app = Flask(__name__)

# Połączenie z bazą danych PostgreSQL
conn = psycopg2.connect(
    host="195.150.230.208",
    port=5432,
    database="2022_ciochon_adrian",
    user="2022_ciochon_adrian",
    password="34275"
)

cur = conn.cursor()

# Tworzenie tabeli w bazie danych
#cur.execute(
#    "CREATE TABLE IF NOT EXISTS exchange.kurs (id_waluty SERIAL PRIMARY KEY, currency CHARACTER(50), code CHARACTER(5), mid CHARACTER(10));")


# Endpoint API NBP
url = 'http://api.nbp.pl/api/exchangerates/tables/a/'

# Pobranie danych z API NBP
response = req.get(url)
data = response.json()[0]['rates']

# Zapis danych do bazy danych PostgreSQL
for item in data:
    cur.execute("INSERT INTO exchange.kurs (currency, code, mid) VALUES (%s, %s, %s)",
                (item['currency'], item['code'], item['mid']))
conn.commit()




#@app.route('/')
#def index():
#    # Pobranie danych z bazy danych PostgreSQL
#    cur.execute("SELECT * FROM exchange.kurs ORDER BY id_waluty DESC LIMIT 33")
#    rows = cur.fetchall()
#    return render_template('index.html', rows=rows)

@app.route('/currency')
def currency():
    rates = []
    for currency in data:
        rates.append({
            "currency": currency['currency'],
            'code': currency['code'],
            'mid': currency['mid']
        })
    return jsonify({"Rates": rates})

if __name__ == '__main__':
    app.run(debug=True)










