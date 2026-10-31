import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderOrquideas } from './HeaderOrquideas';

export const Scene5OrquideasPoll: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const barSpring = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 80 },
  });

  const barA = interpolate(barSpring, [0, 1], [0, 52]);
  const barB = interpolate(barSpring, [0, 1], [0, 48]);

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
        category="¿A QUIÉN LE DAS LA"
        categoryHighlight="CORONA?"
        badgeText="TU VOTO"
        badgeColor="#fbbf24"
      />

      {/* Main Framed Laboratory Stage */}
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
          padding: '0 50px',
          zIndex: 15,
        }}
      >
        <div style={{ position: 'absolute', top: 14, left: 18, color: '#00f5ff', fontFamily: 'monospace', fontSize: 16 }}>
          DEBATE COMUNITARIO · ENIGMAIQ
        </div>
        <div style={{ position: 'absolute', top: 14, right: 18, color: '#fbbf24', fontFamily: 'monospace', fontSize: 16 }}>
          VOTACIÓN EN VIVO
        </div>

        {/* Central Poll Card */}
        <div
          style={{
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: 28,
          }}
        >
          {/* Trophy Badge Icon */}
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 10,
              marginBottom: 10,
            }}
          >
            <div
              style={{
                width: 90,
                height: 90,
                borderRadius: '50%',
                backgroundColor: 'rgba(251, 191, 36, 0.1)',
                border: '2px solid rgba(251, 191, 36, 0.4)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 0 25px rgba(251, 191, 36, 0.25)',
              }}
            >
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M6 9H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h2" />
                <path d="M18 9h2a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2h-2" />
                <path d="M4 3h16v6a8 8 0 0 1-16 0V3z" />
                <path d="M12 17v4M8 21h8" />
              </svg>
            </div>
            <div
              style={{
                fontFamily: 'Consolas, monospace',
                fontSize: 18,
                letterSpacing: 3,
                color: '#94a3b8',
                fontWeight: 600,
              }}
            >
              EL REINO DE LAS ORQUÍDEAS
            </div>
          </div>

          {/* Option A: Colombia */}
          <div
            style={{
              backgroundColor: 'rgba(20, 26, 36, 0.9)',
              border: '2px solid #00f5ff',
              borderRadius: 14,
              padding: '24px 30px',
              display: 'flex',
              flexDirection: 'column',
              gap: 15,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 30, fontWeight: 900, color: '#ffffff' }}>
                🌸 [A] COLOMBIA (4.600 en total)
              </span>
              <span style={{ fontFamily: 'Consolas, monospace', fontSize: 34, fontWeight: 900, color: '#00f5ff' }}>
                {Math.round(barA)}%
              </span>
            </div>
            <div style={{ width: '100%', height: 16, backgroundColor: 'rgba(255, 255, 255, 0.1)', borderRadius: 8, overflow: 'hidden' }}>
              <div style={{ width: `${barA}%`, height: '100%', backgroundColor: '#00f5ff', borderRadius: 8 }} />
            </div>
          </div>

          {/* Option B: Ecuador */}
          <div
            style={{
              backgroundColor: 'rgba(20, 26, 36, 0.9)',
              border: '2px solid #fb923c',
              borderRadius: 14,
              padding: '24px 30px',
              display: 'flex',
              flexDirection: 'column',
              gap: 15,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 30, fontWeight: 900, color: '#ffffff' }}>
                🌺 [B] ECUADOR (4X más densidad)
              </span>
              <span style={{ fontFamily: 'Consolas, monospace', fontSize: 34, fontWeight: 900, color: '#fb923c' }}>
                {Math.round(barB)}%
              </span>
            </div>
            <div style={{ width: '100%', height: 16, backgroundColor: 'rgba(255, 255, 255, 0.1)', borderRadius: 8, overflow: 'hidden' }}>
              <div style={{ width: `${barB}%`, height: '100%', backgroundColor: '#fb923c', borderRadius: 8 }} />
            </div>
          </div>

          {/* Call to action badge */}
          <div
            style={{
              alignSelf: 'center',
              marginTop: 15,
              backgroundColor: 'rgba(251, 191, 36, 0.15)',
              border: '2px solid #fbbf24',
              borderRadius: 12,
              padding: '16px 36px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 26, fontWeight: 900, color: '#fbbf24', letterSpacing: 1 }}>
              ESCRIBE 'COLOMBIA' O 'ECUADOR' EN COMENTARIOS 👇
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
