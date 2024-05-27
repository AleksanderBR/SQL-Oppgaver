import sqlite3
import csv

# Funksjon for å opprette tabeller
def opprett_tabeller(conn):
    var_cursor = conn.cursor()
    # Opprett kundeinfo tabell
    var_cursor.execute("""
    CREATE TABLE IF NOT EXISTS kundeinfo (
        kundenummer INTEGER PRIMARY KEY,
        fornavn TEXT,
        etternavn TEXT,
        epost TEXT,
        telefon TEXT,
        postnummer TEXT,
        FOREIGN KEY (postnummer) REFERENCES postnummer_tabell(Postnummer)
    )
    """)
    # Opprett postnummer tabell
    var_cursor.execute("""
    CREATE TABLE IF NOT EXISTS postnummer_tabell (
        Postnummer TEXT PRIMARY KEY,
        Poststed TEXT,
        Kommunenummer TEXT,
        Kommunenavn TEXT,
        Kategori TEXT
    )
    """)
    conn.commit()

# Funksjon for å lese data fra kundeinfo CSV-fil og legge til i databasen
def legg_til_data_fra_csv_kundeinfo(conn, filnavn):
    var_cursor = conn.cursor()
    with open(filnavn, 'r', encoding='utf-8') as fil:
        var_reader = csv.reader(fil)
        next(var_reader)  # Hopper over header
        for var_rad in var_reader:
            var_fornavn, var_etternavn, var_epost, var_telefon, var_postnummer = var_rad
            var_cursor.execute("INSERT INTO kundeinfo (fornavn, etternavn, epost, telefon, postnummer) VALUES (?, ?, ?, ?, ?)",
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
            var_cursor.execute("INSERT INTO postnummer_tabell (Postnummer, Poststed, Kommunenummer, Kommunenavn, Kategori) VALUES (?, ?, ?, ?, ?)",
                           (var_postnummer, var_poststed, var_kommunenummer, var_kommunenavn, var_kategori))
    conn.commit()

# Funksjon for å koble til databasen
def koble_til_database(database_navn):
    return sqlite3.connect(database_navn)

# Funksjon for å lukke tilkoblingen til databasen
def lukk_tilkobling(conn):
    if conn:
        conn.close()

# Funksjon for å vise kundeinformasjon basert på kundenummer
def vis_kundeinfo(conn, kundenummer):
    var_cursor = conn.cursor()
    var_cursor.execute("""
    SELECT k.*, p.Poststed, p.Kommunenummer, p.Kommunenavn, p.Kategori 
    FROM kundeinfo k
    JOIN postnummer_tabell p ON k.postnummer = p.Postnummer
    WHERE k.kundenummer = ?
    """, (kundenummer,))
    var_kundeinfo = var_cursor.fetchone()
    if var_kundeinfo:
        print(f"Kundenummer: {var_kundeinfo[0]}")
        print(f"Fornavn: {var_kundeinfo[1]}")
        print(f"Etternavn: {var_kundeinfo[2]}")
        print(f"Epost: {var_kundeinfo[3]}")
        print(f"Telefon: {var_kundeinfo[4]}")
        print(f"Postnummer: {var_kundeinfo[5]}")
        print(f"Poststed: {var_kundeinfo[6]}")
        print(f"Kommunenummer: {var_kundeinfo[7]}")
        print(f"Kommunenavn: {var_kundeinfo[8]}")
        print(f"Kategori: {var_kundeinfo[9]}")
    else:
        print("Kundenummer ikke funnet.")

# Main funksjon
def main():
    var_database_navn = "min_database_sql3.db"
    var_kundeinfo_csv_filnavn = "randoms.csv"
    var_postnummer_csv_filnavn = "Postnummerregister.csv"

    # Koble til databasen
    var_conn = koble_til_database(var_database_navn)

    # Opprett tabeller
    opprett_tabeller(var_conn)

    # Legg inn data fra kundeinfo CSV-fil
    legg_til_data_fra_csv_kundeinfo(var_conn, var_kundeinfo_csv_filnavn)

    # Legg inn data fra postnummer CSV-fil
    legg_til_data_fra_csv_postnummer(var_conn, var_postnummer_csv_filnavn)

    # Spør brukeren om kundenummer og vis kundeinformasjon
    kundenummer = input("Vennligst oppgi kundenummer: ")
    vis_kundeinfo(var_conn, kundenummer)

    # Lukk koblingen til databasen
    lukk_tilkobling(var_conn)

if __name__ == "__main__":
    main()
