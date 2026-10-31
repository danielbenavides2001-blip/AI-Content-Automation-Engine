import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { CatatumboHeader } from './CatatumboHeader';

export const Scene2HorseshoeTrap: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const arrowOffset = (frame * 3) % 40;

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
        titlePrimary="LA TRAMPA"
        titleHighlight="GEOGRÁFICA"
        highlightColor="#fbbf24"
        stickerText="HERRADURA NATURAL"
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
        <div style={{ position: 'absolute', top: 12, left: 16, color: '#fbbf24', fontFamily: 'monospace', fontSize: 16 }}>RELIEVE 3D · BARRERAS ANDINAS</div>
        <div style={{ position: 'absolute', top: 12, right: 16, color: '#00f5ff', fontFamily: 'monospace', fontSize: 16 }}>CUENCA EN HERRADURA</div>
        <div style={{ position: 'absolute', bottom: 12, left: 16, color: '#64748b', fontFamily: 'monospace', fontSize: 14 }}>esquema · encierro orográfico</div>
        <div style={{ position: 'absolute', bottom: 12, right: 16, color: '#ff5722', fontFamily: 'monospace', fontSize: 14 }}>SIN SALIDA AL SUR</div>

        {/* Mountain Horseshoe Diagram */}
        <div style={{ position: 'relative', width: 800, height: 720 }}>
          <svg width="800" height="720" viewBox="0 0 800 720" fill="none">
            {/* North Entrance for Caribbean Winds */}
            <rect x="250" y="30" width="300" height="70" rx="8" fill="rgba(0, 245, 255, 0.1)" stroke="#00f5ff" strokeWidth="1.5" />
            <text x="300" y="70" fill="#00f5ff" fontFamily="Consolas, monospace" fontSize="20" fontWeight="bold">ENTRADA CARIBE (NORTE)</text>

            {/* Inflow Wind Arrows */}
            <path
              d="M 400 110 L 400 240"
              stroke="#00f5ff"
              strokeWidth="4"
              strokeDasharray="10 6"
              strokeDashoffset={-arrowOffset}
            />
            <polygon points="400,260 388,235 412,235" fill="#00f5ff" />

            {/* Central Lake Basin */}
            <ellipse cx="400" cy="380" rx="140" ry="170" fill="#081826" stroke="#00f5ff" strokeWidth="2.5" />
            <text x="350" y="375" fill="#ffffff" fontFamily="Consolas, monospace" fontSize="22" fontWeight="bold">LAGO</text>
            <text x="325" y="405" fill="#00f5ff" fontFamily="Consolas, monospace" fontSize="20" fontWeight="bold">MARACAIBO</text>

            {/* WEST WALL: Serranía del Perijá */}
            <path
              d="M 230 180 Q 210 320 220 520 Q 240 560 270 580"
              stroke="#10b981"
              strokeWidth="32"
              strokeLinecap="round"
              fill="none"
              opacity="0.85"
            />
            <path
              d="M 230 180 Q 210 320 220 520 Q 240 560 270 580"
              stroke="#ffffff"
              strokeWidth="2"
              strokeDasharray="6 6"
              fill="none"
            />
            {/* Label West */}
            <rect x="20" y="330" width="180" height="55" rx="6" fill="#12161f" stroke="#10b981" strokeWidth="1.5" />
            <text x="35" y="354" fill="#10b981" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold">SERRANÍA DEL PERIJÁ</text>
            <text x="35" y="375" fill="#ffffff" fontFamily="Consolas, monospace" fontSize="15">3.600 M ALTITUD</text>

            {/* EAST & SOUTH WALL: Cordillera de Mérida */}
            <path
              d="M 570 190 Q 600 350 560 550 Q 480 620 340 600"
              stroke="#fbbf24"
              strokeWidth="38"
              strokeLinecap="round"
              fill="none"
              opacity="0.85"
            />
            <path
              d="M 570 190 Q 600 350 560 550 Q 480 620 340 600"
              stroke="#ffffff"
              strokeWidth="2"
              strokeDasharray="6 6"
              fill="none"
            />
            {/* Label East */}
            <rect x="590" y="420" width="195" height="55" rx="6" fill="#12161f" stroke="#fbbf24" strokeWidth="1.5" />
            <text x="605" y="444" fill="#fbbf24" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold">CORDILLERA DE MÉRIDA</text>
            <text x="605" y="465" fill="#ffffff" fontFamily="Consolas, monospace" fontSize="15">4.980 M GLACIARES</text>

            {/* The Trap Box (Dead End) */}
            <rect x="300" y="520" width="200" height="50" rx="8" fill="#ff5722" />
            <text x="320" y="552" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="22" fontWeight="900" letterSpacing="1">⚠️ TRAP HORSE-SHOE</text>
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
              border: '1.5px solid #10b981',
              borderRadius: 12,
              padding: '12px 28px',
              textAlign: 'center',
            }}
          >
            <div style={{ fontFamily: 'Consolas, monospace', fontSize: 16, color: '#10b981' }}>BARRERA OESTE</div>
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 38, fontWeight: 900, color: '#ffffff' }}>PERIJÁ <span style={{ fontSize: 22, color: '#fbbf24' }}>3.600 M</span></div>
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
            <div style={{ fontFamily: 'Consolas, monospace', fontSize: 16, color: '#fbbf24' }}>BARRERA ESTE/SUR</div>
            <div style={{ fontFamily: 'Bahnschrift, sans-serif', fontSize: 38, fontWeight: 900, color: '#ffffff' }}>MÉRIDA <span style={{ fontSize: 22, color: '#00f5ff' }}>4.980 M</span></div>
          </div>
        </div>
      </div>
    </div>
  );
};
