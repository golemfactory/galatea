import styled from 'styled-components';

export const StyledText = styled.div`
  width: 560px;
  height: 280px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
`;

export const StyledResult = styled.div`
  height: 100px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;

  div {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  div > div {
    display: flex;
    margin-top: 10px;

    &:last-of-type {
      margin-bottom: 20px;
    }

    span {
      margin: 5px;
    }
  }

  span {
    margin-bottom: 15px;
  }
`;
