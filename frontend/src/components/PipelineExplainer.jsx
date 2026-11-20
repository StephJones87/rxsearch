
import './PipelineExplainer.css'

function PipelineExplainer({ results }) {
  if (!results) return null

  const prescription = results.prescriptions[0]
  const medication = prescription?.medications?.[0]

  return (
    <section className="explainer">
      <h2>How RxSearch works</h2>
      <p>
        Follow a prescription from unstructured text to
        searchable clinical data.
      </p>

      <div className="explainer-label">
        PART 1 — BEFORE YOU SEARCH
      </div>

      <div className="explainer-steps">
        <div className="explainer-step">
          <span className="step-number">1</span>
          <h3>Original prescription</h3>
          <p>{prescription?.prescription_text}</p>
          <small>Unstructured text generated for this demo.</small>
        </div>

        <div className="explainer-step">
          <span className="step-number">2</span>
          <h3>spaCy extraction</h3>
          <p>
            Recognised medication:
            <strong> {medication?.text || 'None'}</strong>
          </p>
          <small>
            A rule-based EntityRuler identifies medication mentions.
          </small>
        </div>

        <div className="explainer-step">
          <span className="step-number">3</span>
          <h3>Normalisation</h3>
          <p>
            {medication?.text || 'Unknown'}
            {' → '}
            <strong>{medication?.ingredient || 'Unknown'}</strong>
          </p>
          <small>
            Brand and generic names map to a common ingredient.
          </small>
        </div>

        <div className="explainer-step">
          <span className="step-number">4</span>
          <h3>Elasticsearch indexing</h3>
          <p>Enriched document stored in Elasticsearch.</p>
          <small>
            This processing happened before the search.
          </small>
        </div>
      </div>

      <div className="explainer-label">
        PART 2 — WHEN YOU CLICK SEARCH
      </div>

      <div className="explainer-steps">
        <div className="explainer-step">
          <span className="step-number">5</span>
          <h3>Your search</h3>
          <p><strong>{results.query}</strong></p>
        </div>

        <div className="explainer-step">
          <span className="step-number">6</span>
          <h3>Query normalisation</h3>
          <p>
            {results.query}
            {' → '}
            <strong>{results.normalised_ingredient}</strong>
          </p>
        </div>

        <div className="explainer-step">
          <span className="step-number">7</span>
          <h3>Elasticsearch retrieval</h3>
          <p>
            <strong>{results.enriched_matches}</strong> concept matches
          </p>
          <small>
            Compared with {results.raw_matches} raw text matches.
          </small>
        </div>
      </div>
    </section>
  )
}

export default PipelineExplainer
