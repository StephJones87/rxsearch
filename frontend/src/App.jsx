import { useState } from 'react'
import './App.css'
import PipelineExplainer from './components/PipelineExplainer'

function App() {
  const [medication, setMedication] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSearch(event) {
    event.preventDefault()

    if (!medication.trim()) return

    setLoading(true)
    setError('')
    setResults(null)

    try {
      const response = await fetch(
        `http://127.0.0.1:8001/search?medication=${encodeURIComponent(medication.trim())}`
      )

      if (!response.ok) {
        throw new Error(`Search failed (${response.status})`)
      }

      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>RxSearch</h1>
        <p>Explore how NLP makes clinical prescriptions searchable.</p>
      </header>

      <main>
        <section>
          <h2>Search prescriptions</h2>
          <p>Enter a medication brand or generic ingredient.</p>

          <form onSubmit={handleSearch}>
            <input
              type="text"
              placeholder="e.g. Stelara or ustekinumab"
              value={medication}
              onChange={(e) => setMedication(e.target.value)}
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>

          {error && <p role="alert">Error: {error}</p>}
        </section>

        {results && (
          <>
            <PipelineExplainer results={results} />
            
            <section>
              <h2>How your search worked</h2>

              <div className="pipeline">
                <div>
                  <strong>1. Your query</strong>
                  <p>{results.query}</p>
                </div>
                <div>→</div>
                <div>
                  <strong>2. Normalised ingredient</strong>
                  <p>{results.normalised_ingredient}</p>
                </div>
                <div>→</div>
                <div>
                  <strong>3. Elasticsearch</strong>
                  <p>{results.enriched_matches} matches</p>
                </div>
              </div>
            </section>

            <section>
              <h2>Compare search methods</h2>

              <p>Raw text matches: <strong>{results.raw_matches}</strong></p>
              <p>Enriched matches: <strong>{results.enriched_matches}</strong></p>

              <p>
                Raw search looks for the entered words. Enriched search
                retrieves prescriptions using their normalised ingredient.
              </p>
            </section>

            <section>
              <h2>Matching prescriptions</h2>

              <p>
                Showing {results.prescriptions.length} of{' '}
                {results.enriched_matches} matches.
              </p>

              {results.prescriptions.map((prescription) => (
                <div key={prescription.prescription_id} className="prescription">
                  <strong>{prescription.prescription_id}</strong>
                  <p>{prescription.prescription_text}</p>

                  <small>
                    Extracted medication:{' '}
                    {prescription.medications
                      .map((med) => `${med.text} → ${med.ingredient}`)
                      .join(', ')}
                  </small>
                </div>
              ))}
            </section>
          </>
        )}
      </main>
    </div>
  )
}

export default App