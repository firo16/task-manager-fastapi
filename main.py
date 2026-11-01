from fastapi import FastAPI, HTTPException
from models import CreateZadanie,UpdateZadanie
from database import dodaj_zadanie, pobierz_zadania, pobierz_zadanie,aktualizuj_zadanie,usun_zadanie

app = FastAPI()


@app.get("/")
def home():
    return {"message": 'chyba dziala'}

@app.post('/zadania')
def utworz_zadanie(zadanie: CreateZadanie):
    dodaj_zadanie(zadanie.tytul,zadanie.opis)
    return {
        'tytul': zadanie.tytul,
        'opis': zadanie.opis,
        'wykonane': False
    }

@app.get("/zadania")
def pokaz_zadania(wykonane: bool | None = None,
                  szukaj: str | None = None):

    return pobierz_zadania(wykonane,szukaj)

@app.get("/zadania/{zadanie_id}")
def pokaz_zadanie(zadanie_id: int):
    zadanie = pobierz_zadanie(zadanie_id)

    if zadanie is None:
        raise HTTPException(
            status_code=404,
            detail='zadanie nie istnieje'
        )

    return zadanie

@app.put("/zadania/{zadanie_id}")
def zmien_zadanie(
        zadanie_id: int,
        zadanie: UpdateZadanie
):
    liczba_zmienionych = aktualizuj_zadanie(zadanie_id,zadanie.tytul,zadanie.opis,zadanie.wykonane)

    if liczba_zmienionych == 0:
        raise HTTPException(
            status_code=404,
            detail='zadanie nie istnieje'
        )

    return pobierz_zadanie(zadanie_id)


@app.delete("/zadania/{zadanie_id}")
def delete_zadanie(zadanie_id: int):
    odpowiedz = usun_zadanie(zadanie_id)

    if odpowiedz == 0:
        raise HTTPException(
            status_code=404,
            detail='zadanie nie istnieje'
        )

    return {'message':'zadanie zostalo usuniete'}




