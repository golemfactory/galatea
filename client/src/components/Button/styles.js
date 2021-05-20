import styled, { css } from 'styled-components';
import color from '../../styles/colors';

export const StyledButton = styled.button`
  width: 17.5rem;

  color: ${color.white};
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 1.1rem;
  line-height: 1.4rem;
  text-transform: uppercase;
  letter-spacing: 0.4rem;

  background-color: ${color.petrol};
  border: 0.1rem solid ${color.petrol};

  margin: 0 2rem 2rem;
  padding: 0.7em 0.5rem;

  &:hover {
    opacity: 0.7;
  }

  ${({ outlined }) =>
    outlined &&
    css`
      color: ${color.petrol};

      background-color: ${color.white};
    `}

  ${({ short }) =>
    short &&
    css`
      width: 13rem;
    `}
`;
