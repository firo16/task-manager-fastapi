import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [zadania, setZadania] = useState([])
  const [tytul,setTytul] = useState('')
  const [opis, setOpis] = useState('')
  const [filtr,setFiltr] = useState('wszystkie')
  const [szukaj, setSzukaj] = useState('')

  const[ladowanie,setLadowanie] = useState(true)
  const [blad, setBlad] = useState('')




  async function zmienFiltr(nowyFiltr) {
      setFiltr(nowyFiltr)
      await pobierzZadania(nowyFiltr,szukaj)
  }




  async function zmienStatus(zadanie) {
      const odpowiedz = await fetch(
          `http://127.0.0.1:8000/zadania/${zadanie.id}`,
          {
              method:'PATCH',
              headers:{'Content-Type': 'application/json',
              },
          body: JSON.stringify({
              wykonane: !zadanie.wykonane,
              }),
          }
      )
      if (odpowiedz.ok) {
          await pobierzZadania()
      }
  }





  async function usunZadanie(zadanieId) {
  const czyUsunac = window.confirm('czy napewno chcesz usunac zadanie?')

  if (!czyUsunac) {
      return
  }
  const odpowiedz = await fetch(
    `http://127.0.0.1:8000/zadania/${zadanieId}`,
    {
      method: 'DELETE',
    }
  )

  if (odpowiedz.ok) {
    await pobierzZadania()
  }
}





  async function pobierzZadania(
      wybranyFiltr = filtr,
      tekstWyszukiwania = szukaj) {

    setLadowanie(true)
    setBlad('')


    try{
        const parametry = new URLSearchParams()

        if (wybranyFiltr === 'aktywne') {
            parametry.set('wykonane', 'false')
        } else if (wybranyFiltr === 'wykonane') {
            parametry.set('wykonane','true')
        }

        if (tekstWyszukiwania.trim() !== '') {
            parametry.set(
                'szukaj',
                tekstWyszukiwania.trim()
            )
        }

        let adres = 'http://127.0.0.1:8000/zadania'

        const queryString = parametry.toString()

        if (queryString !== '') {
            adres += `?${queryString}`
            }

        const odpowiedz = await fetch(adres)
        const dane = await odpowiedz.json()
        setZadania(dane)
  } catch (error) {
      setBlad('Nie udalo sie pobrac zadan')
      setZadania([])
  } finally {
      setLadowanie(false)
  }
}





  async function dodajZadanie(event) {
      event.preventDefault()

      if (tytul.trim() === '') {
          return
      }

      const odpowiedz = await fetch('http://127.0.0.1:8000/zadania',
          {
          method:'POST',
          headers: {'Content-Type': 'application/json',},
          body: JSON.stringify({
              tytul:tytul,
              opis:opis.trim() === '' ? null : opis,
              }),
          }
      )

      if (odpowiedz.ok) {
          setTytul('')
          setOpis('')

          await pobierzZadania()
      }
  }




  return (
  <main>
    <h1>Menedżer zadań</h1>

    <div className="app-layout">
      <aside className="sidebar">

        <form
          className="add-form"
          onSubmit={dodajZadanie}
        >
          <h2>Nowe zadanie</h2>

          <div>
            <label htmlFor="tytul">Tytuł</label>

            <input
              id="tytul"
              type="text"
              value={tytul}
              onChange={(event) =>
                setTytul(event.target.value)
              }
              placeholder="Wpisz tytuł zadania"
            />
          </div>

          <div>
            <label htmlFor="opis">Opis</label>

            <textarea
              id="opis"
              value={opis}
              onChange={(event) =>
                setOpis(event.target.value)
              }
              placeholder="Opcjonalny opis"
            />
          </div>

          <button type="submit">
            Dodaj zadanie
          </button>
        </form>

        <form
          className="search-form"
          onSubmit={(event) => {
            event.preventDefault()
            pobierzZadania(filtr, szukaj)
          }}
        >
          <h2>Wyszukiwanie</h2>

          <label htmlFor="szukaj">
            Wyszukaj po tytule
          </label>

          <input
            id="szukaj"
            type="search"
            value={szukaj}
            onChange={(event) =>
              setSzukaj(event.target.value)
            }
            placeholder="Wpisz fragment tytułu"
          />

          <div className="search-buttons">
            <button type="submit">
              Szukaj
            </button>

            <button
              type="button"
              className="secondary-button"
              onClick={() => {
                setSzukaj('')
                pobierzZadania(filtr, '')
              }}
            >
              Wyczyść
            </button>
          </div>
        </form>

        <nav className="filters">
          <button
            type="button"
            className={
              filtr === 'wszystkie'
                ? 'aktywny-filtr'
                : ''
            }
            onClick={() =>
              zmienFiltr('wszystkie')
            }
          >
            Wszystkie
          </button>

          <button
            type="button"
            className={
              filtr === 'aktywne'
                ? 'aktywny-filtr'
                : ''
            }
            onClick={() =>
              zmienFiltr('aktywne')
            }
          >
            Do zrobienia
          </button>

          <button
            type="button"
            className={
              filtr === 'wykonane'
                ? 'aktywny-filtr'
                : ''
            }
            onClick={() =>
              zmienFiltr('wykonane')
            }
          >
            Wykonane
          </button>
        </nav>
      </aside>

      <section className="tasks-panel">
        <div className="tasks-header">
          <div>
            <p className="eyebrow">
              Twoja lista
            </p>

            <h2>Zadania</h2>
          </div>

          <span className="task-count">
            {zadania.length}
          </span>
        </div>

        {ladowanie && (
          <p className="komunikat">
            Ładowanie zadań...
          </p>
        )}

        {blad && (
          <p className="komunikat blad">
            {blad}
          </p>
        )}

        {!ladowanie &&
          !blad &&
          zadania.length === 0 && (
            <p className="komunikat">
              Brak pasujących zadań.
            </p>
          )}

        <div className="tasks-list">
          {zadania.map((zadanie) => (
            <article
              key={zadanie.id}
              className={
                zadanie.wykonane
                  ? 'task-card completed'
                  : 'task-card'
              }
            >
              <div className="task-content">
                <h3>{zadanie.tytul}</h3>

                {zadanie.opis && (
                  <p>{zadanie.opis}</p>
                )}

                <span className="task-date">
                  {zadanie.utworzono}
                </span>
              </div>

              <div className="task-actions">
                <label className="status-control">
                  <input
                    type="checkbox"
                    checked={zadanie.wykonane}
                    onChange={() =>
                      zmienStatus(zadanie)
                    }
                  />

                  <span>
                    {zadanie.wykonane
                      ? 'Wykonane'
                      : 'Do zrobienia'}
                  </span>
                </label>

                <button
                  type="button"
                  className="delete-button"
                  onClick={() =>
                    usunZadanie(zadanie.id)
                  }
                >
                  Usuń
                </button>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  </main>
)
}


export default App