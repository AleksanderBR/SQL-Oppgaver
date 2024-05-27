import sqlite3
import csv

# Funksjon for å opprette tabeller
def opprett_tabeller(conn):
    var_cursor = conn.cursor()
    # Opprett personer tabell
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
    # Opprett postnummer tabell
    var_cursor.execute("""
    CREATE TABLE IF NOT EXISTS postnummer (
        Postnummer TEXT PRIMARY KEY,
        Poststed TEXT,
        Kommunenummer TEXT,
        Kommunenavn TEXT,
        Kategori TEXT
    )
    """)
    conn.commit()

# Funksjon for å lese data fra personer CSV-fil og legge til i databasen
def legg_til_data_fra_csv_personer(conn, filnavn):
    var_cursor = conn.cursor()
    with open(filnavn, 'r', encoding='utf-8') as fil:
        var_reader = csv.reader(fil)
        next(var_reader)  # Hopper over header
        for var_rad in var_reader:
            var_fornavn, var_etternavn, var_epost, var_telefon, var_postnummer = var_rad
            var_cursor.execute("INSERT INTO personer (fornavn, etternavn, epost, telefon, postnummer) VALUES (?, ?, ?, ?, ?)",
                           (var_fornavn, var_etternavn, var_epost, var_telefon, var_postnummer))
    conn.commit()

# Funksjon for å lese data fra postnummer CSV-fil og legge til i databasen
def legg_til_data_fra_csv_postnummer(conn, filnavn):
    var_cursor = conn.cursor()
    with open(filnavn, 'r', encoding='utf-8') as fil:
        var_reader = csv.reader(fil, delimiter=';')
        next(var_reader)  # Hopper over header
        for var_rad in var_reader:
            var_postnummer, var_poststed, var_kommunenummer, var_kommunenavn, var_kategori = var_rad
            var_cursor.execute("INSERT INTO postnummer (Postnummer, Poststed, Kommunenummer, Kommunenavn, Kategori) VALUES (?, ?, ?, ?, ?)",
                           (var_postnummer, var_poststed, var_kommunenummer, var_kommunenavn, var_kategori))
    conn.commit()

# Funksjon for å koble til databasen
def koble_til_database(database_navn):
    return sqlite3.connect(database_navn)

# Funksjon for å lukke tilkoblingen til databasen
def lukk_tilkobling(conn):
    if conn:
        conn.close()

# Main funksjon
def main():
    var_database_navn = "min_database_sql2.db"
    var_personer_csv_filnavn = "randoms.csv"
    var_postnummer_csv_filnavn = "Postnummerregister.csv"

    # Koble til databasen
    var_conn = koble_til_database(var_database_navn)

    # Opprett tabeller
    opprett_tabeller(var_conn)

    # Legg inn data fra personer CSV-fil
    legg_til_data_fra_csv_personer(var_conn, var_personer_csv_filnavn)

    # Legg inn data fra postnummer CSV-fil
    legg_til_data_fra_csv_postnummer(var_conn, var_postnummer_csv_filnavn)

    # Lukk koblingen til databasen
    lukk_tilkobling(var_conn)

if __name__ == "__main__":
    main()
