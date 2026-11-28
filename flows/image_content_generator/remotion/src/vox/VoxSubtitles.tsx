import React from 'react';
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { VoxWord } from './types';

interface Props {
  words: VoxWord[];
}

interface WordGroup {
  words: VoxWord[];
  startSec: number;
  endSec: number;
}

function buildGroups(words: VoxWord[]): WordGroup[] {
  const groups: WordGroup[] = [];
  let i = 0;
  while (i < words.length) {
    const w1 = words[i];
    const w2 = i + 1 < words.length ? words[i + 1] : null;
    if (w2 && w1.text.length <= 5 && w2.text.length <= 8 && w2.startSec - w1.endSec < 0.18) {
      groups.push({ words: [w1, w2], startSec: w1.startSec, endSec: w2.endSec });
      i += 2;
    } else {
      groups.push({ words: [w1], startSec: w1.startSec, endSec: w1.endSec });
      i += 1;
    }
  }
  return groups;
}

export const VoxSubtitles: React.FC<Props> = ({ words }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const nowSec = frame / fps;

  const groups = React.useMemo(() => buildGroups(words), [words]);
  if (!groups.length) return null;

  let activeIdx = -1;
  for (let i = 0; i < groups.length; i++) {
    const g = groups[i];
    const nextStart = i + 1 < groups.length ? groups[i + 1].startSec : g.endSec + 0.45;
    if (nowSec >= g.startSec && nowSec < Math.min(nextStart, g.endSec + 0.35)) {
      activeIdx = i;
      break;
    }
  }
  if (activeIdx === -1) return null;

  const active = groups[activeIdx];
  const localFrame = Math.max(0, Math.round((nowSec - active.startSec) * fps));
  const pop = spring({
    frame: localFrame,
    fps,
    config: { damping: 14, stiffness: 260, mass: 0.45 },
  });
  const scale = activeIdx === 0 && frame < 4 ? 1 : 0.92 + 0.08 * pop;

  return (
    <div
      style={{
        position: 'absolute',
        left: 60,
        right: 60,
        bottom: 290,
        zIndex: 95,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        pointerEvents: 'none',
        transform: `scale(${scale})`,
      }}
    >
      <div
        style={{
          display: 'inline-flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: 14,
          backgroundColor: '#141414',
          border: '4px solid #141414',
          boxShadow: '9px 9px 0px #FFE14D',
          padding: '14px 28px',
          maxWidth: 920,
        }}
      >
        {active.words.map((w, idx) => {
          const isSpoken = nowSec >= w.startSec - 0.02;
          return (
            <span
              key={`${w.text}_${idx}`}
              style={{
                fontFamily: "'VoxSans', 'Montserrat', Arial, sans-serif",
                fontWeight: 900,
                fontSize: 64,
                lineHeight: 1.05,
                letterSpacing: 1,
                textTransform: 'uppercase',
                padding: '2px 10px',
                backgroundColor: isSpoken ? '#FFE14D' : 'transparent',
                color: isSpoken ? '#141414' : '#FFFFFF',
              }}
            >
              {w.text}
            </span>
          );
        })}
      </div>
    </div>
  );
};
