import React from 'react';

interface GeotechnicalProps {
  frame: number;
}

export const GeotechnicalCrossSection: React.FC<GeotechnicalProps> = ({ frame }) => {
  // Silt drift and riverbank erosion pulse
  const shiftOffset = Math.sin(frame * 0.05) * 8;

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: 1080,
        height: 1920,
        backgroundColor: '#030a14',
        overflow: 'hidden',
      }}
    >
      {/* Background ambient lighting */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: 1080,
          height: 1920,
          background:
            'radial-gradient(ellipse at 50% 35%, #08213b 0%, #031020 60%, #01060d 100%)',
        }}
      />

      {/* Main Geotechnical Geological SVG Container */}
      <div
        style={{
          position: 'absolute',
          top: 360,
          left: 40,
          width: 1000,
          height: 960,
        }}
      >
        <svg viewBox="0 0 1000 960" width="1000" height="960" style={{ overflow: 'visible' }}>
          <defs>
            {/* Water Gradient */}
            <linearGradient id="geoWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#0369a1" stopOpacity="0.95" />
            </linearGradient>

            {/* Soft Silt / Mud Gradient */}
            <linearGradient id="softMudGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#854d0e" />
              <stop offset="50%" stopColor="#582d09" />
              <stop offset="100%" stopColor="#381a04" />
            </linearGradient>

            {/* Deep Solid Bedrock Gradient */}
            <linearGradient id="solidRockGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#334155" />
              <stop offset="100%" stopColor="#0f172a" />
            </linearGradient>

            <filter id="warningPulse" x="-30%" y="-30%" width="160%" height="160%">
              <feGaussianBlur stdDeviation="6" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* 1. LAYER 3 (DEEPEST): SOLID BEDROCK (ROCA FIRME) */}
          <path
            d="M 0 760 Q 300 750 600 770 T 1000 750 L 1000 960 L 0 960 Z"
            fill="url(#solidRockGrad)"
            stroke="#64748b"
            strokeWidth="2"
          />
          <text
            x="500"
            y="805"
            textAnchor="middle"
            fill="#94a3b8"
            fontSize="22"
            fontFamily="Consolas, monospace"
            fontWeight="800"
            letterSpacing="2"
          >
            ROCA MADRE SÓLIDA [ INALCANZABLE EN SUPERFICIE ]
          </text>

          {/* Depth measurement callout */}
          <line x1="90" y1="360" x2="90" y2="760" stroke="#f59e0b" strokeWidth="2" strokeDasharray="6 6" />
          <polygon points="90,360 84,374 96,374" fill="#f59e0b" />
          <polygon points="90,760 84,746 96,746" fill="#f59e0b" />
          <text
            x="110"
            y="570"
            fill="#fbbf24"
            fontSize="20"
            fontFamily="Consolas, monospace"
            fontWeight="900"
          >
            +60m A +100m DE PROFUNDIDAD
          </text>

          {/* 2. LAYER 2 (MIDDLE): UNSTABLE SOFT MUD & SILT (LODO ALUVIAL) */}
          <path
            d={`M 0 340 Q 250 330 480 390 Q 620 440 760 370 Q 880 320 1000 340 L 1000 760 L 0 760 Z`}
            fill="url(#softMudGrad)"
          />

          {/* Mud Texture Speckles */}
          <g opacity="0.35" fill="#fde047">
            {[...Array(25)].map((_, idx) => (
              <circle
                key={idx}
                cx={(idx * 47) % 960 + 20}
                cy={450 + (idx * 31) % 280}
                r={2.5 + (idx % 3)}
              />
            ))}
          </g>

          <text
            x="785"
            y="520"
            textAnchor="middle"
            fill="#fef08a"
            fontSize="19"
            fontFamily="Consolas, monospace"
            fontWeight="900"
            letterSpacing="1.5"
            filter="drop-shadow(0 2px 6px rgba(0,0,0,0.9))"
          >
            CAPA DE LODO BLANDO Y SEDIMENTOS
          </text>
          <text
            x="785"
            y="555"
            textAnchor="middle"
            fill="#fde047"
            fontSize="16"
            fontFamily="Consolas, monospace"
            fontWeight="700"
            opacity="0.9"
          >
            [ SUELO INESTABLE QUE COLAPSA ]
          </text>

          {/* 3. LAYER 1 (TOP): RIVER WATER MASS */}
          <path
            d="M 0 140 Q 250 145 500 140 T 1000 140 L 1000 340 Q 880 320 760 370 Q 620 440 480 390 Q 250 330 0 340 Z"
            fill="url(#geoWaterGrad)"
          />
          {/* Surface ripples */}
          <line x1="0" y1="140" x2="1000" y2="140" stroke="#bae6fd" strokeWidth="3" />

          {/* 4. ATTEMPTED HYPOTHETICAL BRIDGE PILLAR (TILTING / SINKING) */}
          <g transform={`translate(${500 + shiftOffset}, 40) rotate(${shiftOffset * 0.2} 0 400)`}>
            {/* Bridge deck on top */}
            <rect x="-140" y="20" width="280" height="26" rx="4" fill="#64748b" stroke="#cbd5e1" strokeWidth="2" />
            <line x1="-130" y1="46" x2="130" y2="46" stroke="#94a3b8" strokeWidth="3" />

            {/* Concrete pillar sinking into mud */}
            <path
              d="M -30 46 L -36 580 L 36 580 L 30 46 Z"
              fill="#475569"
              stroke="#cbd5e1"
              strokeWidth="2.5"
            />

            {/* Stress crack lines in pillar */}
            <path
              d="M -20 380 L 8 410 L -12 440"
              stroke="#ef4444"
              strokeWidth="3"
              fill="none"
              filter="url(#warningPulse)"
            />

            {/* Sinking Arrows */}
            <polygon points="0,620 -15,595 15,595" fill="#ef4444" />
            <line x1="0" y1="560" x2="0" y2="615" stroke="#ef4444" strokeWidth="3" />

            {/* Red Warning Badge */}
            <g transform="translate(0, 240)">
              <rect
                x="-120"
                y="-22"
                width="240"
                height="44"
                rx="10"
                fill="rgba(220, 38, 38, 0.92)"
                stroke="#ffffff"
                strokeWidth="2"
                filter="url(#warningPulse)"
              />
              <text
                x="0"
                y="6"
                textAnchor="middle"
                fill="#ffffff"
                fontSize="18"
                fontFamily="Bahnschrift, Arial, sans-serif"
                fontWeight="900"
                letterSpacing="1"
              >
                ⚠️ EROSIÓN Y HUNDIMIENTO
              </text>
            </g>
          </g>
        </svg>
      </div>

      {/* Top Banner Tag */}
      <div
        style={{
          position: 'absolute',
          top: 250,
          left: 100,
          right: 100,
          display: 'flex',
          justifyContent: 'center',
          pointerEvents: 'none',
          zIndex: 50,
        }}
      >
        <div
          style={{
            backgroundColor: 'rgba(5, 15, 30, 0.92)',
            border: '1.5px solid rgba(239, 68, 68, 0.5)',
            borderRadius: 14,
            padding: '10px 24px',
            boxShadow: '0 8px 30px rgba(0, 0, 0, 0.9)',
            display: 'flex',
            alignItems: 'center',
            gap: 12,
          }}
        >
          <span style={{ fontSize: 24 }}>🧱</span>
          <div
            style={{
              fontFamily: 'Consolas, monospace',
              fontSize: 22,
              fontWeight: 800,
              color: '#fca5a5',
              letterSpacing: 1.5,
            }}
          >
            PESADILLA GEOTÉCNICA : EL FONDO ES LODO VIVO
          </div>
        </div>
      </div>
    </div>
  );
};
