import React from 'react';
import { useCurrentFrame } from 'remotion';

export const WatermarkLogo: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        position: 'absolute',
        top: 65,
        right: 60,
        zIndex: 60,
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        opacity: 0.9,
      }}
    >
      <div
        style={{
          width: 52,
          height: 52,
          borderRadius: '50%',
          border: '2px solid rgba(56, 189, 248, 0.7)',
          overflow: 'hidden',
          backgroundColor: '#020914',
          boxShadow: '0 0 16px rgba(56, 189, 248, 0.4)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <span
          style={{
            color: '#38bdf8',
            fontFamily: "'Bahnschrift', Arial, sans-serif",
            fontSize: 18,
            fontWeight: 900,
            letterSpacing: 1,
          }}
        >
          IQ
        </span>
      </div>
    </div>
  );
};
