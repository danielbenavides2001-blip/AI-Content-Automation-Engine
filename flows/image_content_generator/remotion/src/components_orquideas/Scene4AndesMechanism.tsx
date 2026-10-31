import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderOrquideas } from './HeaderOrquideas';

export const Scene4AndesMechanism: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const mountainSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 90 },
  });

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: 10,
      }}
    >
      <HeaderOrquideas
        category="¿POR QUÉ"
        categoryHighlight="AHÍ?"
        bigMetric="15%"
        metricSubtitle="de las plantas del planeta en el 1% de tierra"
        badgeText="EFECTO ANDES"
        badgeColor="#00f5ff"
      />

      {/* Main Framed Stage */}
      <div
        style={{
          position: 'absolute',
          top: 320,
          left: 60,
          right: 60,
          height: 1050,
          border: '1.5px solid rgba(255, 255, 255, 0.15)',
          backgroundColor: 'rgba(11, 14, 20, 0.9)',
          backdropFilter: 'blur(10px)',
          borderRadius: 16,
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '30px',
          zIndex: 15,
        }}
      >
        <div style={{ alignSelf: 'flex-start', color: '#00f5ff', fontFamily: 'monospace', fontSize: 16 }}>
          EVOLUCIÓN EN CORDILLERA · ÚLTIMOS 20 MILLONES DE AÑOS
        </div>

        {/* Mountain Range Illustration & Seed wind */}
        <div style={{ width: '100%', height: 600, position: 'relative' }}>
          <svg width="100%" height="100%" viewBox="0 0 900 600">
            <defs>
              <linearGradient id="andesGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="#475569" />
                <stop offset="50%" stopColor="#1e293b" />
                <stop offset="100%" stopColor="#0f172a" />
              </linearGradient>
              <linearGradient id="amazonGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#15803d" />
                <stop offset="100%" stopColor="#166534" />
              </linearGradient>
            </defs>

            {/* Andes peaks rising */}
            <g transform={`scale(1, ${mountainSpring})`} style={{ transformOrigin: 'bottom center' }}>
              <path
                d="M 50 560 L 250 200 L 380 340 L 520 120 L 680 380 L 850 560 Z"
                fill="url(#andesGrad)"
                stroke="#00f5ff"
                strokeWidth="2"
              />
              {/* Snow caps */}
              <polygon points="520,120 480,180 560,180" fill="#ffffff" opacity="0.9" />
              <polygon points="250,200 220,250 280,250" fill="#ffffff" opacity="0.8" />
            </g>

            {/* Amazonian forest baseline */}
            <rect x="50" y="550" width="800" height="40" fill="url(#amazonGrad)" rx="6" />
            <text x="70" y="575" fill="#4ade80" fontFamily="monospace" fontSize="18" fontWeight="bold">
              ANCESTROS AMAZÓNICOS
            </text>

            {/* Microscopic seed dust wind */}
            {[...Array(40)].map((_, i) => {
              const xPos = 120 + ((i * 19 + frame * 3.5) % 680);
              const yPos = 150 + ((i * 27) % 360) + Math.sin((frame + i * 10) * 0.08) * 20;
              return (
                <circle
                  key={i}
                  cx={xPos}
                  cy={yPos}
                  r={2.5}
                  fill={i % 2 === 0 ? '#facc15' : '#e879f9'}
                  opacity={0.8}
                />
              );
            })}

            {/* Wind flow curve */}
            <path
              d="M 100 480 Q 400 350 780 200"
              fill="none"
              stroke="rgba(0, 245, 255, 0.4)"
              strokeWidth="2"
              strokeDasharray="8 6"
            />
          </svg>

          {/* Micro seed info pill */}
          <div
            style={{
              position: 'absolute',
              top: 50,
              right: 30,
              backgroundColor: 'rgba(20, 26, 36, 0.95)',
              border: '1.5px solid #d946ef',
              borderRadius: 12,
              padding: '16px 24px',
              maxWidth: 380,
            }}
          >
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 24, fontWeight: 900, color: '#d946ef' }}>
              SEMILLAS TIPO POLVO
            </div>
            <div style={{ fontFamily: 'Consolas, monospace', fontSize: 18, color: '#e2e8f0', marginTop: 4 }}>
              Hasta 4 millones por fruto. Llenas de aire, viajan miles de km con el viento.
            </div>
          </div>
        </div>

        {/* Bottom Metrics Dual Cards */}
        <div style={{ width: '100%', display: 'flex', gap: 20 }}>
          <div
            style={{
              flex: 1,
              backgroundColor: 'rgba(20, 26, 36, 0.9)',
              border: '1.5px solid #00f5ff',
              borderRadius: 12,
              padding: '14px 20px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontFamily: 'Consolas, monospace', fontSize: 16, color: '#94a3b8' }}>DIVERSIDAD GLOBAL</div>
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 24, fontWeight: 800, color: '#00f5ff' }}>
              15% PLANTAS EN 1% TIERRA
            </div>
          </div>
          <div
            style={{
              flex: 1,
              backgroundColor: 'rgba(20, 26, 36, 0.9)',
              border: '1.5px solid #fbbf24',
              borderRadius: 12,
              padding: '14px 20px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontFamily: 'Consolas, monospace', fontSize: 16, color: '#94a3b8' }}>EDAD GEOLÓGICA</div>
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 24, fontWeight: 800, color: '#fbbf24' }}>
              20 MILLONES DE AÑOS
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
