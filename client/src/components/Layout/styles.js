import styled from 'styled-components';

export const StyledLayout = styled.div`
  width: 100%;
  height: calc(100% - 2rem);

  position: relative;

  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;

  padding-top: 5rem;
  padding-bottom: 4rem;

  > div {
    width: 100%;
  }
`;
