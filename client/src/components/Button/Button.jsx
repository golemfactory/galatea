import { StyledButton } from './styles';

const Button = ({ label, onClick, outlined, short }) => (
  <StyledButton type="button" onClick={onClick} outlined={outlined} short={short}>
    {label}
  </StyledButton>
);

export default Button;
