import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { CatatumboHeader } from './CatatumboHeader';

export const Scene3ThermalClashCrossSection: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const vaporRise = (frame * 2.5) % 60;
  const coldDrop = (frame * 3) % 60;
  const cloudPulse = Math.sin(frame * 0.15) * 10;

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
        titlePrimary="CHOQUE"
        titleHighlight="TÉRMICO"
        highlightColor="#00f5ff"
        stickerText="CHIMENEA 12 KM"
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
          zIndex: 15,
        }}
      >
        <div style={{ position: 'absolute', top: 12, left: 16, color: '#fbbf24', fontFamily: 'monospace', fontSize: 16 }}>CORTE TRANSVERSAL · TERMODINÁMICA</div>
        <div style={{ position: 'absolute', top: 12, right: 16, color: '#00f5ff', fontFamily: 'monospace', fontSize: 16 }}>CONVECCIÓN NOCTURNA</div>
        <div style={{ position: 'absolute', bottom: 12, left: 16, color: '#64748b', fontFamily: 'monospace', fontSize: 14 }}>esquema · alturas y nube exageradas</div>
        <div style={{ position: 'absolute', bottom: 12, right: 16, color: '#00f5ff', fontFamily: 'monospace', fontSize: 14 }}>CUMULONIMBUS GIGANTE</div>

        {/* Cross Section SVG */}
        <div style={{ position: 'relative', width: 820, height: 720 }}>
          <svg width="820" height="720" viewBox="0 0 820 720" fill="none">
            {/* 1. Ground Profile: Coast -> Lake -> High Andes */}
            <path
              d="M 20 540 Q 150 540 220 580 L 460 580 Q 520 550 580 440 Q 640 320 680 180 Q 720 300 800 480 L 800 680 L 20 680 Z"
              fill="#181c24"
              stroke="rgba(255, 255, 255, 0.3)"
              strokeWidth="2.5"
            />

            {/* Lake Water Surface */}
            <rect x="220" y="580" width="240" height="100" fill="#082236" />
            <line x1="220" y1="580" x2="460" y2="580" stroke="#00f5ff" strokeWidth="3" />
            <text x="270" y="630" fill="#00f5ff" fontFamily="Consolas, monospace" fontSize="22" fontWeight="bold">LAGO CÁLIDO</text>
            <text x="310" y="655" fill="#fbbf24" fontFamily="Consolas, monospace" fontSize="18">+32 °C</text>

            {/* Andes Mountain Peak */}
            <polygon points="680,180 660,220 700,220" fill="#ffffff" />
            <text x="630" y="145" fill="#ffffff" fontFamily="Consolas, monospace" fontSize="18" fontWeight="bold">ANDES</text>
            <text x="615" y="168" fill="#fbbf24" fontFamily="Consolas, monospace" fontSize="16">4.980 METROS</text>

            {/* Rising Warm Moist Air (Orange arrows) */}
            <g stroke="#ff5722" strokeWidth="3" strokeDasharray="8 6" strokeDashoffset={-vaporRise}>
              <path d="M 290 560 Q 280 450 310 320" />
              <path d="M 340 560 Q 335 440 350 310" />
              <path d="M 390 560 Q 395 450 380 320" />
            </g>
            <rect x="260" y="440" width="160" height="36" rx="6" fill="#141820" stroke="#ff5722" strokeWidth="1.5" />
            <text x="275" y="464" fill="#ff5722" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold">VAPOR HÚMEDO ⬆</text>

            {/* Descending Cold Mountain Wind (Cyan arrows) */}
            <g stroke="#00f5ff" strokeWidth="3.5" strokeDasharray="8 6" strokeDashoffset={coldDrop}>
              <path d="M 660 250 Q 560 380 430 450" />
              <path d="M 680 300 Q 600 420 480 480" />
            </g>
            <rect x="520" y="360" width="170" height="36" rx="6" fill="#141820" stroke="#00f5ff" strokeWidth="1.5" />
            <text x="535" y="384" fill="#00f5ff" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold">AIRE HELADO ⬇ -5°C</text>

            {/* Massive Cumulonimbus Anvil Cloud */}
            <path
              d={`M 180 220 
                 C 140 180, 220 100, 320 110 
                 C 360 70, 480 60, 520 110 
                 C 620 90, 680 180, 620 230 
                 C 640 310, 560 360, 480 340 
                 C 420 380, 280 370, 240 320 
                 Z`}
              fill="rgba(30, 36, 48, 0.9)"
              stroke="#00f5ff"
              strokeWidth="2.5"
              filter="drop-shadow(0 0 20px rgba(0, 245, 255, 0.4))"
              transform={`translate(0, ${cloudPulse})`}
            />

            {/* Internal Lightning Flash in Cloud */}
            <path
              d="M 380 140 L 350 200 L 390 210 L 340 290"
              stroke="#ffffff"
              strokeWidth="4"
              strokeLinecap="round"
              filter="drop-shadow(0 0 15px #00f5ff)"
            />

            {/* Elevation Dimension Scale on Left */}
            <line x1="80" y1="100" x2="80" y2="580" stroke="#fbbf24" strokeWidth="2" strokeDasharray="4 4" />
            <line x1="70" y1="100" x2="90" y2="100" stroke="#fbbf24" strokeWidth="2" />
            <line x1="70" y1="580" x2="90" y2="580" stroke="#fbbf24" strokeWidth="2" />
            <rect x="40" y="320" width="110" height="50" rx="6" fill="#12161f" stroke="#fbbf24" strokeWidth="1.5" />
            <text x="52" y="345" fill="#fbbf24" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold">12 KM</text>
            <text x="50" y="362" fill="#ffffff" fontFamily="Consolas, monospace" fontSize="13">40.000 FT</text>
          </svg>
        </div>

        {/* Bottom Metric Badges */}
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
              border: '1.5px solid #ff5722',
              borderRadius: 12,
              padding: '12px 28px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontFamily: 'Consolas, monospace', fontSize: 16, color: '#ff5722' }}>VAPOR LACUSTRE</div>
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 38, fontWeight: 900, color: '#ffffff' }}>+32 °C <span style={{ fontSize: 20, color: '#fbbf24' }}>ASCENDENTE</span></div>
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
            <div style={{ fontFamily: 'Consolas, monospace', fontSize: 16, color: '#00f5ff' }}>NUBE CUMULONIMBUS</div>
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 38, fontWeight: 900, color: '#ffffff' }}>12.000 M <span style={{ fontSize: 20, color: '#00f5ff' }}>DE ALTURA</span></div>
          </div>
        </div>
      </div>
    </div>
  );
};
