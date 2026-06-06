import { Composition } from 'remotion';
import { Subtitles } from './Subtitles';

const FPS = 30;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Subtitles"
        component={Subtitles}
        durationInFrames={30000}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={{
          words: [
            { text: "EnigmaIQ", start: 0, end: 1000 },
            { text: "Inteligencia", start: 1000, end: 2000 },
            { text: "Financiera", start: 2000, end: 3000 }
          ]
        }}
        calculateMetadata={({ props }) => {
          const words = props.words as { text: string; start: number; end: number }[] | undefined;
          if (words && words.length > 0) {
            const lastWord = words[words.length - 1];
            const durationMs = (lastWord.end || 60000) + 2000;
            const durationFrames = Math.ceil((durationMs / 1000) * FPS);
            return { durationInFrames: Math.max(durationFrames, 150) };
          }
          return { durationInFrames: 30000 };
        }}
      />
    </>
  );
};
