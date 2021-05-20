import AngerSVG from '../../assets/emotions/anger.svg';
import FearSVG from '../../assets/emotions/fear.svg';
import JoySVG from '../../assets/emotions/joy.svg';
import LoveSVG from '../../assets/emotions/love.svg';
import SadnessSVG from '../../assets/emotions/sadness.svg';
import SurpriseSVG from '../../assets/emotions/surprise.svg';

export const imageSrc = (label) => {
  switch (label) {
    case 'anger':
      return AngerSVG;
    case 'fear':
      return FearSVG;
    case 'joy':
      return JoySVG;
    case 'love':
      return LoveSVG;
    case 'surprise':
      return SurpriseSVG;
    default:
      return SadnessSVG;
  }
};
