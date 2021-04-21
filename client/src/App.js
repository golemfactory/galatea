import { useState } from 'react';

const App = () => {
  const [text, setText] = useState('');

  const handleChange = (e) => {
    e.preventDefault();

    setText(e.currentTarget.value);
  };

  const [result, setResult] = useState(undefined);

  const handleReset = () => setResult(undefined);

  const handleFetch = (e) => {
    e.preventDefault();

    fetch('http://0.0.0.0:5000/api/classify', {
      method: 'post',
      body: new URLSearchParams(`text=${text}`),
    })
      .then((response) => response.json())
      .then(({ results }) => setResult(results))
      .catch((error) => console.log(error));
  };

  return result ? (
    <div className="result">
      <div>
        <span>Response is:</span>
        {result.map((result) => result.summary_text)}
      </div>
      <button type="button" onClick={handleReset}>
        Reset
      </button>
    </div>
  ) : (
    <form onSubmit={handleFetch}>
      <label htmlFor="text">What do you want to send?</label>
      <div>
        <input name="text" id="text" placeholder="Type something" value={text} onChange={handleChange} />
        <button>Submit</button>
      </div>
    </form>
  );
};

export default App;
