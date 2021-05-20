import { Footer, Header } from '../index';
import { StyledLayout } from './styles';

const Layout = ({ children }) => (
  <StyledLayout>
    <Header />
    {children}
    <Footer />
  </StyledLayout>
);

export default Layout;
