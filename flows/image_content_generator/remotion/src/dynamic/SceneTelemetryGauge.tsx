import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { DynamicScene } from './types';

export const SceneTelemetryGauge: React.FC<{
  scene: DynamicScene;
  primaryColor?: string;
  secondaryColor?: string;
  accentColor?: string;
}> = ({
  scene,
  primaryColor = '#00f5ff',
  secondaryColor = '#38bdf8',
  accentColor = '#f59e0b'
}) => {
  const frame = useCurrentFrame();

  const progress = interpolate(frame, [0, 60], [0, 85], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const angle = (progress / 100) * 260 - 130;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '120px 40px 320px 40px',
        boxSizing: 'border-box',
        fontFamily: "'Bahnschrift', 'Montserrat', Arial, sans-serif",
      }}
    >
      {/* Top Headline */}
      <div style={{ textAlign: 'center', marginBottom: 25 }}>
        <div style={{ fontSize: 20, letterSpacing: 4, color: primaryColor, fontWeight: 800, textTransform: 'uppercase' }}>
          {scene.headline || 'DATOS & TELEMETRÍA CIENTÍFICA'}
        </div>
        <div style={{ fontSize: 32, fontWeight: 900, color: '#ffffff', marginTop: 4 }}>
          {scene.subheadline || 'ANÁLISIS DE MAGNITUDES FÍSICAS'}
        </div>
      </div>

      {/* Main Circular Dial */}
      <div
        style={{
          position: 'relative',
          width: 500,
          height: 500,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <svg width="500" height="500" viewBox="0 0 500 500">
          {/* Dial Background Ring */}
          <circle
            cx="250"
            cy="250"
            r="190"
            fill="none"
            stroke="rgba(255,255,255,0.08)"
            strokeWidth="20"
          />

          {/* Active Radial Progress Arc */}
          <circle
            cx="250"
            cy="250"
            r="190"
            fill="none"
            stroke={primaryColor}
            strokeWidth="20"
            strokeDasharray="1194"
            strokeDashoffset={1194 * (1 - progress / 100)}
            strokeLinecap="round"
            transform="rotate(-90 250 250)"
            style={{
              filter: `drop-shadow(0 0 16px ${primaryColor})`,
            }}
          />

          {/* Needle Indicator */}
          <g transform={`rotate(${angle} 250 250)`}>
            <line x1="250" y1="250" x2="250" y2="80" stroke={accentColor} strokeWidth="4" strokeLinecap="round" />
            <circle cx="250" cy="250" r="16" fill="#020914" stroke={accentColor} strokeWidth="4" />
          </g>
        </svg>

        {/* Center Digital Metric Value */}
        <div
          style={{
            position: 'absolute',
            textAlign: 'center',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 2,
          }}
        >
          <div style={{ fontSize: 58, fontWeight: 900, color: '#ffffff' }}>
            {scene.metricValA || `${Math.round(progress)}%`}
          </div>
          <div style={{ fontSize: 16, fontWeight: 800, color: primaryColor, letterSpacing: 2, textTransform: 'uppercase' }}>
            {scene.metricLabel || 'MAGNITUD REGISTRADA'}
          </div>
          {scene.metricUnit && (
            <div style={{ fontSize: 14, fontWeight: 700, color: '#9ca3af' }}>
              UNIDAD: {scene.metricUnit}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
