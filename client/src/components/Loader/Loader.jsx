import { Heading } from '../index';
import { StyledLoader, StyledSpinner } from './styles';

const Loader = ({ children }) => (
  <div>
    {children}
    <StyledLoader>
      <Heading>Please wait...</Heading>
      It shouldn’t take more than 10 seconds
      <StyledSpinner />
    </StyledLoader>
  </div>
);

export default Loader;
