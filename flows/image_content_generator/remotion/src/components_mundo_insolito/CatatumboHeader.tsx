import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface HeaderProps {
  breadcrumb?: string;
  titlePrimary: string;
  titleHighlight?: string;
  highlightColor?: string;
  stickerText?: string;
  stickerColor?: string;
}

export const CatatumboHeader: React.FC<HeaderProps> = ({
  breadcrumb = 'ENIGMAIQ  //  FENÓMENOS EXTREMOS',
  titlePrimary,
  titleHighlight,
  highlightColor = '#00f5ff',
  stickerText,
  stickerColor = '#ff5722',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 120 },
  });

  const stickerSpring = spring({
    frame: frame - 10,
    fps,
    config: { damping: 10, stiffness: 160 },
  });

  return (
    <div
      style={{
        position: 'absolute',
        top: 70,
        left: 60,
        right: 60,
        zIndex: 50,
      }}
    >
      {/* Top Channel Breadcrumb */}
      <div
        style={{
          fontFamily: 'Consolas, monospace',
          fontSize: 22,
          fontWeight: 700,
          color: 'rgba(0, 245, 255, 0.85)',
          letterSpacing: '0.12em',
          textTransform: 'uppercase',
          marginBottom: 10,
          opacity: Math.min(1, frame / 10),
        }}
      >
        {breadcrumb}
      </div>

      {/* Main Punchy Title */}
      <div
        style={{
          fontFamily: 'Bahnschrift, Arial, sans-serif',
          fontSize: 66,
          fontWeight: 900,
          lineHeight: 1.1,
          color: '#ffffff',
          letterSpacing: '-0.02em',
          textTransform: 'uppercase',
          transform: `translateY(${(1 - titleSpring) * -20}px)`,
          opacity: titleSpring,
          display: 'flex',
          flexWrap: 'wrap',
          alignItems: 'baseline',
          gap: 14,
        }}
      >
        <span>{titlePrimary}</span>
        {titleHighlight && (
          <span style={{ color: highlightColor }}>{titleHighlight}</span>
        )}

        {/* Tilted Neon Hook Sticker */}
        {stickerText && (
          <div
            style={{
              display: 'inline-block',
              transform: `scale(${stickerSpring}) rotate(-4deg)`,
              opacity: stickerSpring,
              backgroundColor: 'rgba(18, 22, 28, 0.95)',
              border: `2.5px solid ${stickerColor}`,
              borderRadius: 8,
              padding: '6px 16px',
              fontFamily: 'Consolas, monospace',
              fontSize: 24,
              fontWeight: 900,
              color: stickerColor,
              letterSpacing: '0.08em',
              boxShadow: `0 0 20px ${stickerColor}40`,
              marginLeft: 10,
            }}
          >
            {stickerText}
          </div>
        )}
      </div>
    </div>
  );
};
