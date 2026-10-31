import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderSierra } from './HeaderSierra';

export const Scene2MarathonGradient: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const runnerProgress = interpolate(frame, [0, 150], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const runnerX = interpolate(runnerProgress, [0, 1], [100, 750]);

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
      <HeaderSierra
        category="MIRA LO QUE"
        categoryHighlight="SIGNIFICA"
        bigMetric="42 km"
        metricSubtitle="la distancia de un maratón · de la playa al hielo"
        badgeText="EXTREMO"
        badgeColor="#fbbf24"
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
          LA ESCALA DEL GRADIENTE: DISTANCIA MARATÓN
        </div>

        {/* Dynamic Distance Ruler Graphic */}
        <div style={{ width: '100%', height: 650, position: 'relative' }}>
          <svg width="100%" height="100%" viewBox="0 0 850 550">
            <defs>
              <linearGradient id="tempGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#ea580c" />
                <stop offset="35%" stopColor="#eab308" />
                <stop offset="70%" stopColor="#06b6d4" />
                <stop offset="100%" stopColor="#ffffff" />
              </linearGradient>
            </defs>

            {/* Gradient Road Bar */}
            <rect x="80" y="260" width="690" height="24" rx="12" fill="url(#tempGradient)" />

            {/* Distance Ticks */}
            {[0, 10, 20, 30, 42].map((km, i) => {
              const tx = 80 + (km / 42) * 690;
              return (
                <g key={i} transform={`translate(${tx}, 260)`}>
                  <line x1={0} y1={-15} x2={0} y2={39} stroke="#ffffff" strokeWidth="2" />
                  <text x={0} y={65} fill="#94a3b8" fontFamily="Consolas, monospace" fontSize="18" textAnchor="middle">
                    {km} KM
                  </text>
                </g>
              );
            })}

            {/* Left Extreme: Playa Caribe */}
            <g transform="translate(60, 120)">
              <rect x="0" y="0" width="160" height="90" rx="10" fill="rgba(234, 88, 12, 0.15)" stroke="#ea580c" strokeWidth="2" />
              <text x="80" y="32" fill="#ea580c" fontFamily="Bahnschrift, sans-serif" fontSize="22" fontWeight="bold" textAnchor="middle">
                PLAYA
              </text>
              <text x="80" y="65" fill="#ffffff" fontFamily="Consolas, monospace" fontSize="30" fontWeight="900" textAnchor="middle">
                +30°C
              </text>
            </g>

            {/* Right Extreme: Cumbre Helada */}
            <g transform="translate(630, 120)">
              <rect x="0" y="0" width="160" height="90" rx="10" fill="rgba(255, 255, 255, 0.15)" stroke="#ffffff" strokeWidth="2" />
              <text x="80" y="32" fill="#00f5ff" fontFamily="Bahnschrift, sans-serif" fontSize="22" fontWeight="bold" textAnchor="middle">
                GLACIAR
              </text>
              <text x="80" y="65" fill="#ffffff" fontFamily="Consolas, monospace" fontSize="30" fontWeight="900" textAnchor="middle">
                0°C
              </text>
            </g>

            {/* Animated Pin */}
            <g transform={`translate(${runnerX}, 248)`}>
              <circle cx={0} cy={-25} r={20} fill="#fbbf24" stroke="#ffffff" strokeWidth="2" />
              <text x={0} y={-18} fill="#0b0e14" fontFamily="Bahnschrift, sans-serif" fontSize="18" fontWeight="bold" textAnchor="middle">
                🏃
              </text>
              <polygon points="0,0 -8,-10 8,-10" fill="#fbbf24" />
            </g>
          </svg>

          {/* Central Highlight Card */}
          <div
            style={{
              position: 'absolute',
              bottom: 40,
              left: 40,
              right: 40,
              backgroundColor: 'rgba(20, 26, 36, 0.95)',
              border: '1.5px solid #00f5ff',
              borderRadius: 12,
              padding: '18px 24px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 26, fontWeight: 900, color: '#ffffff' }}>
              EN NINGÚN OTRO LUGAR DE LA TIERRA
            </div>
            <div style={{ fontFamily: 'Consolas, monospace', fontSize: 18, color: '#94a3b8', marginTop: 4 }}>
              Pasas del mar Caribe tropical a la nieve perpetua en la misma distancia que corre un maratonista.
            </div>
          </div>
        </div>

        {/* Bottom Banner */}
        <div
          style={{
            backgroundColor: 'rgba(251, 191, 36, 0.12)',
            border: '1.5px solid #fbbf24',
            borderRadius: 10,
            padding: '12px 30px',
            fontFamily: 'Consolas, monospace',
            fontSize: 20,
            fontWeight: 800,
            color: '#fbbf24',
            letterSpacing: 2,
          }}
        >
          CAMBIO TÉRMICO DE 30°C EN 42 KILÓMETROS
        </div>
      </div>
    </div>
  );
};
