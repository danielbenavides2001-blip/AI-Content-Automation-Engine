import React from 'react';
import { staticFile, useCurrentFrame } from 'remotion';

interface Props {
  pillarLabel: string;
  issueNumber: string;
}

export const VoxPaperBackground: React.FC<Props> = ({ pillarLabel, issueNumber }) => {
  const frame = useCurrentFrame();
  // Subtle organic paper drift so background always stays alive
  const gridShiftX = (frame * 0.22) % 48;
  const gridShiftY = (frame * 0.14) % 48;
  const fontUrl = staticFile('fonts/Montserrat-Bold.ttf');

  return (
    <>
      <style>{`
        @font-face {
          font-family: 'VoxSans';
          src: url('${fontUrl}') format('truetype');
          font-weight: 400 900;
          font-style: normal;
        }
      `}</style>

      {/* Cream editorial paper base (#F4EFE6) */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundColor: '#F4EFE6',
          backgroundImage: `
            radial-gradient(circle at 18% 12%, rgba(255, 225, 77, 0.16) 0%, transparent 45%),
            radial-gradient(circle at 82% 85%, rgba(230, 57, 70, 0.08) 0%, transparent 45%),
            linear-gradient(to right, rgba(25, 25, 25, 0.055) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(25, 25, 25, 0.055) 1px, transparent 1px)
          `,
          backgroundSize: '100% 100%, 100% 100%, 48px 48px, 48px 48px',
          backgroundPosition: `0 0, 0 0, ${gridShiftX}px ${gridShiftY}px, ${gridShiftX}px ${gridShiftY}px`,
        }}
      />

      {/* Printed halftone corner texture */}
      <svg
        width={1080}
        height={1920}
        style={{ position: 'absolute', inset: 0, pointerEvents: 'none', opacity: 0.14 }}
      >
        <defs>
          <pattern id="voxHalftone" width="14" height="14" patternUnits="userSpaceOnUse">
            <circle cx="3.5" cy="3.5" r="1.4" fill="#181818" />
          </pattern>
        </defs>
        <rect x="0" y="0" width="320" height="240" fill="url(#voxHalftone)" opacity="0.45" />
        <rect x="760" y="1640" width="320" height="280" fill="url(#voxHalftone)" opacity="0.45" />
      </svg>

      {/* Soft paper border vignette */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          boxShadow: 'inset 0 0 110px rgba(72, 54, 30, 0.14)',
          pointerEvents: 'none',
        }}
      />

      {/* Editorial Top Bar (Reels Top Safe Zone) */}
      <div
        style={{
          position: 'absolute',
          top: 56,
          left: 54,
          right: 54,
          zIndex: 80,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderBottom: '3px solid #141414',
          paddingBottom: 14,
          fontFamily: "'VoxSans', 'Montserrat', Arial, sans-serif",
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div
            style={{
              backgroundColor: '#141414',
              color: '#F4EFE6',
              padding: '7px 16px',
              fontSize: 20,
              fontWeight: 900,
              letterSpacing: 1.4,
            }}
          >
            CURIOSIDADES DEL MUNDO
          </div>
          <div
            style={{
              backgroundColor: '#FFE14D',
              color: '#141414',
              border: '2.5px solid #141414',
              padding: '5px 12px',
              fontSize: 18,
              fontWeight: 900,
              letterSpacing: 0.8,
            }}
          >
            {pillarLabel.toUpperCase()}
          </div>
        </div>
        <div
          style={{
            fontFamily: "'Courier New', monospace",
            fontSize: 19,
            fontWeight: 700,
            color: '#141414',
            opacity: 0.8,
          }}
        >
          {issueNumber}
        </div>
      </div>
    </>
  );
};
