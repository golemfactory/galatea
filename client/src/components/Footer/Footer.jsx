import golemLogo from '../../assets/logo/golem_logo.svg';
import { StyledFooter } from './styles';

const Footer = () => (
  <StyledFooter>
    Proudly powered by
    <img src={golemLogo} alt="golem logo" />
  </StyledFooter>
);

export default Footer;
