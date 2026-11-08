import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [zadania, setZadania] = useState([])
  const [tytul,setTytul] = useState('')
  const [opis, setOpis] = useState('')


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

  async function pobierzZadania() {
    const odpowiedz = await fetch(
      'http://127.0.0.1:8000/zadania'
    )

    const dane = await odpowiedz.json()

    setZadania(dane)
  }

  useEffect(() => {
    pobierzZadania()
  }, [])


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
      <form onSubmit={dodajZadanie}>
          <div>
            <label htmlFor="tytul">Tytuł</label>

            <input
              id="tytul"
              type="text"
              value={tytul}
              onChange={(event) => setTytul(event.target.value)}
              placeholder="Wpisz tytuł zadania"
            />
          </div>

          <div>
            <label htmlFor="opis">Opis</label>

            <textarea
              id="opis"
              value={opis}
              onChange={(event) => setOpis(event.target.value)}
              placeholder="Opcjonalny opis"
            />
          </div>

          <button type="submit">
            Dodaj zadanie
          </button>
        </form>



      {zadania.length === 0 && (
        <p>Brak zadań.</p>
      )}

      <section>
        {zadania.map((zadanie) => (
          <article key={zadanie.id}>
            <h2>{zadanie.tytul}</h2>

            {zadanie.opis && (
              <p>{zadanie.opis}</p>
            )}

            <label>
              <input
                type="checkbox"
                checked={zadanie.wykonane}
                onChange={() => zmienStatus(zadanie)}
              />

              {zadanie.wykonane
                ? 'Wykonane'
                : 'Do zrobienia'}
            </label>
            <button
              type="button"
              onClick={() => usunZadanie(zadanie.id)}
            >
              Usuń
            </button>
          </article>
        ))}
      </section>
    </main>
  )
}

export default App