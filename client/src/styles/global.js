import { createGlobalStyle } from 'styled-components';
import styledNormalize from 'styled-normalize';
import color from './colors';

const GlobalStyle = createGlobalStyle`
  ${styledNormalize};

  * {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
    outline: none;
  }

  html {
    font-size: 10px;
  }
  
  body {
    color: ${color.navy};
    font-family: 'Roboto Mono', monospace;
    font-weight: 500;
    font-size: 0.8rem;
    line-height: 1.1rem;
  }
  
  #galatea-root {
    width: 35.7rem;
    height: 80rem;
  }
`;

export default GlobalStyle;
