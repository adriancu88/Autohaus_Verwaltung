from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Datenbank-Konfigurationsdetails
db_config = {
    'user': 'user',
    'password': 'pa$$w0rd',
    'host': 'localhost',
    'database': 'autohaus_verwaltungssystem',
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT k.kundeid, k.vorname, k.nachname, k.adresse, k.telefonnummer, 
           v.rechnungsnummer, v.verkaufsdatum,
           f.marke, f.modell, f.farbe, f.preis,
           w.beschreibung, w.kosten, w.datum
    FROM Kunden k
    LEFT JOIN Verkaeufe v ON k.kundeid = v.kundeid
    LEFT JOIN Fahrzeuge f ON v.fahrzeugid = f.fahrzeugid
    LEFT JOIN Wartungen w ON f.fahrzeugid = w.fahrzeugid
    WHERE k.nachname = %s
    """
    params = (search_term,)

    cursor.execute(query, params)
    customer_info = cursor.fetchone()

    cursor.close()
    conn.close()

    if customer_info:
        return render_template('search_results.html', customer_info=customer_info)
    else:
        return render_template('search_results.html', not_found=True)

if __name__ == '__main__':
    app.run(debug=True)

