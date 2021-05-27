import { Heading } from '../index';
import { StyledError } from './styles';
import { imageSrc } from '../Result/utils';

const Error = ({ children }) => (
  <div>
    {children}
    <StyledError>
      <Heading>Some error occured...</Heading>
      <p>and we are unable to analyze your text at this moment</p>
      <img src={imageSrc()} alt="sad face" />
    </StyledError>
  </div>
);

export default Error;
