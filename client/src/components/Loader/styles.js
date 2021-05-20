import styled from 'styled-components';
import SpinnerSVG from './spinner.svg';

export const StyledLoader = styled.div`
  width: 100%;

  display: flex;
  flex-direction: column;

  padding: 1rem 2.5rem 2.5rem;
`;

export const StyledSpinner = styled.div`
  width: 5rem;
  height: 5rem;

  background-image: url(${SpinnerSVG});
  background-position: center;
  background-repeat: no-repeat;
  background-size: 3rem;

  transform: rotateY(180deg);

  margin: 3rem auto;
`;
