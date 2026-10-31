import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderOrquideas } from './HeaderOrquideas';
import { OrchidFlowerIcon } from './OrchidFlowerIcon';
import {
  COLOMBIA_SVG_PATH,
  COLOMBIA_VIEWBOX,
  COLOMBIA_FLOWERS,
  ECUADOR_SVG_PATH,
  ECUADOR_VIEWBOX,
  ECUADOR_FLOWERS,
} from './real_maps_data';

export const Scene2EndemicComparison: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Switch point: frame 160 (exact moment voice transitions to "Ahora mira a Ecuador")
  const isEcuadorPhase = frame >= 160;

  const transitionSpring = spring({
    frame: frame - 160,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  const colombiaOpacity = interpolate(frame, [150, 175], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const ecuadorOpacity = interpolate(frame, [160, 185], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Animated counter for Ecuador: 3784 -> 4450
  const ecuadorCount = interpolate(frame, [190, 320], [3784, 4450], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const formattedEcuadorCount = isEcuadorPhase
    ? `+${Math.round(ecuadorCount).toLocaleString('es-CO')}`
    : '1 572';

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
        category={isEcuadorPhase ? 'AHORA:' : 'ESPECIES:'}
        categoryHighlight={isEcuadorPhase ? 'ECUADOR' : 'ÚNICAS'}
        bigMetric={formattedEcuadorCount}
        metricSubtitle={
          isEcuadorPhase
            ? 'especies reportadas · catálogo & fundación'
            : 'solo existen en Colombia · Endémicas'
        }
        badgeText={isEcuadorPhase ? 'ECUADOR' : 'EXCLUSIVAS'}
        badgeColor={isEcuadorPhase ? '#fb923c' : '#00f5ff'}
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
        <div style={{ position: 'absolute', top: 14, left: 18, color: isEcuadorPhase ? '#fb923c' : '#00f5ff', fontFamily: 'monospace', fontSize: 16 }}>
          {isEcuadorPhase ? 'ECUADOR · SILUETA GEOGRÁFICA REAL' : 'COLOMBIA · ESPECIES ENDÉMICAS'}
        </div>
        <div style={{ position: 'absolute', top: 14, right: 18, color: '#fbbf24', fontFamily: 'monospace', fontSize: 16 }}>
          {isEcuadorPhase ? 'REPORTES 2016-2026' : 'MINAMBIENTE COLOMBIA'}
        </div>

        {/* Phase 1: Real Colombia Map with Endemics */}
        {colombiaOpacity > 0.01 && (
          <div
            style={{
              position: 'absolute',
              opacity: colombiaOpacity,
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
            }}
          >
            <svg width="580" height="680" viewBox={COLOMBIA_VIEWBOX}>
              <defs>
                <clipPath id="colombiaEndemicClip">
                  <path d={COLOMBIA_SVG_PATH} />
                </clipPath>
              </defs>

              <g clipPath="url(#colombiaEndemicClip)">
                <rect x="0" y="0" width="600" height="350" fill="#facc15" />
                <rect x="0" y="350" width="600" height="175" fill="#1d4ed8" />
                <rect x="0" y="525" width="600" height="175" fill="#dc2626" />
              </g>

              <path
                d={COLOMBIA_SVG_PATH}
                fill="none"
                stroke="#00f5ff"
                strokeWidth="3.5"
                strokeLinejoin="round"
              />

              {COLOMBIA_FLOWERS.slice(0, 25).map((pos, idx) => (
                <OrchidFlowerIcon
                  key={idx}
                  x={pos.x}
                  y={pos.y}
                  size={36}
                  delay={idx * 2}
                  colorScheme="colombia"
                />
              ))}
            </svg>
          </div>
        )}

        {/* Phase 2: Real Ecuador Map */}
        {ecuadorOpacity > 0.01 && (
          <div
            style={{
              position: 'absolute',
              opacity: ecuadorOpacity,
              transform: `scale(${0.85 + 0.15 * transitionSpring})`,
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
            }}
          >
            <svg width="560" height="560" viewBox={ECUADOR_VIEWBOX}>
              <defs>
                <clipPath id="ecuadorRealClip">
                  <path d={ECUADOR_SVG_PATH} />
                </clipPath>
                <filter id="ecuaGlow">
                  <feDropShadow dx="0" dy="0" stdDeviation="15" floodColor="#fb923c" floodOpacity="0.35" />
                </filter>
              </defs>

              <g clipPath="url(#ecuadorRealClip)" filter="url(#ecuaGlow)">
                <rect x="0" y="0" width="560" height="280" fill="#facc15" />
                <rect x="0" y="280" width="560" height="140" fill="#1d4ed8" />
                <rect x="0" y="420" width="560" height="140" fill="#dc2626" />
              </g>

              <path
                d={ECUADOR_SVG_PATH}
                fill="none"
                stroke="#ffffff"
                strokeWidth="3.5"
                strokeLinejoin="round"
              />

              {ECUADOR_FLOWERS.map((pos, idx) => (
                <OrchidFlowerIcon
                  key={idx}
                  x={pos.x}
                  y={pos.y}
                  size={36}
                  delay={idx * 2.5}
                  colorScheme="ecuador"
                />
              ))}
            </svg>
          </div>
        )}

        {/* Bottom Banner */}
        <div
          style={{
            position: 'absolute',
            bottom: 25,
            backgroundColor: 'rgba(20, 26, 36, 0.95)',
            border: `1.5px solid ${isEcuadorPhase ? '#fb923c' : '#00f5ff'}`,
            borderRadius: 10,
            padding: '10px 24px',
            fontFamily: 'Consolas, monospace',
            fontSize: 20,
            fontWeight: 800,
            color: isEcuadorPhase ? '#fb923c' : '#00f5ff',
            letterSpacing: 2,
          }}
        >
          {isEcuadorPhase ? 'ECUADOR REPORTA MÁS DE 4.400 ESPECIES' : '1.572 ESPECIES EXCLUSIVAS DE COLOMBIA'}
        </div>
      </div>
    </div>
  );
};
