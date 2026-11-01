import React from 'react';
import { useCurrentFrame } from 'remotion';
import { DynamicScene } from './types';

export const KineticSubtitles: React.FC<{
  activeScene: DynamicScene;
  primaryColor?: string;
  secondaryColor?: string;
}> = ({
  activeScene,
  primaryColor = '#f59e0b',
  secondaryColor = '#38bdf8'
}) => {
  const frame = useCurrentFrame();

  if (!activeScene || !activeScene.narration) return null;

  const localFrame = frame - activeScene.startFrame;
  const totalFrames = Math.max(1, activeScene.durationFrames);
  const text = activeScene.narration.trim();
  const words = text.split(/\s+/);

  // Calculate current active word index based on time progress
  const progress = Math.min(1, Math.max(0, localFrame / (totalFrames * 0.96)));
  const activeWordIdx = Math.min(words.length - 1, Math.floor(progress * words.length));

  // Chunking exacto al video de referencia: 2 a 3 palabras por pantalla (ritmo rápido y visual)
  const windowSize = 3;
  const chunkIdx = Math.floor(activeWordIdx / windowSize);
  const startIdx = chunkIdx * windowSize;
  const visibleWords = words.slice(startIdx, startIdx + windowSize);

  return (
    <div
      style={{
        position: 'absolute',
        top: 1220,
        left: 50,
        right: 50,
        zIndex: 85,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          fontFamily: "'Montserrat', 'Montserrat Black', sans-serif",
          fontSize: visibleWords.length > 3 ? 82 : 94,
          fontWeight: 900,
          lineHeight: 1.15,
          letterSpacing: '-2px',
          textTransform: 'uppercase',
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          alignItems: 'center',
          maxWidth: 980,
        }}
      >
        {visibleWords.map((word, i) => {
          const actualIdx = startIdx + i;
          const isActive = actualIdx === activeWordIdx;
          return (
            <span
              key={i}
              style={{
                color: isActive ? '#f59e0b' : '#ffffff',
                display: 'inline-block',
                margin: '0 12px',
                WebkitTextStroke: '10px #000000',
                paintOrder: 'stroke fill',
                textShadow: '0 4px 18px rgba(0,0,0,0.85)',
                transform: isActive ? 'scale(1.10)' : 'scale(1)',
                transition: 'transform 0.05s ease',
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
