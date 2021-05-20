import styled from 'styled-components';
import color from '../../styles/colors';

export const StyledResult = styled.div`
  > div {
    width: 100%;

    display: flex;
    flex-direction: column;
  }
`;

export const StyledAbstract = styled.div`
  background-color: ${color.ash};

  padding: 1rem 2.5rem 2.5rem;
`;

export const StyledEmotions = styled.div`
  padding: 1rem 2.5rem 2.5rem;

  > div {
    display: flex;
    flex-wrap: wrap;
  }
`;

export const StyledEmotion = styled.div`
  width: 33%;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  span {
    font-family: 'Roboto Mono', monospace;
    font-weight: 400;
    font-size: 1.2rem;
    line-height: 1.6rem;

    margin: 1rem 0;

    &::first-letter {
      text-transform: uppercase;
    }
  }
`;

export const StyledChart = styled.div`
  width: 6rem;
  height: 6rem;

  position: relative;

  svg {
    position: absolute;
  }

  img {
    position: absolute;
    top: -1.5rem;
    left: -1.5rem;

    transform: translate(3rem, 3rem);
  }
`;
