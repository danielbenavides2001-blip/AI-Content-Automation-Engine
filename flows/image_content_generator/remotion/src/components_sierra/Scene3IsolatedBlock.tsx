import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderSierra } from './HeaderSierra';

export const Scene3IsolatedBlock: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const triangleSpring = spring({
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
      <HeaderSierra
        category="¿POR QUÉ"
        categoryHighlight="ESTÁ AHÍ?"
        badgeText="NO ES ANDES"
        badgeColor="#ef4444"
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
          VISTA SATELITAL · ESTRUCTURA TECTÓNICA AISLADA
        </div>

        {/* Top-down Satellite Scheme SVG */}
        <div style={{ width: '100%', height: 750, position: 'relative' }}>
          <svg width="100%" height="100%" viewBox="0 0 850 700">
            <defs>
              <linearGradient id="caribSea" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="#0369a1" />
                <stop offset="100%" stopColor="#075985" />
              </linearGradient>
            </defs>

            {/* Caribbean Sea top zone */}
            <rect x="0" y="0" width="850" height="240" fill="url(#caribSea)" />
            <text x="50" y="70" fill="#38bdf8" fontFamily="Bahnschrift, sans-serif" fontSize="32" fontWeight="bold">
              MAR CARIBE
            </text>

            {/* Northern Colombia coastline */}
            <path
              d="M 0 240 Q 180 230 260 210 L 320 180 Q 420 160 520 180 L 640 140 L 720 170 L 850 200 L 850 700 L 0 700 Z"
              fill="#1e293b"
              stroke="#334155"
              strokeWidth="2"
            />

            {/* Andes Cordillera Chain passing on the right (elongated green spine) */}
            <g transform="translate(480, 260) rotate(35)">
              <rect x="0" y="0" width="130" height="480" rx="65" fill="#15803d" stroke="#22c55e" strokeWidth="3" opacity="0.85" />
              <text x="65" y="240" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="28" fontWeight="bold" textAnchor="middle" transform="rotate(-90 65 240)">
                CORDILLERA ANDES
              </text>
            </g>

            {/* Cesar River Valley separating them (blue line + label) */}
            <path
              d="M 440 250 Q 400 400 360 620"
              fill="none"
              stroke="#0284c7"
              strokeWidth="6"
              strokeDasharray="8 6"
            />
            <rect x="330" y="440" width="150" height="40" rx="6" fill="rgba(11, 14, 20, 0.9)" stroke="#0284c7" strokeWidth="1" />
            <text x="405" y="465" fill="#38bdf8" fontFamily="Consolas, monospace" fontSize="14" textAnchor="middle">
              VALLE RÍO CESAR
            </text>

            {/* Isolated Sierra Nevada Triangular Block */}
            <g
              transform={`translate(310, 240) scale(${triangleSpring})`}
              style={{ transformOrigin: 'center center' }}
            >
              <polygon
                points="0,0 180,40 60,220"
                fill="#d97706"
                stroke="#00f5ff"
                strokeWidth="4"
              />
              {/* Concentric high elevation rings */}
              <polygon points="20,30 140,55 60,170" fill="#b45309" stroke="#fbbf24" strokeWidth="2" />
              {/* Snowy core */}
              <polygon points="50,60 110,75 65,130" fill="#ffffff" stroke="#ffffff" strokeWidth="2" />
              <circle cx="75" cy="85" r="8" fill="#00f5ff" />
            </g>

            {/* Red X cutting Andes connection */}
            <g transform="translate(430, 310)">
              <line x1="-25" y1="-25" x2="25" y2="25" stroke="#ef4444" strokeWidth="8" strokeLinecap="round" />
              <line x1="25" y1="-25" x2="-25" y2="25" stroke="#ef4444" strokeWidth="8" strokeLinecap="round" />
            </g>

            {/* Labels */}
            <g transform="translate(100, 480)">
              <rect x="0" y="0" width="220" height="75" rx="8" fill="rgba(20, 26, 36, 0.95)" stroke="#00f5ff" strokeWidth="2" />
              <text x="110" y="32" fill="#00f5ff" fontFamily="Consolas, monospace" fontSize="16" textAnchor="middle">ESTRUCTURA</text>
              <text x="110" y="58" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="22" fontWeight="bold" textAnchor="middle">
                BLOQUE AISLADO
              </text>
            </g>
          </svg>
        </div>

        {/* Bottom Banner */}
        <div
          style={{
            backgroundColor: 'rgba(239, 68, 68, 0.12)',
            border: '1.5px solid #ef4444',
            borderRadius: 10,
            padding: '12px 30px',
            fontFamily: 'Consolas, monospace',
            fontSize: 20,
            fontWeight: 800,
            color: '#ef4444',
            letterSpacing: 2,
          }}
        >
          UNA PIRÁMIDE ROCOSA INDEPENDIENTE DEL SISTEMA ANDINO
        </div>
      </div>
    </div>
  );
};
