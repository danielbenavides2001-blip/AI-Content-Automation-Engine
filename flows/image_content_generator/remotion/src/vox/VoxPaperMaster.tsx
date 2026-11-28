import React from 'react';
import { Sequence, useCurrentFrame } from 'remotion';
import { VoxBlueprint } from './types';
import { VoxPaperBackground } from './VoxPaperBackground';
import { VoxSceneView } from './VoxScenes';
import { VoxSubtitles } from './VoxSubtitles';

export const DEFAULT_VOX_BLUEPRINT: VoxBlueprint = {
  episodeId: 'VOX_DEMO',
  title: 'Demo Vox Paper Collage',
  pillarLabel: 'INGENIERÍA',
  issueNumber: 'ED. 01',
  fps: 30,
  totalFrames: 180,
  beats: [
    {
      id: 'b1',
      kind: 'paper_highlight',
      startFrame: 0,
      durationFrames: 180,
      kicker: 'DEMO',
      headline: 'Así se construyen gráficos editoriales en automático.',
      highlightPhrase: 'gráficos editoriales',
    },
  ],
  words: [
    { text: 'ASÍ', startSec: 0, endSec: 0.4 },
    { text: 'FUNCIONA', startSec: 0.4, endSec: 1.1 },
  ],
};

export const VoxPaperMaster: React.FC<VoxBlueprint> = (props) => {
  const frame = useCurrentFrame();
  const data = props?.beats?.length ? props : DEFAULT_VOX_BLUEPRINT;
  const activeBeatIdx = Math.max(
    0,
    data.beats.findIndex((b) => frame >= b.startFrame && frame < b.startFrame + b.durationFrames)
  );
  const currentBeat = data.beats[activeBeatIdx] || data.beats[data.beats.length - 1];

  return (
    <div
      style={{
        width: 1080,
        height: 1920,
        position: 'relative',
        overflow: 'hidden',
        backgroundColor: '#F4EFE6',
      }}
    >
      <VoxPaperBackground pillarLabel={data.pillarLabel} issueNumber={data.issueNumber} />

      {data.beats.map((beat, idx) => (
        <Sequence
          key={beat.id}
          from={beat.startFrame}
          durationInFrames={Math.max(1, beat.durationFrames)}
        >
          <VoxSceneView beat={beat} isFirstScene={idx === 0} />
        </Sequence>
      ))}

      {/* Subtle beat progress indicator strip at very bottom above IG/FB UI */}
      <div
        style={{
          position: 'absolute',
          left: 58,
          right: 58,
          bottom: 228,
          height: 10,
          backgroundColor: 'rgba(20,20,20,0.14)',
          border: '2px solid #141414',
          zIndex: 90,
          display: 'flex',
        }}
      >
        <div
          style={{
            width: `${((frame + 1) / Math.max(1, data.totalFrames)) * 100}%`,
            height: '100%',
            backgroundColor: currentBeat.kind === 'data_bars' ? '#1D4ED8' : '#E63946',
          }}
        />
      </div>

      <VoxSubtitles words={data.words} />
    </div>
  );
};
