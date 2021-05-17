import { useCallback, useEffect, useState } from 'react';
import { StyledForm, StyledResult } from './styles';

const App = () => {
  const url = 'http://0.0.0.0:5000';
  const chrome = window.chrome;

  const [text, setText] = useState('');

  const handleChange = (e) => {
    e.preventDefault();

    setText(e.currentTarget.value);
  };

  const [result, setResult] = useState(undefined);

  const handleReset = () => {
    setText('');
    setResult(undefined);
  };

  const handleFetch = (e) => {
    e.preventDefault();

    fetch(`${url}/api/classify`, {
      method: 'post',
      body: new URLSearchParams(`text=${text}`),
    })
      .then((response) => response.json())
      .then(({ results }) => setResult(results))
      .catch((error) => console.log(error));
  };

  const handleMessage = useCallback((message) => setText(message), []);

  useEffect(() => {
    if (chrome && chrome.runtime) {
      chrome.runtime.onMessage.addListener(handleMessage);

      return () => {
        chrome.runtime.onMessage.removeListener(handleMessage);
      };
    }
  }, [chrome, handleMessage]);

  return result ? (
    <StyledResult>
      <div>
        <span>Response is:</span>
        {result && result.summary.summary_text}
        {result &&
          result.emotion.map(({ label, score }) => (
            <div>
              <span>{label}:</span>
              <span>{score}</span>
            </div>
          ))}
      </div>
      <button type="button" onClick={handleReset}>
        Reset
      </button>
    </StyledResult>
  ) : (
    <StyledForm onSubmit={handleFetch}>
      <label htmlFor="text">What do you want to send?</label>
      <textarea
        name="text"
        id="text"
        placeholder="Type something or mark some text below"
        value={text}
        onChange={handleChange}
      />
      <button>Submit</button>
    </StyledForm>
  );
};

export default App;
