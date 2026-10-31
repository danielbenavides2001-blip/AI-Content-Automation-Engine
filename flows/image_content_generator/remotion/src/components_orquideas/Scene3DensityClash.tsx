import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderOrquideas } from './HeaderOrquideas';
import { OrchidFlowerIcon } from './OrchidFlowerIcon';
import {
  COLOMBIA_SVG_PATH,
  COLOMBIA_VIEWBOX,
  ECUADOR_SVG_PATH,
  ECUADOR_VIEWBOX,
} from './real_maps_data';

export const Scene3DensityClash: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Phase transition at frame 140 (when voice switches to "Si repartes las flores...")
  const isBoxPhase = frame >= 135;

  const mapScaleSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  const boxSpring = spring({
    frame: frame - 135,
    fps,
    config: { damping: 14, stiffness: 100 },
  });

  const mapOpacity = interpolate(frame, [125, 145], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const boxOpacity = interpolate(frame, [135, 155], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
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
        category={isBoxPhase ? 'REPARTE EN' : 'MIRA EL'}
        categoryHighlight={isBoxPhase ? '1 000 KM²' : 'TAMAÑO'}
        bigMetric={isBoxPhase ? '4X' : '×4,4'}
        metricSubtitle={
          isBoxPhase
            ? 'más orquídeas por km² en Ecuador'
            : 'más grande Colombia · 937.011 km²'
        }
        badgeText={isBoxPhase ? 'DENSIDAD' : 'SUPERFICIE'}
        badgeColor={isBoxPhase ? '#fbbf24' : '#00f5ff'}
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
          padding: '20px',
          zIndex: 15,
        }}
      >
        <div style={{ position: 'absolute', top: 14, left: 18, color: '#00f5ff', fontFamily: 'monospace', fontSize: 16 }}>
          {isBoxPhase ? 'DENSIDAD POR KM² · FÓRMULA MATEMÁTICA' : 'ESCALA COMPARATIVA DE TERRITORIO'}
        </div>
        <div style={{ position: 'absolute', top: 14, right: 18, color: '#fbbf24', fontFamily: 'monospace', fontSize: 16 }}>
          BANCO MUNDIAL / CIENCIA
        </div>

        {/* Phase 1: Real Map Scale Superposition (Colombia with 4 Ecuadors inside) */}
        {mapOpacity > 0.01 && (
          <div
            style={{
              position: 'absolute',
              opacity: mapOpacity,
              transform: `scale(${mapScaleSpring})`,
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
            }}
          >
            <svg width="600" height="700" viewBox={COLOMBIA_VIEWBOX}>
              <defs>
                <clipPath id="colombiaScaleClip">
                  <path d={COLOMBIA_SVG_PATH} />
                </clipPath>
              </defs>

              {/* Full Colombia Map */}
              <g clipPath="url(#colombiaScaleClip)">
                <rect x="0" y="0" width="600" height="350" fill="#facc15" />
                <rect x="0" y="350" width="600" height="175" fill="#1d4ed8" />
                <rect x="0" y="525" width="600" height="175" fill="#dc2626" />
              </g>

              <path
                d={COLOMBIA_SVG_PATH}
                fill="none"
                stroke="#ffffff"
                strokeWidth="4"
                strokeLinejoin="round"
              />

              {/* Stacked dashed outlines of Ecuador showing 4x fit inside Colombia */}
              <g transform="translate(180, 140) scale(0.42)">
                <path d={ECUADOR_SVG_PATH} fill="none" stroke="#00f5ff" strokeWidth="6" strokeDasharray="10 8" />
              </g>
              <g transform="translate(290, 240) scale(0.42)">
                <path d={ECUADOR_SVG_PATH} fill="none" stroke="#00f5ff" strokeWidth="6" strokeDasharray="10 8" />
              </g>
              <g transform="translate(160, 340) scale(0.42)">
                <path d={ECUADOR_SVG_PATH} fill="none" stroke="#00f5ff" strokeWidth="6" strokeDasharray="10 8" />
              </g>
              <g transform="translate(260, 440) scale(0.42)">
                <path d={ECUADOR_SVG_PATH} fill="none" stroke="#00f5ff" strokeWidth="6" strokeDasharray="10 8" />
              </g>

              {/* Callout chip */}
              <rect x="180" y="58" width="240" height="42" rx="8" fill="rgba(11, 14, 20, 0.95)" stroke="#00f5ff" strokeWidth="1.5" />
              <text x="300" y="85" fill="#00f5ff" fontFamily="Consolas, monospace" fontSize="18" fontWeight="bold" textAnchor="middle">
                4,4 VECES ECUADOR
              </text>
            </svg>
          </div>
        )}

        {/* Phase 2: Density Comparison Boxes */}
        {boxOpacity > 0.01 && (
          <div
            style={{
              position: 'absolute',
              opacity: boxOpacity,
              transform: `scale(${boxSpring})`,
              width: '94%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 20,
            }}
          >
            <div
              style={{
                display: 'flex',
                gap: 20,
                width: '100%',
                justifyContent: 'center',
              }}
            >
              {/* Colombia Box (4 flowers) */}
              <div
                style={{
                  flex: 1,
                  height: 490,
                  backgroundColor: 'rgba(18, 24, 34, 0.95)',
                  border: '2px solid rgba(0, 245, 255, 0.5)',
                  borderRadius: 14,
                  position: 'relative',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  padding: 16,
                  overflow: 'hidden',
                }}
              >
                <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 6, display: 'flex' }}>
                  <div style={{ flex: 2, backgroundColor: '#facc15' }} />
                  <div style={{ flex: 1, backgroundColor: '#1d4ed8' }} />
                  <div style={{ flex: 1, backgroundColor: '#dc2626' }} />
                </div>

                <svg width="100%" height="340" style={{ marginTop: 20 }}>
                  <OrchidFlowerIcon x={80} y={90} size={44} delay={0} colorScheme="colombia" />
                  <OrchidFlowerIcon x={240} y={90} size={44} delay={5} colorScheme="colombia" />
                  <OrchidFlowerIcon x={120} y={230} size={44} delay={10} colorScheme="colombia" />
                  <OrchidFlowerIcon x={260} y={230} size={44} delay={15} colorScheme="colombia" />
                </svg>

                <div
                  style={{
                    backgroundColor: 'rgba(11, 14, 20, 0.85)',
                    borderRadius: 10,
                    padding: '12px 10px',
                    textAlign: 'center',
                    fontFamily: 'Bahnschrift, sans-serif',
                    fontSize: 26,
                    fontWeight: 900,
                    color: '#fbbf24',
                  }}
                >
                  COLOMBIA · <span style={{ color: '#ffffff' }}>4 FLORES</span>
                </div>
              </div>

              {/* Ecuador Box (15 flowers) */}
              <div
                style={{
                  flex: 1,
                  height: 490,
                  backgroundColor: 'rgba(18, 24, 34, 0.95)',
                  border: '2px solid #fb923c',
                  borderRadius: 14,
                  position: 'relative',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  padding: 16,
                  overflow: 'hidden',
                  boxShadow: '0 0 25px rgba(251, 146, 60, 0.25)',
                }}
              >
                <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 6, display: 'flex' }}>
                  <div style={{ flex: 2, backgroundColor: '#facc15' }} />
                  <div style={{ flex: 1, backgroundColor: '#1d4ed8' }} />
                  <div style={{ flex: 1, backgroundColor: '#dc2626' }} />
                </div>

                <svg width="100%" height="340" style={{ marginTop: 20 }}>
                  {[
                    { x: 50, y: 50 }, { x: 120, y: 50 }, { x: 190, y: 50 }, { x: 260, y: 50 },
                    { x: 50, y: 120 }, { x: 120, y: 120 }, { x: 190, y: 120 }, { x: 260, y: 120 },
                    { x: 50, y: 190 }, { x: 120, y: 190 }, { x: 190, y: 190 }, { x: 260, y: 190 },
                    { x: 85, y: 260 }, { x: 155, y: 260 }, { x: 225, y: 260 },
                  ].map((pos, idx) => (
                    <OrchidFlowerIcon
                      key={idx}
                      x={pos.x + 35}
                      y={pos.y + 20}
                      size={32}
                      delay={idx * 0.8}
                      colorScheme="ecuador"
                    />
                  ))}
                </svg>

                <div
                  style={{
                    backgroundColor: 'rgba(11, 14, 20, 0.85)',
                    borderRadius: 10,
                    padding: '12px 10px',
                    textAlign: 'center',
                    fontFamily: 'Bahnschrift, sans-serif',
                    fontSize: 26,
                    fontWeight: 900,
                    color: '#fb923c',
                  }}
                >
                  ECUADOR · <span style={{ color: '#ffffff' }}>15 FLORES</span>
                </div>
              </div>
            </div>

            {/* Bottom Density Banner */}
            <div
              style={{
                backgroundColor: 'rgba(251, 191, 36, 0.15)',
                border: '1.5px solid #fbbf24',
                borderRadius: 10,
                padding: '12px 30px',
                fontFamily: 'Consolas, monospace',
                fontSize: 22,
                fontWeight: 800,
                color: '#fbbf24',
                letterSpacing: 2,
              }}
            >
              ¡ECUADOR TIENE CASI 4 VECES MÁS DENSIDAD!
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
