import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { DynamicScene } from './types';

export const SceneGeologicalCrossSection: React.FC<{
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

  const wave = Math.sin(frame * 0.05) * 8;
  const flowProgress = (frame * 3) % 200;

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
        <div style={{ fontSize: 20, letterSpacing: 4, color: accentColor, fontWeight: 800, textTransform: 'uppercase' }}>
          {scene.headline || 'CORTE TRANSVERSAL GEOLÓGICO'}
        </div>
        <div style={{ fontSize: 32, fontWeight: 900, color: '#ffffff', marginTop: 4 }}>
          {scene.subheadline || 'ESTRATOS SUBTERRÁNEOS & MECÁNICA DE PLACAS'}
        </div>
      </div>

      {/* Cross-section Graphic Canvas */}
      <div
        style={{
          position: 'relative',
          width: '100%',
          maxWidth: 900,
          height: 520,
          backgroundColor: '#050b1a',
          borderRadius: 20,
          border: `2px solid ${primaryColor}70`,
          overflow: 'hidden',
          boxShadow: `0 0 35px ${primaryColor}25`,
        }}
      >
        <svg width="100%" height="100%" viewBox="0 0 900 520">
          <defs>
            <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#0a192f" />
              <stop offset="100%" stopColor="#1e3a5f" />
            </linearGradient>
            <linearGradient id="soilGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#2b1810" />
              <stop offset="100%" stopColor="#4a2e1b" />
            </linearGradient>
            <linearGradient id="sedimentGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#1f2937" />
              <stop offset="100%" stopColor="#374151" />
            </linearGradient>
            <linearGradient id="magmaGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#7f1d1d" />
              <stop offset="100%" stopColor="#b91c1c" />
            </linearGradient>
          </defs>

          {/* Layer 1: Surface & Topography */}
          <path
            d={`M 0 120 Q 220 ${100 + wave} 450 130 T 900 ${110 - wave} L 900 200 L 0 200 Z`}
            fill="url(#soilGrad)"
            stroke={primaryColor}
            strokeWidth="2"
          />

          {/* Layer 2: Sedimentary Mud / Aquifer */}
          <path
            d={`M 0 200 L 900 200 L 900 320 Q 600 ${340 + wave} 300 310 L 0 320 Z`}
            fill="url(#sedimentGrad)"
            stroke={secondaryColor}
            strokeWidth="1.5"
            strokeDasharray="6 4"
          />

          {/* Animated Water / Fluid Vectors */}
          <line
            x1={50 + flowProgress * 3}
            y1="260"
            x2={180 + flowProgress * 3}
            y2="260"
            stroke="#00f5ff"
            strokeWidth="3"
            strokeDasharray="8 6"
            opacity="0.8"
          />

          {/* Layer 3: Deep Bedrock & Tectonic Fault */}
          <path
            d="M 0 320 L 900 320 L 900 440 L 0 440 Z"
            fill="#111827"
            stroke="#4b5563"
            strokeWidth="2"
          />

          {/* Layer 4: Deep Thermal Base / Magma Chamber */}
          <path
            d="M 0 440 L 900 440 L 900 520 L 0 520 Z"
            fill="url(#magmaGrad)"
            stroke={accentColor}
            strokeWidth="2.5"
          />

          {/* Depth Scale Ruler */}
          <g transform="translate(30, 40)" opacity="0.85">
            <line x1="0" y1="0" x2="0" y2="440" stroke="#ffffff" strokeWidth="2" />
            <text x="15" y="85" fill="#ffffff" fontSize="14" fontWeight="800">0 m (Superficie)</text>
            <text x="15" y="165" fill={primaryColor} fontSize="14" fontWeight="800">-50 m (Sedimento blando)</text>
            <text x="15" y="285" fill={secondaryColor} fontSize="14" fontWeight="800">-2.000 m (Lecho rocoso)</text>
            <text x="15" y="420" fill={accentColor} fontSize="14" fontWeight="800">-5.000 m (Presión térmica)</text>
          </g>

          {/* Fault Line Arrow */}
          <path
            d="M 520 180 L 580 340 L 620 460"
            fill="none"
            stroke={accentColor}
            strokeWidth="3.5"
            strokeDasharray="10 6"
          />
        </svg>

        {/* Telemetry Badge Callout */}
        <div
          style={{
            position: 'absolute',
            top: 25,
            right: 25,
            padding: '10px 18px',
            backgroundColor: 'rgba(2, 9, 20, 0.85)',
            border: `1px solid ${accentColor}60`,
            borderRadius: 12,
            backdropFilter: 'blur(10px)',
            color: '#ffffff',
            fontSize: 15,
            fontWeight: 800,
          }}
        >
          ANOMALÍA // <span style={{ color: accentColor }}>{scene.metricLabel || 'PRESIÓN ESTRUCTURAL'}: {scene.metricValA || 'CRÍTICA'}</span>
        </div>
      </div>
    </div>
  );
};
