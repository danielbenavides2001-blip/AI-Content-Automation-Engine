import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { CatatumboHeader } from './CatatumboHeader';

export const Scene5CatatumboPoll: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const barSpring = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 80 },
  });

  const barA = interpolate(barSpring, [0, 1], [0, 68]);
  const barB = interpolate(barSpring, [0, 1], [0, 32]);

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
      <CatatumboHeader
        titlePrimary="¿TE ATREVERÍAS A"
        titleHighlight="NAVEGARLO?"
        highlightColor="#00f5ff"
        stickerText="TU TURNO"
        stickerColor="#fbbf24"
      />

      {/* Main Framed Laboratory Stage */}
      <div
        style={{
          position: 'absolute',
          top: 270,
          left: 60,
          right: 60,
          height: 1100,
          border: '1.5px solid rgba(255, 255, 255, 0.15)',
          backgroundColor: 'rgba(14, 17, 22, 0.88)',
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
        <div style={{ position: 'absolute', top: 12, left: 16, color: '#00f5ff', fontFamily: 'monospace', fontSize: 16 }}>DEBATE COMUNITARIO · ENIGMAIQ</div>
        <div style={{ position: 'absolute', top: 12, right: 16, color: '#fbbf24', fontFamily: 'monospace', fontSize: 16 }}>VOTACIÓN EN VIVO</div>
        <div style={{ position: 'absolute', bottom: 12, left: 16, color: '#64748b', fontFamily: 'monospace', fontSize: 14 }}>comenta tu opinión</div>
        <div style={{ position: 'absolute', bottom: 12, right: 16, color: '#00f5ff', fontFamily: 'monospace', fontSize: 14 }}>SÍ vs NO</div>

        {/* Central Poll Card */}
        <div
          style={{
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: 28,
          }}
        >
          {/* Radar / Expedition Ship Badge Icon */}
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
                backgroundColor: 'rgba(0, 245, 255, 0.08)',
                border: '2px solid rgba(0, 245, 255, 0.35)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 0 25px rgba(0, 245, 255, 0.2)',
              }}
            >
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#00f5ff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M2 12h20M12 2v20M4.93 4.93l14.14 14.14M4.93 19.07l14.14-14.14" strokeOpacity="0.3" />
                <circle cx="12" cy="12" r="9" stroke="#00f5ff" strokeWidth="1.5" />
                <polygon points="12 6 15 14 12 12 9 14 12 6" fill="#fbbf24" stroke="#fbbf24" strokeWidth="1" />
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
              EXPEDICIÓN LAGO DE MARACAIBO
            </div>
          </div>
          {/* Option A */}
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
              <span style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 32, fontWeight: 900, color: '#ffffff' }}>
                ⚡ [A] SÍ, SERÍA ÉPICO
              </span>
              <span style={{ fontFamily: 'Consolas, monospace', fontSize: 34, fontWeight: 900, color: '#00f5ff' }}>
                {Math.round(barA)}%
              </span>
            </div>
            <div style={{ width: '100%', height: 16, backgroundColor: 'rgba(255, 255, 255, 0.1)', borderRadius: 8, overflow: 'hidden' }}>
              <div style={{ width: `${barA}%`, height: '100%', backgroundColor: '#00f5ff', borderRadius: 8 }} />
            </div>
          </div>

          {/* Option B */}
          <div
            style={{
              backgroundColor: 'rgba(20, 26, 36, 0.9)',
              border: '2px solid #ff5722',
              borderRadius: 14,
              padding: '24px 30px',
              display: 'flex',
              flexDirection: 'column',
              gap: 15,
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 32, fontWeight: 900, color: '#ffffff' }}>
                ⛔ [B] NI LOCO, MUCHO MIEDO
              </span>
              <span style={{ fontFamily: 'Consolas, monospace', fontSize: 34, fontWeight: 900, color: '#ff5722' }}>
                {Math.round(barB)}%
              </span>
            </div>
            <div style={{ width: '100%', height: 16, backgroundColor: 'rgba(255, 255, 255, 0.1)', borderRadius: 8, overflow: 'hidden' }}>
              <div style={{ width: `${barB}%`, height: '100%', backgroundColor: '#ff5722', borderRadius: 8 }} />
            </div>
          </div>

          {/* Call to action badge */}
          <div
            style={{
              alignSelf: 'center',
              marginTop: 20,
              backgroundColor: 'rgba(251, 191, 36, 0.15)',
              border: '2px solid #fbbf24',
              borderRadius: 12,
              padding: '16px 36px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 26, fontWeight: 900, color: '#fbbf24', letterSpacing: 1 }}>
              ESCRIBE 'SÍ' O 'NO' EN LOS COMENTARIOS 👇
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
