import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderOrquideas } from './HeaderOrquideas';
import { OrchidFlowerIcon } from './OrchidFlowerIcon';
import {
  COLOMBIA_SVG_PATH,
  COLOMBIA_VIEWBOX,
  COLOMBIA_FLOWERS,
} from './real_maps_data';

export const Scene1OrquideasHook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance spring for Colombia map
  const mapSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  // Animated counter for 4.600
  // Voice speaks about 4.600 starting around frame 150
  const counterProgress = interpolate(frame, [80, 240], [0, 4600], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const formattedCount = Math.round(counterProgress).toLocaleString('es-CO');

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
        category="PRIMERO:"
        categoryHighlight="CUENTA"
        bigMetric={formattedCount}
        metricSubtitle="especies de orquídeas · Colombia"
        badgeText="MAYOR DEL TRÓPICO"
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
          justifyContent: 'center',
          zIndex: 15,
        }}
      >
        <div style={{ position: 'absolute', top: 14, left: 18, color: '#00f5ff', fontFamily: 'monospace', fontSize: 16 }}>
          COLOMBIA · DISTRIBUCIÓN FLORAL (GEO 50M)
        </div>
        <div style={{ position: 'absolute', top: 14, right: 18, color: '#fbbf24', fontFamily: 'monospace', fontSize: 16 }}>
          ESTUDIO PHYTOKEYS 2023
        </div>

        {/* Real Scaled Map Container */}
        <div
          style={{
            transform: `scale(${mapSpring})`,
            transformOrigin: 'center center',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <svg width="600" height="700" viewBox={COLOMBIA_VIEWBOX}>
            <defs>
              <clipPath id="colombiaRealClip">
                <path d={COLOMBIA_SVG_PATH} />
              </clipPath>
              <filter id="mapGlow">
                <feDropShadow dx="0" dy="0" stdDeviation="15" floodColor="#00f5ff" floodOpacity="0.35" />
              </filter>
            </defs>

            {/* Colombian National Flag Fill (50% Yellow, 25% Blue, 25% Red) */}
            <g clipPath="url(#colombiaRealClip)" filter="url(#mapGlow)">
              <rect x="0" y="0" width="600" height="350" fill="#facc15" />
              <rect x="0" y="350" width="600" height="175" fill="#1d4ed8" />
              <rect x="0" y="525" width="600" height="175" fill="#dc2626" />
            </g>

            {/* Precision Boundary Outline */}
            <path
              d={COLOMBIA_SVG_PATH}
              fill="none"
              stroke="#ffffff"
              strokeWidth="3.5"
              strokeLinejoin="round"
              strokeLinecap="round"
            />

            {/* 42 Blooming Orchids in Real Territory */}
            {COLOMBIA_FLOWERS.map((pos, idx) => (
              <OrchidFlowerIcon
                key={idx}
                x={pos.x}
                y={pos.y}
                size={34}
                delay={idx * 4.5}
                colorScheme="colombia"
              />
            ))}
          </svg>
        </div>

        {/* Bottom Status Chip */}
        <div
          style={{
            position: 'absolute',
            bottom: 25,
            backgroundColor: 'rgba(20, 26, 36, 0.95)',
            border: '1.5px solid #00f5ff',
            borderRadius: 10,
            padding: '10px 24px',
            fontFamily: 'Consolas, monospace',
            fontSize: 20,
            fontWeight: 800,
            color: '#00f5ff',
            letterSpacing: 2,
          }}
        >
          N.° 1 EN DIVERSIDAD CONTINENTAL
        </div>
      </div>
    </div>
  );
};
