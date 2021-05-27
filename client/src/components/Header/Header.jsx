import galateaLogo from '../../assets/logo/galatea_logo.svg';
import { StyledHeader } from './styles';

const Header = () => (
  <StyledHeader>
    <img src={galateaLogo} alt="galatea logo" />
  </StyledHeader>
);

export default Header;
