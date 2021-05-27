import { useCallback, useEffect, useState } from 'react';
import { Button, Error, Layout, Loader, Placeholder, Result, Text } from '../components';
import GlobalStyle from '../styles/global';

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
      .then((result) => setResult(result))
      .catch(() => setError(true));

  const handleStorage = useCallback(({ text }) => {
    setText(text);

    handleFetch(text);
  }, []);

  useEffect(() => {
    chrome && chrome.storage && chrome.storage.local.get(['text'], handleStorage);
  }, [chrome, handleStorage]);

  return (
    <>
      <GlobalStyle />
      <Layout>
        {error ? (
          <>
            <Error>
              <Text>{text}</Text>
            </Error>
            <div>
              <Button label="Try again" onClick={() => handleRestart(text)} short />
              <Button label="Cancel" onClick={handleCancel} outlined short />
            </div>
          </>
        ) : text ? (
          result ? (
            <>
              <Result result={result}>
                <Text>{text}</Text>
              </Result>
              <Button label="Close" onClick={handleCancel} />
            </>
          ) : (
            <>
              <Loader>
                <Text>{text}</Text>
              </Loader>
              <Button label="Cancel" onClick={handleCancel} outlined />
            </>
          )
        ) : (
          <>
            <Placeholder />
            <Button label="Close" onClick={handleCancel} />
          </>
        )}
      </Layout>
    </>
  );
};

export default App;
