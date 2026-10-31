import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { DynamicScene } from './types';

export const SceneGeologicalCrossSection: React.FC<{
  scene: DynamicScene;
  primaryColor?: string;
  secondaryColor?: string;
  accentColor?: string;
}> = ({
  scene,
  primaryColor = '#00f5ff',
  secondaryColor = '#38bdf8',
  accentColor = '#f59e0b'
}) => {
  const frame = useCurrentFrame();

  // Natural organic waves and fluid drift
  const waveA = Math.sin(frame * 0.06) * 7;
  const waveB = Math.cos(frame * 0.08) * 5;
  const waterFlow = (frame * 3.5) % 300;
  const bubbleY = (frame * 1.5) % 120;
  const seismicPulse = Math.sin(frame * 0.15) * 0.25 + 0.75;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '110px 40px 320px 40px',
        boxSizing: 'border-box',
        fontFamily: "'Bahnschrift', 'Montserrat', Arial, sans-serif",
      }}
    >
      {/* 1. Top Scene Headline */}
      <div
        style={{
          textAlign: 'center',
          marginBottom: 20,
          opacity: Math.min(1, frame / 12),
          transform: `translateY(${interpolate(frame, [0, 12], [-16, 0], { extrapolateRight: 'clamp' })}px)`,
        }}
      >
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 10,
            padding: '6px 18px',
            borderRadius: 20,
            backgroundColor: 'rgba(2, 9, 20, 0.85)',
            border: `1.5px solid ${accentColor}80`,
            boxShadow: `0 0 20px ${accentColor}30`,
            marginBottom: 8,
          }}
        >
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              backgroundColor: accentColor,
              boxShadow: `0 0 10px ${accentColor}`,
            }}
          />
          <span
            style={{
              fontSize: 18,
              letterSpacing: 3,
              color: '#ffffff',
              fontWeight: 800,
              textTransform: 'uppercase',
            }}
          >
            {scene.headline || 'ESTRUCTURA SUBSUPERFICIAL & GEOLOGÍA'}
          </span>
        </div>

        <div
          style={{
            fontSize: 34,
            fontWeight: 900,
            color: '#ffffff',
            lineHeight: 1.15,
            maxWidth: 960,
            textShadow: '0 4px 24px rgba(0,0,0,0.9)',
          }}
        >
          {scene.subheadline || 'CORTE TRANSVERSAL: ESTRATOS & FENÓMENOS OCULTOS'}
        </div>
      </div>

      {/* 2. Main Geological Cross-Section Canvas */}
      <div
        style={{
          position: 'relative',
          width: '100%',
          maxWidth: 960,
          height: 620,
          backgroundColor: '#020712',
          borderRadius: 24,
          border: `2px solid ${primaryColor}80`,
          overflow: 'hidden',
          boxShadow: `0 0 45px ${primaryColor}25`,
        }}
      >
        <svg width="100%" height="100%" viewBox="0 0 960 620" style={{ overflow: 'visible' }}>
          <defs>
            {/* Surface Rainforest / Topography Gradient */}
            <linearGradient id="surfaceFloraGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#15803d" />
              <stop offset="35%" stopColor="#047857" />
              <stop offset="100%" stopColor="#2b1810" />
            </linearGradient>

            {/* Karst Limestone & Mud Sediment Gradient */}
            <linearGradient id="karstSedimentGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#582d09" />
              <stop offset="45%" stopColor="#78716c" />
              <stop offset="100%" stopColor="#44403c" />
            </linearGradient>

            {/* Subterranean Aquifer Water Gradient (Turquoise Glow) */}
            <linearGradient id="aquiferWaterGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#0284c7" stopOpacity="0.85" />
              <stop offset="50%" stopColor="#00f5ff" stopOpacity="0.95" />
              <stop offset="100%" stopColor="#0369a1" stopOpacity="0.85" />
            </linearGradient>

            {/* Basalt Bedrock Slate Gradient */}
            <linearGradient id="basaltRockGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#1e293b" />
              <stop offset="100%" stopColor="#090d16" />
            </linearGradient>

            {/* Deep Geothermal Magma Chamber Gradient */}
            <linearGradient id="magmaThermalGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#f97316" />
              <stop offset="40%" stopColor="#dc2626" />
              <stop offset="100%" stopColor="#450a0a" />
            </linearGradient>

            {/* Water Glow & Caustic Filter */}
            <filter id="waterGlowFilter" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>

            {/* Seismic Fault Glow */}
            <filter id="faultWarningGlow" x="-30%" y="-30%" width="160%" height="160%">
              <feGaussianBlur stdDeviation="5" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* ---------------------------------------------------- */}
          {/* LAYER 5 (BASE): DEEP GEOTHERMAL MAGMA CHAMBER (-4.000m) */}
          {/* ---------------------------------------------------- */}
          <path
            d="M 0 520 Q 240 500 480 525 T 960 515 L 960 620 L 0 620 Z"
            fill="url(#magmaThermalGrad)"
          />
          {/* Magma Convection Heat Lines */}
          <g opacity={seismicPulse * 0.7}>
            <path
              d="M 120 610 Q 180 550 220 540"
              fill="none"
              stroke="#fbbf24"
              strokeWidth="2.5"
              strokeDasharray="6 6"
            />
            <path
              d="M 520 610 Q 560 545 610 535"
              fill="none"
              stroke="#fbbf24"
              strokeWidth="2.5"
              strokeDasharray="6 6"
            />
            <path
              d="M 780 610 Q 820 560 870 545"
              fill="none"
              stroke="#fbbf24"
              strokeWidth="2.5"
              strokeDasharray="6 6"
            />
          </g>

          {/* ---------------------------------------------------- */}
          {/* LAYER 4: BASALT & TECTONIC BEDROCK (-1.500m to -4.000m) */}
          {/* ---------------------------------------------------- */}
          <path
            d={`M 0 350 Q 260 ${335 + waveA} 500 360 T 960 ${345 - waveA} L 960 520 Q 720 515 480 525 T 0 520 Z`}
            fill="url(#basaltRockGrad)"
            stroke="#334155"
            strokeWidth="1.5"
          />

          {/* Bedrock Strata Texture Flecks */}
          <g opacity="0.3" fill="#94a3b8">
            {[...Array(35)].map((_, idx) => (
              <circle
                key={`flecks-${idx}`}
                cx={(idx * 59) % 940 + 10}
                cy={370 + (idx * 23) % 130}
                r={1.8 + (idx % 3) * 0.8}
              />
            ))}
          </g>

          {/* Tectonic Fault Line with Seismic Stress Indicators */}
          <g filter="url(#faultWarningGlow)">
            <path
              d="M 380 340 L 440 430 L 490 530"
              fill="none"
              stroke="#ef4444"
              strokeWidth="3.5"
              strokeDasharray="10 5"
              opacity={seismicPulse}
            />
            {/* Stress Arrow Callout */}
            <polygon points="430,410 415,405 425,420" fill="#ef4444" />
            <polygon points="450,450 465,455 455,440" fill="#ef4444" />
          </g>

          {/* ---------------------------------------------------- */}
          {/* LAYER 3: SUBTERRANEAN AQUIFER / CAVERN CHAMBER (-300m) */}
          {/* ---------------------------------------------------- */}
          {/* Organic Cavern Chamber Hollow */}
          <path
            d={`M 140 230 C 260 210 320 180 540 210 C 720 230 840 200 960 240 L 960 350 Q 700 ${360 + waveB} 480 345 T 0 350 L 0 250 C 60 235 90 240 140 230 Z`}
            fill="url(#aquiferWaterGrad)"
            filter="url(#waterGlowFilter)"
          />

          {/* Cavern Stalactites hanging into the subterranean water */}
          <g fill="#57534e" stroke="#292524" strokeWidth="1">
            <polygon points="210,195 220,245 228,198" />
            <polygon points="340,190 350,260 362,192" />
            <polygon points="410,192 418,235 426,194" />
            <polygon points="680,198 692,255 702,200" />
            <polygon points="760,202 770,240 778,204" />
          </g>

          {/* Animated Water Current Vector Lines */}
          <g opacity="0.85">
            <line
              x1={(waterFlow * 3.2) % 960}
              y1="270"
              x2={((waterFlow * 3.2) % 960) + 90}
              y2="270"
              stroke="#ffffff"
              strokeWidth="3"
              strokeDasharray="12 8"
            />
            <line
              x1={((waterFlow * 2.8 + 200) % 960)}
              y1="310"
              x2={(((waterFlow * 2.8 + 200) % 960)) + 120}
              y2="310"
              stroke="#00f5ff"
              strokeWidth="2.5"
              strokeDasharray="16 10"
            />
          </g>

          {/* Bioluminescent Micro-Bubbles floating up */}
          {[...Array(14)].map((_, idx) => {
            const bx = (idx * 73 + frame * 0.8) % 920 + 20;
            const by = 330 - ((idx * 27 + bubbleY * 1.5) % 110);
            return (
              <circle
                key={`bubble-${idx}`}
                cx={bx}
                cy={by}
                r={2 + (idx % 3)}
                fill="#ffffff"
                opacity="0.75"
              />
            );
          })}

          {/* ---------------------------------------------------- */}
          {/* LAYER 2: KARST LIMESTONE & SEDIMENTARY CRUST */}
          {/* ---------------------------------------------------- */}
          <path
            d={`M 0 110 Q 240 ${95 + waveA} 480 120 T 960 ${105 - waveA} L 960 230 C 840 200 720 230 540 210 C 320 180 260 210 140 230 C 90 240 60 235 0 250 Z`}
            fill="url(#karstSedimentGrad)"
            stroke="#78716c"
            strokeWidth="1.5"
          />

          {/* Soil Speckles */}
          <g opacity="0.35" fill="#fde047">
            {[...Array(20)].map((_, idx) => (
              <circle
                key={`soil-${idx}`}
                cx={(idx * 47) % 940 + 10}
                cy={130 + (idx * 17) % 80}
                r={1.5 + (idx % 2)}
              />
            ))}
          </g>

          {/* ---------------------------------------------------- */}
          {/* LAYER 1: TOP SURFACE & FLORA CANOPY (0 m) */}
          {/* ---------------------------------------------------- */}
          <path
            d={`M 0 110 Q 240 ${95 + waveA} 480 120 T 960 ${105 - waveA} L 960 135 Q 720 130 480 135 T 0 130 Z`}
            fill="url(#surfaceFloraGrad)"
          />

          {/* Surface Tree Canopy Clumps / Mountain Ridge along surface */}
          <g fill="#166534" opacity="0.9">
            {[...Array(24)].map((_, idx) => {
              const tx = idx * 40 + 10;
              const ty = 105 + Math.sin(idx * 0.7) * 8;
              return (
                <circle
                  key={`tree-${idx}`}
                  cx={tx}
                  cy={ty}
                  r={8 + (idx % 4) * 2}
                />
              );
            })}
          </g>

          {/* ---------------------------------------------------- */}
          {/* DEPTH SCALE RULER (SCIENTIFIC METRIC AXIS) */}
          {/* ---------------------------------------------------- */}
          <g transform="translate(35, 45)" opacity="0.95">
            {/* Vertical Ruler Line */}
            <line x1="0" y1="60" x2="0" y2="520" stroke="#ffffff" strokeWidth="2" strokeDasharray="4 4" />

            {/* Depth Markers */}
            <g transform="translate(14, 65)">
              <polygon points="-14,0 -6,-4 -6,4" fill="#ffffff" />
              <text fill="#ffffff" fontSize="13" fontWeight="900" letterSpacing="1">
                0 m (SUPERFICIE & BIOMA)
              </text>
            </g>

            <g transform="translate(14, 150)">
              <polygon points="-14,0 -6,-4 -6,4" fill="#fde047" />
              <text fill="#fde047" fontSize="13" fontWeight="900" letterSpacing="1">
                -120 m (ESTRATO CÁRSTICO / LIMO)
              </text>
            </g>

            <g transform="translate(14, 270)">
              <polygon points="-14,0 -6,-4 -6,4" fill="#00f5ff" />
              <text fill="#00f5ff" fontSize="14" fontWeight="900" letterSpacing="1">
                -450 m (ACUÍFERO SUBTERRÁNEO MASIVO)
              </text>
            </g>

            <g transform="translate(14, 410)">
              <polygon points="-14,0 -6,-4 -6,4" fill="#cbd5e1" />
              <text fill="#cbd5e1" fontSize="13" fontWeight="900" letterSpacing="1">
                -2.200 m (ROCA MADRE & FALLA SÍSMICA)
              </text>
            </g>

            <g transform="translate(14, 510)">
              <polygon points="-14,0 -6,-4 -6,4" fill="#f97316" />
              <text fill="#f97316" fontSize="13" fontWeight="900" letterSpacing="1">
                -4.500 m (PRESIÓN TÉRMICA & MAGMA)
              </text>
            </g>
          </g>
        </svg>

        {/* Telemetry Alert Status Badge */}
        <div
          style={{
            position: 'absolute',
            top: 20,
            right: 20,
            padding: '12px 18px',
            backgroundColor: 'rgba(2, 9, 22, 0.90)',
            border: `1.5px solid ${accentColor}80`,
            borderRadius: 14,
            backdropFilter: 'blur(12px)',
            boxShadow: `0 0 25px ${accentColor}30`,
            display: 'flex',
            flexDirection: 'column',
            gap: 4,
          }}
        >
          <div style={{ color: accentColor, fontSize: 13, fontWeight: 900, letterSpacing: 1.5 }}>
            TELEMETRÍA // ANOMALÍA ACTIVA
          </div>
          <div style={{ color: '#ffffff', fontSize: 18, fontWeight: 900 }}>
            {scene.metricLabel || 'PRESIÓN ESTRUCTURAL'}:{' '}
            <span style={{ color: primaryColor }}>{scene.metricValA || 'CRÍTICA'}</span>
          </div>
        </div>
      </div>
    </div>
  );
};