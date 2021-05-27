import styled from 'styled-components';
import color from '../../styles/colors';

export const StyledError = styled.div`
  width: 100%;

  display: flex;
  flex-direction: column;

  padding: 1rem 2.5rem 2.5rem;

  h2 {
    color: ${color.red};
  }

  img {
    margin: 5rem auto;
  }
`;
