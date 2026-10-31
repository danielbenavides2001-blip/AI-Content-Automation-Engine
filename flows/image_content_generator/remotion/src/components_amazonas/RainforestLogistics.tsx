import React from 'react';
import { interpolate } from 'remotion';

interface RainforestProps {
  frame: number;
  mode: 'logistics' | 'ponte_negro'; // Beat 4 vs Beat 5
}

export const RainforestLogistics: React.FC<RainforestProps> = ({ frame, mode }) => {
  // Boat traffic along the river
  const boat1X = 80 + ((frame * 2.2) % 820);
  const boat2X = 860 - (((frame + 120) * 1.5) % 800);
  const boatBobY = Math.sin(frame * 0.1) * 3;

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: 1080,
        height: 1920,
        backgroundColor: '#020d18',
        overflow: 'hidden',
      }}
    >
      {/* Background Deep Rainforest Ambient */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: 1080,
          height: 1920,
          background:
            'radial-gradient(circle at 50% 30%, #06281e 0%, #02140e 60%, #010806 100%)',
        }}
      />

      {/* SVG Container */}
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
            {/* River Gradient */}
            <linearGradient id="canopyRiverGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#0e7490" />
              <stop offset="50%" stopColor="#0891b2" />
              <stop offset="100%" stopColor="#0284c7" />
            </linearGradient>

            {/* Dark Rio Negro water */}
            <linearGradient id="rioNegroGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#09090b" />
              <stop offset="100%" stopColor="#18181b" />
            </linearGradient>

            {/* Road asphalt */}
            <linearGradient id="roadGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#334155" />
              <stop offset="100%" stopColor="#1e293b" />
            </linearGradient>
          </defs>

          {/* 1. DENSE JUNGLE CANOPY (EMERALD GREEN TEXTURE) */}
          <rect x="0" y="0" width="1000" height="960" fill="#062e1b" />

          {/* Forest Canopy Clumps */}
          <g opacity="0.6">
            {[...Array(60)].map((_, idx) => {
              const cx = (idx * 67) % 980 + 10;
              const cy = (idx * 43) % 940 + 10;
              const r = 28 + (idx % 4) * 8;
              return (
                <circle
                  key={idx}
                  cx={cx}
                  cy={cy}
                  r={r}
                  fill={idx % 2 === 0 ? '#044e2b' : '#0a5c36'}
                />
              );
            })}
          </g>

          {/* 2. THE WINDING AMAZON RIVER CHANNEL */}
          <path
            d="M 0 460 C 250 420 350 560 600 500 C 850 440 920 540 1000 520 L 1000 700 C 900 720 800 620 600 680 C 350 740 250 600 0 640 Z"
            fill="url(#canopyRiverGrad)"
            stroke="#67e8f9"
            strokeWidth="3"
          />

          {/* Water Surface Waves */}
          <g stroke="rgba(255,255,255,0.2)" strokeWidth="2" fill="none">
            {[0, 1, 2, 3].map((wIdx) => (
              <path
                key={wIdx}
                d={`M ${(wIdx * 250 + frame * 1.5) % 1000} 530 Q ${((wIdx * 250 + frame * 1.5) % 1000) + 50} 520 ${((wIdx * 250 + frame * 1.5) % 1000) + 100} 530`}
              />
            ))}
          </g>

          {/* 3. DEAD-END HIGHWAY CUTTING THROUGH JUNGLE AND ABRUPTLY ENDING */}
          {mode === 'logistics' && (
            <g>
              {/* Road segment */}
              <path
                d="M 120 0 L 170 340 L 110 340 L 60 0 Z"
                fill="url(#roadGrad)"
                stroke="#64748b"
                strokeWidth="2"
              />
              {/* Dashed center line */}
              <line
                x1="90"
                y1="0"
                x2="140"
                y2="340"
                stroke="#facc15"
                strokeWidth="2.5"
                strokeDasharray="14 12"
              />

              {/* End of Road Barrier (Barricada) */}
              <rect x="95" y="336" width="90" height="14" fill="#dc2626" rx="3" />
              <text
                x="140"
                y="380"
                textAnchor="middle"
                fill="#f87171"
                fontSize="18"
                fontFamily="Consolas, monospace"
                fontWeight="900"
                filter="drop-shadow(0 2px 6px rgba(0,0,0,0.9))"
              >
                FIN DE CARRETERA (0 ACCESOS)
              </text>
            </g>
          )}

          {/* 4. ACTIVE RIVER FLEET (BARGES & FERRIES) */}
          {/* Main Barge */}
          <g transform={`translate(${boat1X}, ${565 + boatBobY})`}>
            {/* Boat hull */}
            <path
              d="M -50 0 L 50 0 L 65 18 L -60 18 Z"
              fill="#f8fafc"
              stroke="#0f172a"
              strokeWidth="2"
            />
            {/* Cabin */}
            <rect x="-35" y="-18" width="55" height="18" rx="3" fill="#0284c7" />
            <rect x="-30" y="-14" width="10" height="8" rx="1" fill="#bae6fd" />
            <rect x="-16" y="-14" width="10" height="8" rx="1" fill="#bae6fd" />
            <rect x="-2" y="-14" width="10" height="8" rx="1" fill="#bae6fd" />

            {/* Cargo containers */}
            <rect x="22" y="-12" width="15" height="12" fill="#ea580c" />
            <rect x="38" y="-12" width="15" height="12" fill="#eab308" />

            {/* Label */}
            <text
              x="0"
              y="-26"
              textAnchor="middle"
              fill="#ffffff"
              fontSize="16"
              fontFamily="Consolas, monospace"
              fontWeight="800"
              filter="drop-shadow(0 2px 4px rgba(0,0,0,0.9))"
            >
              BARCAZA DE TRANSPORTE
            </text>
          </g>

          {/* Secondary Fast Ferry / Lancha */}
          <g transform={`translate(${boat2X}, ${630 - boatBobY})`}>
            <path
              d="M 35 0 L -35 0 L -45 12 L 40 12 Z"
              fill="#38bdf8"
              stroke="#0f172a"
              strokeWidth="1.5"
            />
            <rect x="-20" y="-10" width="35" height="10" rx="2" fill="#f8fafc" />
            <text
              x="0"
              y="-16"
              textAnchor="middle"
              fill="#e0f2fe"
              fontSize="13"
              fontFamily="Consolas, monospace"
              fontWeight="700"
            >
              LANCHA RÁPIDA
            </text>
          </g>

          {/* 5. IN MODE 'PONTE_NEGRO': MANAUS EXCEPTION CALLOUT */}
          {mode === 'ponte_negro' && (
            <g transform="translate(680, 260)">
              {/* Rio Negro Tributary Channel */}
              <path
                d="M -80 -120 Q -40 20 0 180"
                stroke="url(#rioNegroGrad)"
                strokeWidth="70"
                fill="none"
              />
              {/* Ponte Rio Negro Cable-stayed bridge representation */}
              <line
                x1="-40"
                y1="10"
                x2="40"
                y2="50"
                stroke="#ffffff"
                strokeWidth="5"
                strokeLinecap="round"
              />
              {/* Bridge pylon */}
              <polygon points="0,0 -8,55 8,55" fill="#f59e0b" />

              {/* Verified Tag */}
              <rect
                x="-120"
                y="-70"
                width="240"
                height="38"
                rx="8"
                fill="rgba(3, 15, 30, 0.92)"
                stroke="#10b981"
                strokeWidth="1.5"
              />
              <text
                x="0"
                y="-46"
                textAnchor="middle"
                fill="#34d399"
                fontSize="15"
                fontFamily="Consolas, monospace"
                fontWeight="800"
              >
                ✅ PONTE RIO NEGRO (3.6 KM)
              </text>

              {/* Arrow to Main Amazon: 0 Bridges */}
              <line x1="0" y1="80" x2="-80" y2="210" stroke="#ef4444" strokeWidth="2.5" strokeDasharray="4 4" />
              <text
                x="-90"
                y="240"
                textAnchor="middle"
                fill="#f87171"
                fontSize="18"
                fontFamily="Consolas, monospace"
                fontWeight="900"
              >
                🚫 AMAZONAS PRINCIPAL: 0 PUENTES
              </text>
            </g>
          )}
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
            border: '1.5px solid rgba(16, 185, 129, 0.5)',
            borderRadius: 14,
            padding: '10px 24px',
            boxShadow: '0 8px 30px rgba(0, 0, 0, 0.9)',
            display: 'flex',
            alignItems: 'center',
            gap: 12,
          }}
        >
          <span style={{ fontSize: 24 }}>🚢</span>
          <div
            style={{
              fontFamily: 'Consolas, monospace',
              fontSize: 22,
              fontWeight: 800,
              color: '#6ee7b7',
              letterSpacing: 1.5,
            }}
          >
            {mode === 'logistics'
              ? 'LOGÍSTICA AMAZÓNICA : EL RÍO ES LA AUTOPISTA'
              : 'EXCEPCIÓN : PUENTE SOBRE EL RÍO NEGRO, NO EL AMAZONAS'}
          </div>
        </div>
      </div>
    </div>
  );
};
