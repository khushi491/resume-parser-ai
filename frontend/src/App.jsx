import { useState } from 'react';
import './App.css';

function App() {
  const [resumeText, setResumeText] = useState('');
  const [parsedData, setParsedData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleParse = async () => {
    setLoading(true);
    setError(null);
    setParsedData(null);

    try {
      const response = await fetch('http://localhost:8000/parse-resume', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ resume_text: resumeText }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setParsedData(data);
    } catch (e) {
      setError('Failed to parse resume. Please ensure the backend is running and accessible at http://localhost:8000. Error: ' + e.message);
      console.error("Error parsing resume:", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Resume Parser AI</h1>
        <p>Paste your resume text below to parse it.</p>
      </header>
      <div className="input-section">
        <textarea
          placeholder="Paste your resume text here..."
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
          rows="20"
          cols="80"
        ></textarea>
        <button onClick={handleParse} disabled={loading}>
          {loading ? 'Parsing...' : 'Parse Resume'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {parsedData && (
        <div className="output-section">
          <h2>Parsed Data</h2>
          <pre>{JSON.stringify(parsedData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
