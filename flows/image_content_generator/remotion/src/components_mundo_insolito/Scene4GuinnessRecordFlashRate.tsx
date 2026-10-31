import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { CatatumboHeader } from './CatatumboHeader';

export const Scene4GuinnessRecordFlashRate: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const radarSweep = (frame * 4) % 360;
  const pulseRings = (frame * 2) % 60;

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
        titlePrimary="EL FARO"
        titleHighlight="NATURAL"
        highlightColor="#fbbf24"
        stickerText="300 NOCHES / AÑO"
        stickerColor="#00f5ff"
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
        <div style={{ position: 'absolute', top: 12, left: 16, color: '#fbbf24', fontFamily: 'monospace', fontSize: 16 }}>TELEMETRÍA · RANGO ÓPTICO</div>
        <div style={{ position: 'absolute', top: 12, right: 16, color: '#00f5ff', fontFamily: 'monospace', fontSize: 16 }}>NAVEGACIÓN CARIBEÑA</div>
        <div style={{ position: 'absolute', bottom: 12, left: 16, color: '#64748b', fontFamily: 'monospace', fontSize: 14 }}>alcance visual · 400 km mar adentro</div>
        <div style={{ position: 'absolute', bottom: 12, right: 16, color: '#fbbf24', fontFamily: 'monospace', fontSize: 14 }}>28 RAYOS / MINUTO</div>

        {/* Central Lighthouse Radar Visualization */}
        <div style={{ position: 'relative', width: 780, height: 700, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <svg width="760" height="660" viewBox="0 0 760 660" fill="none">
            {/* Concentric Range Rings */}
            {[100, 200, 300, 400].map((km, idx) => {
              const r = 70 + idx * 65;
              return (
                <g key={km}>
                  <circle cx="380" cy="360" r={r} stroke="rgba(0, 245, 255, 0.2)" strokeWidth="1.5" strokeDasharray="4 6" />
                  <text x={385} y={360 - r + 18} fill="rgba(0, 245, 255, 0.6)" fontFamily="Consolas, monospace" fontSize="14">
                    {km} KM
                  </text>
                </g>
              );
            })}

            {/* Pulsing Light Waves radiating */}
            <circle cx="380" cy="360" r={40 + pulseRings * 4} stroke="#fbbf24" strokeWidth="2" opacity={1 - pulseRings / 60} />

            {/* Rotating Light Beam (Faro natural) */}
            <g transform={`rotate(${radarSweep} 380 360)`}>
              <path d="M 380 360 L 680 200 A 340 340 0 0 1 720 360 Z" fill="url(#beamGrad)" opacity="0.45" />
            </g>

            <defs>
              <radialGradient id="beamGrad" cx="0%" cy="50%" r="100%">
                <stop offset="0%" stopColor="#fbbf24" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#00f5ff" stopOpacity="0" />
              </radialGradient>
            </defs>

            {/* Center Catatumbo Epicenter Dot */}
            <circle cx="380" cy="360" r="14" fill="#fbbf24" filter="drop-shadow(0 0 15px #fbbf24)" />
            <circle cx="380" cy="360" r="6" fill="#ffffff" />
            <text x="310" y="415" fill="#ffffff" fontFamily="Consolas, monospace" fontSize="18" fontWeight="bold">EPICENTRO</text>
            <text x="290" y="438" fill="#fbbf24" fontFamily="Consolas, monospace" fontSize="16">FAROL DE MARACAIBO</text>
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
              border: '1.5px solid #fbbf24',
              borderRadius: 12,
              padding: '12px 28px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontFamily: 'Consolas, monospace', fontSize: 16, color: '#fbbf24' }}>CADENCIA DE IMPACTO</div>
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 38, fontWeight: 900, color: '#ffffff' }}>28 RAYOS <span style={{ fontSize: 20, color: '#00f5ff' }}>/ MINUTO</span></div>
          </div>

          <div
            style={{
              backgroundColor: 'rgba(24, 28, 36, 0.95)',
              border: '1.5px solid #00f5ff',
              borderRadius: 12,
              padding: '12px 28px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontFamily: 'Consolas, monospace', fontSize: 16, color: '#00f5ff' }}>VISIBILIDAD EN MAR</div>
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 38, fontWeight: 900, color: '#ffffff' }}>400 KM <span style={{ fontSize: 20, color: '#fbbf24' }}>DE ALCANCE</span></div>
          </div>
        </div>
      </div>
    </div>
  );
};
