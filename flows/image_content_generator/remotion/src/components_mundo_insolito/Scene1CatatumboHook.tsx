import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { CatatumboHeader } from './CatatumboHeader';

export const Scene1CatatumboHook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pulse = Math.sin(frame * 0.2) * 0.5 + 0.5;
  const mapSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 100 },
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
      <CatatumboHeader
        titlePrimary="LA FÁBRICA DE"
        titleHighlight="RAYOS"
        highlightColor="#00f5ff"
        stickerText="RÉCORD GUINNESS"
        stickerColor="#ff5722"
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
          zIndex: 15,
        }}
      >
        {/* Stage Corner Markers */}
        <div style={{ position: 'absolute', top: 12, left: 16, color: '#00f5ff', fontFamily: 'monospace', fontSize: 16 }}>+ 10.0°N</div>
        <div style={{ position: 'absolute', top: 12, right: 16, color: '#00f5ff', fontFamily: 'monospace', fontSize: 16 }}>71.6°W +</div>
        <div style={{ position: 'absolute', bottom: 12, left: 16, color: '#64748b', fontFamily: 'monospace', fontSize: 14 }}>esquema · cuenca del lago de maracaibo</div>
        <div style={{ position: 'absolute', bottom: 12, right: 16, color: '#fbbf24', fontFamily: 'monospace', fontSize: 14 }}>250 RAYOS / KM²</div>

        {/* Map Vector Graphic */}
        <div
          style={{
            transform: `scale(${mapSpring})`,
            opacity: mapSpring,
            position: 'relative',
            width: 800,
            height: 700,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          {/* Caribbean Sea & Coastline Silhouette SVG */}
          <svg width="760" height="660" viewBox="0 0 760 660" fill="none">
            {/* Sea Base */}
            <path
              d="M 50 50 Q 250 80 450 40 T 710 70 L 710 200 Q 550 220 400 240 L 50 200 Z"
              fill="#0d2438"
              stroke="#00f5ff"
              strokeWidth="2"
              opacity="0.8"
            />
            <text x="320" y="110" fill="#00f5ff" fontFamily="Consolas, monospace" fontSize="22" fontWeight="bold" letterSpacing="3">MAR CARIBE</text>

            {/* Land Mass & Lake Basin */}
            <path
              d="M 50 200 Q 200 220 320 250 Q 340 380 320 520 Q 420 540 450 420 Q 480 310 420 250 Q 580 230 710 210 L 710 620 L 50 620 Z"
              fill="#181c24"
              stroke="rgba(255, 255, 255, 0.25)"
              strokeWidth="2"
            />

            {/* Lake Maracaibo Contour */}
            <path
              d="M 330 260 C 370 270 380 340 375 420 C 370 480 340 500 325 460 C 310 400 305 320 330 260 Z"
              fill="#061826"
              stroke="#00f5ff"
              strokeWidth="3.5"
            />
            <text x="320" y="380" fill="#ffffff" fontFamily="Consolas, monospace" fontSize="18" fontWeight="bold">LAGO</text>
            <text x="300" y="405" fill="#00f5ff" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold">MARACAIBO</text>

            {/* Catatumbo Hotspot Pulse Target */}
            <circle
              cx="315"
              cy="450"
              r={25 + pulse * 45}
              fill="none"
              stroke="#ff5722"
              strokeWidth="2"
              opacity={1 - pulse}
            />
            <circle
              cx="315"
              cy="450"
              r={12 + pulse * 20}
              fill="none"
              stroke="#fbbf24"
              strokeWidth="2.5"
              opacity={1 - pulse * 0.7}
            />
            <circle
              cx="315"
              cy="450"
              r="7"
              fill="#00f5ff"
              filter="drop-shadow(0 0 10px #00f5ff)"
            />

            {/* Pointer to Catatumbo Delta */}
            <line x1="315" y1="450" x2="160" y2="520" stroke="#fbbf24" strokeWidth="2" strokeDasharray="4 4" />
            <rect x="70" y="500" width="170" height="42" rx="6" fill="#12161f" stroke="#fbbf24" strokeWidth="1.5" />
            <text x="85" y="528" fill="#fbbf24" fontFamily="Consolas, monospace" fontSize="18" fontWeight="bold">DELTA CATATUMBO</text>
          </svg>
        </div>

        {/* Big Impact Metric Chips at bottom */}
        <div
          style={{
            position: 'absolute',
            bottom: 45,
            display: 'flex',
            gap: 20,
            alignItems: 'center',
          }}
        >
          <div
            style={{
              backgroundColor: 'rgba(24, 28, 36, 0.95)',
              border: '1.5px solid #00f5ff',
              borderRadius: 12,
              padding: '12px 28px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontFamily: 'Consolas, monospace', fontSize: 16, color: '#00f5ff' }}>FRECUENCIA ANUAL</div>
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 42, fontWeight: 900, color: '#ffffff' }}>250 <span style={{ fontSize: 24, color: '#fbbf24' }}>RAYOS / KM²</span></div>
          </div>

          <div
            style={{
              backgroundColor: 'rgba(24, 28, 36, 0.95)',
              border: '1.5px solid #fbbf24',
              borderRadius: 12,
              padding: '12px 28px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontFamily: 'Consolas, monospace', fontSize: 16, color: '#fbbf24' }}>DURACIÓN</div>
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 42, fontWeight: 900, color: '#ffffff' }}>10 HORAS <span style={{ fontSize: 24, color: '#00f5ff' }}>POR NOCHE</span></div>
          </div>
        </div>
      </div>
    </div>
  );
};
