import { Heading } from '../index';
import { StyledAbstract, StyledChart, StyledEmotion, StyledEmotions, StyledResult } from './styles';
import { imageSrc } from './utils';
import { PieChart } from 'react-minimal-pie-chart';
import color from '../../styles/colors';

const Result = ({ children, result }) => (
  <StyledResult>
    {children}
    <StyledAbstract>
      <Heading>Abstract</Heading>
      <p>{result.summary.summary_text}</p>
    </StyledAbstract>
    <StyledEmotions>
      <Heading>Emotions</Heading>
      <div>
        {result.emotion
          .sort((prev, next) => (prev.score > next.score ? -1 : 1))
          .map(({ label, score }) => (
            <StyledEmotion key={label}>
              <span>{label}</span>
              <StyledChart>
                <PieChart
                  data={[
                    { value: 100 - Math.floor(score * 100), color: color.grey },
                    { value: Math.floor(score * 100), color: color.charcoal },
                  ]}
                  lineWidth={14}
                  rounded
                  viewBoxSize={[54, 54]}
                  center={[29, 29]}
                  radius={25}
                />
                <img src={imageSrc(label)} alt={label + ' face'} />
              </StyledChart>
              <span>{Math.floor(score * 100)}</span>
            </StyledEmotion>
          ))}
      </div>
    </StyledEmotions>
  </StyledResult>
);

export default Result;
