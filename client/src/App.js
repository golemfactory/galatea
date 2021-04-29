import { useCallback, useEffect, useState } from 'react';
import { StyledForm, StyledResult } from './styles';

const App = () => {
  const url = process.env.REACT_APP_API;

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

  const handleCopy = useCallback((e) => {
    const selection = document.getSelection();

    setText(selection.toString());

    e.preventDefault();
  }, []);

  useEffect(() => {
    document.addEventListener('copy', handleCopy);

    return () => {
      document.removeEventListener('copy', handleCopy);
    };
  }, [handleCopy]);

  return result ? (
    <StyledResult>
      <div>
        <span>Response is:</span>
        {result && result[0].summary_text}
        {result &&
          result[1].summary_list.map(({ label, score }) => (
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
