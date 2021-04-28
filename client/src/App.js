import { useCallback, useEffect, useState } from 'react';

const App = () => {
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

    fetch('http://0.0.0.0:5000/api/classify', {
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

  return (
    <>
      {result ? (
        <div className="result">
          <div>
            <span>Response is:</span>
            {result && result[0].summary_text}
            {result &&
              result[1].summary_list.map(({ label, score }) => (
                <div className="list">
                  <span>{label}:</span>
                  <span>{score}</span>
                </div>
              ))}
          </div>
          <button type="button" onClick={handleReset}>
            Reset
          </button>
        </div>
      ) : (
        <form onSubmit={handleFetch}>
          <label htmlFor="text">What do you want to send?</label>
          <textarea
            name="text"
            id="text"
            placeholder="Type something or mark some text below"
            value={text}
            onChange={handleChange}
          />
          <button>Submit</button>
        </form>
      )}
      {!result && (
        <div className="mock">
          <div className="featured-news">
            <div className="section-title">
              <div className="text-block-4">00 /</div>
              <div className="text-block-3">Featured News</div>
            </div>
            <div className="container-3 w-container">
              <div className="section-content">
                <div className="w-layout-grid grid">
                  <div className="news-date">
                    <div className="text-block-2">15.04.2021</div>
                    <div className="news-title">
                      <strong className="bold-text">Golem Beta 1 Patch Release - v0.6.4</strong>
                    </div>
                    <div className="paragraph margin-bottom">
                      We’ve been working on another minor update (v0.6.4) to improve stability and some of the issues
                      that the Golem community has reported.
                    </div>
                  </div>
                  <img
                    src="https://assets-global.website-files.com/60005e3965a10f31d245af87/600706b49f261b3510ad7d78_Golem_arrow_right.svg"
                    loading="lazy"
                    width="150"
                    id="w-node-_2b6c84de-8907-198d-f814-cca626aabfd8-b9e15d58"
                    alt=""
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default App;
