import sqlite3

NAZWA_BAZY = 'tasks.db'

def utworz_baze():
    with sqlite3.connect(NAZWA_BAZY) as polaczenie:
        kursor = polaczenie.cursor()

        kursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tytul TEXT NOT NULL,
            opis TEXT,
            wykonane INTEGER NOT NULL DEFAULT 0,
            utworzono TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')

def dodaj_zadanie(tytul, opis):
    with sqlite3.connect(NAZWA_BAZY) as polaczenie:
        kursor = polaczenie.cursor()

        kursor.execute(
            """
            INSERT INTO tasks (
                tytul,
                opis
            )
            VALUES (?, ?)
            """,
            (tytul, opis)
        )




def pobierz_zadania(wykonane=None,szukaj=None):
    with sqlite3.connect(NAZWA_BAZY) as polaczenie:
        polaczenie.row_factory = sqlite3.Row
        kursor = polaczenie.cursor()


        if wykonane is None and szukaj is None:
            kursor.execute("""
        SELECT
            id,
            tytul,
            opis,
            wykonane,
            utworzono
        From tasks
        ORDER BY id DESC""")

        elif wykonane is not None and szukaj is None:
            kursor.execute("""
            SELECT
            id,
            tytul,
            opis,
            wykonane,
            utworzono
            FROM tasks
            WHERE wykonane = ?
            ORDER BY id DESC""",
            (int(wykonane),))

        elif wykonane is None and szukaj is not None:
            kursor.execute("""
            SELECT 
            id,
            tytul,
            opis,
            wykonane,
            utworzono
            FROM tasks
            WHERE tytul LIKE ?
             ORDER BY id DESC""",
            (f'%{szukaj}%',))

        else:
            kursor.execute("""
                    SELECT 
                    id,
                    tytul,
                    opis,
                    wykonane,
                    utworzono
                    FROM tasks
                    WHERE wykonane = ?
                    AND tytul LIKE ?
                     ORDER BY id DESC""",
            (int(wykonane),f'%{szukaj}%',))

    rekordy = kursor.fetchall()

    zadania = []

    for rekord in rekordy:
        zadanie = dict(rekord)

        zadanie["wykonane"] = bool(zadanie["wykonane"])

        zadania.append(zadanie)

    return zadania

def pobierz_zadanie(zadanie_id):
    with sqlite3.connect(NAZWA_BAZY) as polaczenie:
        polaczenie.row_factory = sqlite3.Row

        kursor = polaczenie.cursor()

        kursor.execute(
            """
            SELECT
                id,
                tytul,
                opis,
                wykonane,
                utworzono
            FROM tasks
            WHERE id = ?
            """,
            (zadanie_id,)
        )

        rekord = kursor.fetchone()

        if rekord is None:
            return None

        zadanie = dict(rekord)
        zadanie["wykonane"] = bool(zadanie["wykonane"])

        return zadanie


def wyczysc_zadania():
    with sqlite3.connect(NAZWA_BAZY) as polaczenie:
        kursor = polaczenie.cursor()

        kursor.execute("""
        DELETE FROM tasks""")


def aktualizuj_zadanie(
        zadanie_id,
        tytul,
        opis,
        wykonane
):
    with sqlite3.connect(NAZWA_BAZY) as polaczenie:
        kursor = polaczenie.cursor()

        kursor.execute("""UPDATE tasks SET 
        tytul = ?, 
        opis = ?,
        wykonane = ?
        WHERE id = ?""",
    (tytul,
        opis,
        int(wykonane),
        zadanie_id
            )
        )

    return kursor.rowcount

def usun_zadanie(zadanie_id):
    with sqlite3.connect(NAZWA_BAZY) as polaczenie:
        kursor = polaczenie.cursor()

        kursor.execute("""
        DELETE FROM tasks
        WHERE id = ?""",
        (zadanie_id,)
        )

    return kursor.rowcount






utworz_baze()

