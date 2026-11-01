from pathlib import Path
import pytest
from fastapi.testclient import TestClient
import database
import main

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def przygotuj_baze(tmp_path, monkeypatch):
    testowa_baza = tmp_path / 'test_task.db'

    monkeypatch.setattr(
        database,
        "NAZWA_BAZY" ,
        str(testowa_baza)
        )

    database.utworz_baze()

    yield



def test_utworzenie_zadania():
    odpowiedz = client.post("/zadania",
    json={
        "tytul":"nauczyc sie testow",
        "opis":"przetestowac POST"})


    assert odpowiedz.status_code == 200
    assert odpowiedz.json()["tytul"] == "nauczyc sie testow"
    assert odpowiedz.json()["opis"] == "przetestowac POST"
    assert odpowiedz.json()["wykonane"] is False

    lista = client.get('/zadania')

    assert lista.status_code == 200
    assert len(lista.json()) == 1
    assert lista.json()[0]["tytul"] == "nauczyc sie testow"


def test_pobranie_jednego_zadania():
    client.post("/zadania",
                json={
                    "tytul":"zadanie testowe",
                    "opsi": None
                }
            )

    lista = client.get('/zadania').json()
    zadanie_id = lista[0]["id"]

    odpowiedz = client.get(f'/zadania/{zadanie_id}')

    assert odpowiedz.status_code == 200
    assert odpowiedz.json()["tytul"] == "zadanie testowe"

def test_nieistniejace_zadanie():
    odpowiedz = client.get("/zadania/999999999999")


    assert odpowiedz.status_code == 404
    assert odpowiedz.json() == {"detail":"zadanie nie istnieje"}



def test_aktualizacja_zadania():
    client.post("/zadania",
                json={
                    "tytul":"nauczyc sie SQLA",
                    "opsi": "powtorzyc SELECT"
                }
            )

    zadania = client.get("/zadania").json()
    zadanie_id = zadania[0]["id"]

    odpowiedz = client.put(f"/zadania/{zadanie_id}",
                           json={
                               "tytul":"nauczyc sie SQLA",
                               "opis":"powtorzyc SELECT i napisac pierwszy program",
                               "wykonane": True
                                }
                            )

    assert odpowiedz.status_code == 200
    assert odpowiedz.json()["tytul"] == 'nauczyc sie SQLA'
    assert odpowiedz.json()["wykonane"] is True

    zapisane_zadanie = client.get(f"/zadania/{zadanie_id}").json()

    assert zapisane_zadanie["opis"] == "powtorzyc SELECT i napisac pierwszy program"
    assert zapisane_zadanie["wykonane"] is True


def test_aktualizacji_nieistniejacego_zadania():
    odpowiedz = client.put("/zadania/9999999",
                json={
                    "tytul": "nieistniejace zadanie",
                    "opis": None,
                    "wykonane": True
                })

    assert odpowiedz.status_code == 404
    assert odpowiedz.json() == {
        "detail": "zadanie nie istnieje"
    }


def test_usuniecie_zadania():
    client.post("/zadania",
                json={
                    "tytul":"zadanie do usuniecia",
                    "opsi": None,
                    "wykonane": True
                })

    zadanie = client.get("/zadania").json()
    zadanie_id = zadanie[0]["id"]

    odpowiedz = client.delete(f"/zadania/{zadanie_id}")

    assert odpowiedz.status_code == 200
    assert odpowiedz.json() == {"message":'zadanie zostalo usuniete'}

    odpowiedz_po_usunieciu = client.get(f"/zadania/{zadanie_id}")

    assert odpowiedz_po_usunieciu.status_code == 404


def test_nieistniejacego_zadania():
    odpowiedz = client.delete("/zadania/99999999")

    assert odpowiedz.status_code == 404
    assert odpowiedz.json() == {"detail":"zadanie nie istnieje"}



def test_pusty_tytul():
    odpowiedz = client.post("/zadania",
                            json={
                                "tytul":"",
                                "opis":"pusty tytul",
                                "wykonane": True
                            })

    assert odpowiedz.status_code == 422
    assert len(client.get("/zadania").json()) == 0


def test_wedlug_filtrowania_wykonane():
    client.post("/zadania",
                json={
                    "tytul":"nauczyc sie testow",
                    "opis":None
                })

    client.post("/zadania",
                json={
                    "tytul":"znalesc prace w security",
                    "opis":None
                })

    zadania = client.get("/zadania").json()

    zadanie_do_ukonczenia = next(
        zadanie
        for zadanie in zadania
        if zadanie["tytul"] == "nauczyc sie testow"
    )

    client.put(f"zadania/{zadanie_do_ukonczenia["id"]}",
               json={
                   "tytul":"nauczyc sie testow",
                   "opis":None,
                   "wykonane": True
               })

    wykonane = client.get("/zadania?wykonane=true")

    assert wykonane.status_code == 200
    assert len(wykonane.json()) == 1
    assert wykonane.json()[0]["tytul"] == "nauczyc sie testow"
    assert wykonane.json()[0]["wykonane"] is True



def test_wyszukiwanie_po_tytule():
    client.post("/zadania",
                json={
                    "tytul": "Nauczyc sie SQL",
                    "opis": None
                })

    client.post("/zadania",
                json={
                    "tytul": "Poznac React",
                    "opis": None
                })

    client.post("/zadania",
                json={
                    "tytul":"Zrobic projekt SQL",
                    "opis": None
                })

    odpowiedz = client.get(
        "/zadania?szukaj=sql"
    )

    assert odpowiedz.status_code == 200
    assert len(odpowiedz.json()) == 2

    zadania = [
        zadanie["tytul"]
        for zadanie in odpowiedz.json()
    ]

    assert "Nauczyc sie SQL" in zadania
    assert "Poznac React" not in zadania
    assert "Zrobic projekt SQL" in zadania


