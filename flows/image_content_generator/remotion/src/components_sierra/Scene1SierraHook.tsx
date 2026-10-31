import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderSierra } from './HeaderSierra';

export const Scene1SierraHook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const mountainSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 90 },
  });

  const snowFall = (frame * 2) % 400;

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
        category="DEL MAR A LA"
        categoryHighlight="NIEVE"
        bigMetric="> 5 700"
        metricSubtitle="metros de altura · montaña costera más alta"
        badgeText="RÉCORD MUNDIAL"
        badgeColor="#00f5ff"
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
          PERFIL DE ELEVACIÓN Y PISOS TÉRMICOS
        </div>

        {/* Elevation Cross Section SVG */}
        <div style={{ width: '100%', height: 780, position: 'relative' }}>
          <svg width="100%" height="100%" viewBox="0 0 900 750">
            <defs>
              <linearGradient id="oceanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="#0284c7" />
                <stop offset="100%" stopColor="#0369a1" />
              </linearGradient>
            </defs>

            {/* Rising Mountain Layers */}
            <g transform={`scale(1, ${mountainSpring})`} style={{ transformOrigin: 'bottom center' }}>
              {/* Layer 1: Base Sand & Coastal (0 - 1000m) */}
              <polygon points="120,680 780,680 720,600 210,600" fill="#d97706" opacity="0.85" />
              {/* Layer 2: Tropical Forest (1000 - 2000m) */}
              <polygon points="210,600 720,600 660,510 270,510" fill="#16a34a" />
              {/* Layer 3: Cloud Forest (2000 - 3000m) */}
              <polygon points="270,510 660,510 600,410 330,410" fill="#15803d" />
              {/* Layer 4: High Páramo (3000 - 4200m) */}
              <polygon points="330,410 600,410 540,300 390,300" fill="#047857" />
              {/* Layer 5: Rocky Scree (4200 - 4900m) */}
              <polygon points="390,300 540,300 490,200 440,200" fill="#64748b" />
              {/* Layer 6: Glacial Peak (4900 - 5775m) */}
              <polygon points="440,200 490,200 465,110" fill="#ffffff" stroke="#e2e8f0" strokeWidth="2" />
            </g>

            {/* Caribbean Ocean Base (0m) */}
            <rect x="0" y="680" width="900" height="70" fill="url(#oceanGrad)" />

            {/* Ocean Waves */}
            <path
              d="M 0 695 Q 60 685 120 695 T 240 695 T 360 695 T 480 695 T 600 695 T 720 695 T 840 695 T 900 695"
              fill="none"
              stroke="#38bdf8"
              strokeWidth="3"
            />

            {/* Tropical Palm Tree at sea level */}
            <g transform="translate(60, 600)">
              {/* Trunk */}
              <path d="M 30 80 Q 25 40 30 10" stroke="#78350f" strokeWidth="6" fill="none" strokeLinecap="round" />
              {/* Leaves */}
              <path d="M 30 10 Q 10 5 0 20" stroke="#22c55e" strokeWidth="4" fill="none" />
              <path d="M 30 10 Q 25 -10 15 -15" stroke="#22c55e" strokeWidth="4" fill="none" />
              <path d="M 30 10 Q 45 -10 55 -5" stroke="#22c55e" strokeWidth="4" fill="none" />
              <path d="M 30 10 Q 55 10 65 25" stroke="#22c55e" strokeWidth="4" fill="none" />
            </g>

            {/* Sea label */}
            <text x="35" y="730" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="24" fontWeight="bold">
              MAR CARIBE (0 M · 30°C)
            </text>

            {/* Vertical Altitude dotted line */}
            <line x1="465" y1="110" x2="465" y2="680" stroke="#fbbf24" strokeWidth="2" strokeDasharray="6 6" />

            {/* Snow particles falling from peak */}
            {[...Array(25)].map((_, i) => {
              const sx = 420 + ((i * 13) % 90);
              const sy = 110 + ((i * 29 + snowFall) % 190);
              return <circle key={i} cx={sx} cy={sy} r={2.5} fill="#ffffff" opacity={0.85} />;
            })}

            {/* Peak Callout Box */}
            <g transform="translate(520, 110)">
              <rect x="0" y="0" width="280" height="65" rx="8" fill="rgba(20, 26, 36, 0.9)" stroke="#00f5ff" strokeWidth="1.5" />
              <text x="14" y="28" fill="#94a3b8" fontFamily="Consolas, monospace" fontSize="14">CUMBRE NEVADA</text>
              <text x="14" y="52" fill="#00f5ff" fontFamily="Bahnschrift, sans-serif" fontSize="22" fontWeight="bold">5.775 METROS · 0°C</text>
            </g>
          </svg>
        </div>

        {/* Bottom Status Chip */}
        <div
          style={{
            backgroundColor: 'rgba(20, 26, 36, 0.95)',
            border: '1.5px solid #00f5ff',
            borderRadius: 10,
            padding: '12px 30px',
            fontFamily: 'Consolas, monospace',
            fontSize: 20,
            fontWeight: 800,
            color: '#00f5ff',
            letterSpacing: 2,
          }}
        >
          DESDE LA PLAYA HASTA EL HIELO EN UNA SOLA MONTAÑA
        </div>
      </div>
    </div>
  );
};
