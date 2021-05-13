import { useCallback, useEffect, useState } from 'react';
import { StyledText, StyledResult } from './styles';

const App = () => {
  const url = 'http://0.0.0.0:5000';
  const chrome = window.chrome;

  const [text, setText] = useState('');

  const [result, setResult] = useState(undefined);

  const [error, setError] = useState(false);

  const handleCancel = () => {
    chrome && chrome.storage && chrome.storage.local.set({ text: '' });
    window.close();
  };

  const handleClose = () => {
    setResult(undefined);
    handleCancel();
  };

  const handleRestart = (text) => {
    setError(false);

    handleFetch(text);
  };

  const handleFetch = (text) =>
    fetch(`${url}/api/classify`, {
      method: 'post',
      body: new URLSearchParams(`text=${text}`),
    })
      .then((response) => response.json())
      .then(({ results }) => setTimeout(() => setResult(results), 2000))
      .catch(() => setError(true));

  const handleStorage = useCallback(({ text }) => {
    setText(text);

    handleFetch(text);
  }, []);

  useEffect(() => {
    chrome && chrome.storage && chrome.storage.local.get(['text'], handleStorage);
  }, [chrome, handleStorage]);

  return error ? (
    <div>
      <h2>Some error occured...</h2>
      <p>and we are unable to analyze your text at this moment</p>
      <div>
        <button type="button" onClick={() => handleRestart(text)}>
          Try again
        </button>
        <button type="button" onClick={handleCancel}>
          Cancel
        </button>
      </div>
    </div>
  ) : text ? (
    result ? (
      <StyledResult>
        <div>
          <span>Abstract</span>
          {result && result[0].summary_text}
          <span>Emotions</span>
          {result &&
            result[1].summary_list.map(({ label, score }) => (
              <div>
                <span>{label}:</span>
                <span>{score}</span>
              </div>
            ))}
        </div>
        <button type="button" onClick={handleClose}>
          Close
        </button>
      </StyledResult>
    ) : (
      <StyledText>
        {text}
        <button type="button" onClick={handleCancel}>
          Cancel
        </button>
      </StyledText>
    )
  ) : (
    <div>
      <h2>Please select some text...</h2>
      <p>So we can analyze it</p>
      <button type="button" onClick={handleClose}>
        Close
      </button>
    </div>
  );
};

export default App;
