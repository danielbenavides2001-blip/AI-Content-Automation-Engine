import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderSierra } from './HeaderSierra';

export const Scene4TectonicJourney: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const journeyProgress = interpolate(frame, [0, 160], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const arrowY = interpolate(journeyProgress, [0, 1], [380, 180]);
  const arrowX = interpolate(journeyProgress, [0, 1], [320, 390]);

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
        category="NO SIEMPRE"
        categoryHighlight="ESTUVO AHÍ"
        bigMetric="2 126 km"
        metricSubtitle="de viaje tectónico · Instituto Smithsonian"
        badgeText="170M AÑOS"
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
          padding: '24px 30px',
          zIndex: 15,
        }}
      >
        <div style={{ alignSelf: 'flex-start', color: '#00f5ff', fontFamily: 'monospace', fontSize: 16 }}>
          MIGRACIÓN DE PLACAS · INSTITUTO SMITHSONIAN
        </div>

        {/* South American Globe Scheme SVG */}
        <div style={{ width: '100%', height: 750, position: 'relative' }}>
          <svg width="100%" height="100%" viewBox="0 0 850 700">
            <defs>
              <linearGradient id="globeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#0f172a" />
                <stop offset="100%" stopColor="#020617" />
              </linearGradient>
            </defs>

            {/* Globe Outer Circle with glow */}
            <circle cx="425" cy="350" r="300" fill="url(#globeGrad)" stroke="#00f5ff" strokeWidth="2" opacity="0.8" />
            <ellipse cx="425" cy="350" rx="300" ry="120" fill="none" stroke="rgba(0, 245, 255, 0.15)" strokeWidth="1.5" />
            <ellipse cx="425" cy="350" rx="120" ry="300" fill="none" stroke="rgba(0, 245, 255, 0.15)" strokeWidth="1.5" />

            {/* South America continent contour */}
            <path
              d="M 360 140 Q 420 160 480 180 Q 560 220 540 320 Q 520 420 460 520 Q 420 600 390 620 L 370 560 Q 350 460 330 360 L 310 260 Q 320 180 360 140 Z"
              fill="#1e293b"
              stroke="#475569"
              strokeWidth="2"
            />

            {/* Starting Origin: Northern Peru (320, 380) */}
            <circle cx="320" cy="380" r="14" fill="none" stroke="#ea580c" strokeWidth="3" />
            <circle cx="320" cy="380" r="6" fill="#ea580c" />
            <text x="210" y="386" fill="#ea580c" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold">
              ORIGEN (PERÚ)
            </text>

            {/* Destination Target: Northern Colombia Caribbean (390, 180) */}
            <circle cx="390" cy="180" r="18" fill="none" stroke="#00f5ff" strokeWidth="3" strokeDasharray="4 4" />
            <circle cx="390" cy="180" r="7" fill="#00f5ff" />
            <text x="420" y="186" fill="#00f5ff" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold">
              DESTINO (CARIBE)
            </text>

            {/* Migration Trajectory Path */}
            <path
              d="M 320 380 Q 340 280 390 180"
              fill="none"
              stroke="#fbbf24"
              strokeWidth="4"
              strokeDasharray="8 6"
            />

            {/* Traveling Triangular Block */}
            <g transform={`translate(${arrowX}, ${arrowY})`}>
              <polygon points="-15,10 15,10 0,-15" fill="#fbbf24" stroke="#ffffff" strokeWidth="2" />
            </g>

            {/* Metric Floating Badge */}
            <g transform="translate(480, 360)">
              <rect x="0" y="0" width="280" height="90" rx="12" fill="rgba(20, 26, 36, 0.95)" stroke="#fbbf24" strokeWidth="2" />
              <text x="20" y="34" fill="#fbbf24" fontFamily="Consolas, monospace" fontSize="16">DURACIÓN DEL VIAJE</text>
              <text x="20" y="68" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="24" fontWeight="bold">
                170 MILLONES DE AÑOS
              </text>
            </g>
          </svg>
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
          LAS ROCAS NACIERON EN EL SUR Y NAVEGARON HASTA EL CARIBE
        </div>
      </div>
    </div>
  );
};
