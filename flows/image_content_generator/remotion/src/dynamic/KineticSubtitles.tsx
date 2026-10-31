import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { DynamicScene } from './types';

export const KineticSubtitles: React.FC<{
  activeScene: DynamicScene;
  primaryColor?: string;
  secondaryColor?: string;
}> = ({
  activeScene,
  primaryColor = '#00f5ff',
  secondaryColor = '#38bdf8'
}) => {
  const frame = useCurrentFrame();

  if (!activeScene || !activeScene.narration) return null;

  const localFrame = frame - activeScene.startFrame;
  const totalFrames = Math.max(1, activeScene.durationFrames);
  const text = activeScene.narration.trim();
  const words = text.split(/\s+/);

  // Calculate current active word index based on time progress
  const progress = Math.min(1, Math.max(0, localFrame / (totalFrames * 0.95)));
  const activeWordIdx = Math.min(words.length - 1, Math.floor(progress * words.length));

  // Display sliding window of 6-8 words around the active word
  const windowSize = 7;
  const startIdx = Math.max(0, Math.min(words.length - windowSize, activeWordIdx - 3));
  const visibleWords = words.slice(startIdx, startIdx + windowSize);

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 315, // Reels Bottom Safe Zone
        left: 40,
        right: 40,
        zIndex: 80,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          padding: '16px 28px',
          borderRadius: 20,
          backgroundColor: 'rgba(2, 6, 16, 0.88)',
          border: `1.5px solid ${primaryColor}50`,
          backdropFilter: 'blur(12px)',
          boxShadow: `0 0 30px ${primaryColor}30`,
          maxWidth: 960,
          textAlign: 'center',
          fontFamily: "'Bahnschrift', 'Montserrat', Arial, sans-serif",
          lineHeight: 1.35,
        }}
      >
        <div style={{ fontSize: 30, fontWeight: 900, color: '#ffffff', letterSpacing: 0.5 }}>
          {visibleWords.map((word, i) => {
            const actualIdx = startIdx + i;
            const isActive = actualIdx === activeWordIdx;
            return (
              <span
                key={i}
                style={{
                  color: isActive ? primaryColor : '#ffffff',
                  textShadow: isActive ? `0 0 16px ${primaryColor}` : '0 2px 4px rgba(0,0,0,0.8)',
                  display: 'inline-block',
                  marginRight: 8,
                  transform: isActive ? 'scale(1.12)' : 'scale(1)',
                  transition: 'transform 0.08s ease',
                }}
              >
                {word}
              </span>
            );
          })}
        </div>
      </div>
    </div>
  );
};
