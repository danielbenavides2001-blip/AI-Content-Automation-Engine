import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { DynamicScene } from './types';

export const SceneTechnicalBlueprint: React.FC<{
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

  const rotA = (frame * 1.5) % 360;
  const rotB = (-frame * 1.5) % 360;
  const pulse = Math.sin(frame * 0.1) * 0.2 + 0.8;

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
          {scene.headline || 'MECÁNICA & FUNCIONAMIENTO INTERNO'}
        </div>
        <div style={{ fontSize: 32, fontWeight: 900, color: '#ffffff', marginTop: 4 }}>
          {scene.subheadline || 'ESQUEMA TÉCNICO EN DETALLE'}
        </div>
      </div>

      {/* Blueprint SVG Schematic */}
      <div
        style={{
          position: 'relative',
          width: '100%',
          maxWidth: 720,
          height: 600,
          backgroundColor: 'rgba(2, 9, 22, 0.9)',
          borderRadius: 20,
          border: `2px solid ${primaryColor}70`,
          overflow: 'hidden',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: `0 0 35px ${primaryColor}20`,
        }}
      >
        <svg width="100%" height="100%" viewBox="0 0 720 600">
          {/* Blueprint Grid Lines */}
          <line x1="360" y1="20" x2="360" y2="580" stroke={primaryColor} strokeWidth="1" strokeDasharray="4 4" opacity="0.4" />
          <line x1="20" y1="300" x2="700" y2="300" stroke={primaryColor} strokeWidth="1" strokeDasharray="4 4" opacity="0.4" />

          {/* Central Mechanism Gear A */}
          <g transform={`translate(260, 300) rotate(${rotA})`}>
            <circle cx="0" cy="0" r="110" fill="none" stroke={primaryColor} strokeWidth="3" />
            <circle cx="0" cy="0" r="80" fill="none" stroke={secondaryColor} strokeWidth="1.5" strokeDasharray="8 6" />
            {Array.from({ length: 8 }).map((_, i) => (
              <rect
                key={i}
                x="-12"
                y="-125"
                width="24"
                height="30"
                fill={primaryColor}
                rx="4"
                transform={`rotate(${i * 45})`}
              />
            ))}
            <circle cx="0" cy="0" r="30" fill="#020916" stroke={primaryColor} strokeWidth="2" />
          </g>

          {/* Interlocking Mechanism Gear B */}
          <g transform={`translate(460, 300) rotate(${rotB})`}>
            <circle cx="0" cy="0" r="90" fill="none" stroke={accentColor} strokeWidth="3" />
            <circle cx="0" cy="0" r="65" fill="none" stroke={secondaryColor} strokeWidth="1.5" strokeDasharray="6 4" />
            {Array.from({ length: 6 }).map((_, i) => (
              <rect
                key={i}
                x="-12"
                y="-105"
                width="24"
                height="28"
                fill={accentColor}
                rx="4"
                transform={`rotate(${i * 60})`}
              />
            ))}
            <circle cx="0" cy="0" r="25" fill="#020916" stroke={accentColor} strokeWidth="2" />
          </g>

          {/* Dimension Line & Callouts */}
          <line x1="140" y1="120" x2="380" y2="120" stroke="#ffffff" strokeWidth="1.5" />
          <line x1="140" y1="110" x2="140" y2="130" stroke="#ffffff" strokeWidth="1.5" />
          <line x1="380" y1="110" x2="380" y2="130" stroke="#ffffff" strokeWidth="1.5" />
          <text x="210" y="105" fill="#ffffff" fontSize="15" fontWeight="800">
            TOLERANCIA: 0.02 mm
          </text>
        </svg>

        {/* Dynamic Parameter Card */}
        <div
          style={{
            position: 'absolute',
            bottom: 25,
            left: 25,
            right: 25,
            padding: '14px 20px',
            backgroundColor: 'rgba(2, 9, 20, 0.85)',
            border: `1px solid ${primaryColor}60`,
            borderRadius: 14,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <div>
            <div style={{ color: primaryColor, fontSize: 13, fontWeight: 800 }}>ESTADO DEL MECANISMO</div>
            <div style={{ color: '#ffffff', fontSize: 18, fontWeight: 900 }}>
              {scene.metricLabel || 'SINCRONIZACIÓN CINÉTICA'}: {scene.metricValA || '100% ACTIVA'}
            </div>
          </div>
          <div
            style={{
              padding: '6px 14px',
              backgroundColor: `${accentColor}25`,
              border: `1px solid ${accentColor}`,
              borderRadius: 20,
              color: accentColor,
              fontSize: 14,
              fontWeight: 900,
            }}
          >
            PRECISIÓN OK
          </div>
        </div>
      </div>
    </div>
  );
};
