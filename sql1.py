import sqlite3
import csv

# Funksjon for å opprette tabell
def opprett_tabell(conn):
    var_cursor = conn.cursor()
    var_cursor.execute("""
    CREATE TABLE IF NOT EXISTS personer (
        id INTEGER PRIMARY KEY,
        fornavn TEXT,
        etternavn TEXT,
        epost TEXT,
        telefon TEXT,
        postnummer TEXT
    )
    """)
    conn.commit()

# Funksjon for å lese data fra CSV-fil og legge til i databasen
def legg_til_data_fra_csv(conn, filnavn):
    var_cursor = conn.cursor()
    with open(filnavn, 'r') as fil:
        var_reader = csv.reader(fil)
        next(var_reader)  # Hopper over header
        for var_rad in var_reader:
            var_fornavn, var_etternavn, var_epost, var_telefon, var_postnummer = var_rad
            var_cursor.execute("INSERT INTO personer (fornavn, etternavn, epost, telefon, postnummer) VALUES (?, ?, ?, ?, ?)",
                           (var_fornavn, var_etternavn, var_epost, var_telefon, var_postnummer))
    conn.commit()

# Funksjon for å koble til databasen
def koble_til_database(database_navn):
    var_conn = sqlite3.connect(database_navn)
    return var_conn

# Funsjon for å lukke tilkoblingen til databasen
def lukk_tilkobling(conn):
    conn.close()

# Main funksjon
def main():
    var_database_navn = "min_database.db"
    var_csv_filnavn = "randoms.csv"

    # Koble til databasen
    var_conn = koble_til_database(var_database_navn)

    # Opprett tabell
    opprett_tabell(var_conn)

    # Legg inn data fra CSV-fil
    legg_til_data_fra_csv(var_conn, var_csv_filnavn)

    # Lukk koblingen til databasen
    lukk_tilkobling(var_conn)

if __name__ == "__main__":
    main()