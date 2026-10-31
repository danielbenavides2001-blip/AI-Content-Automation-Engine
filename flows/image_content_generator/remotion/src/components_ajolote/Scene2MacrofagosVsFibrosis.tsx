import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderAjolote } from './HeaderAjolote';

export const Scene2MacrofagosVsFibrosis: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 90 },
  });

  // Animated macrophage pseudopods breathing/phagocytosis
  const pulse = Math.sin(frame * 0.1) * 6;
  const sweep = (frame * 1.5) % 300;

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
      <HeaderAjolote
        category="MACRÓFAGOS VS"
        categoryHighlight="CICATRIZ"
        bigMetric="FAGOCITOSIS"
        metricSubtitle="limpieza activa de restos · sin macrófagos no hay regeneración"
        badgeText="EXPERIMENTO CLAVE"
        badgeColor="#10b981"
      />

      {/* Main Framed Stage */}
      <div
        style={{
          position: 'absolute',
          top: 365,
          left: 60,
          right: 60,
          height: 1000,
          border: '1.5px solid rgba(255, 255, 255, 0.15)',
          backgroundColor: 'rgba(11, 14, 20, 0.92)',
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
        <div
          style={{
            alignSelf: 'flex-start',
            color: '#10b981',
            fontFamily: 'Consolas, monospace',
            fontSize: 16,
            letterSpacing: 2,
            display: 'flex',
            gap: 15,
          }}
        >
          <span>CONTROL INMUNOLÓGICO</span>
          <span style={{ color: '#64748b' }}>|</span>
          <span style={{ color: '#f43f5e' }}>RESPUESTA A DEPLECIÓN CELULAR</span>
        </div>

        {/* Split Comparison Stage */}
        <div style={{ width: '100%', height: 780, position: 'relative' }}>
          <svg width="100%" height="100%" viewBox="0 0 900 780">
            <defs>
              <linearGradient id="macroGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#34d399" />
                <stop offset="100%" stopColor="#059669" />
              </linearGradient>

              <linearGradient id="scarGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#f43f5e" />
                <stop offset="100%" stopColor="#881337" />
              </linearGradient>
            </defs>

            {/* Split Divider */}
            <line x1="450" y1="40" x2="450" y2="700" stroke="rgba(255,255,255,0.2)" strokeWidth="2" strokeDasharray="6 6" />

            {/* ======================================= */}
            {/* LEFT PANEL: CON MACRÓFAGOS (REGENERACIÓN) */}
            {/* ======================================= */}
            <g transform={`scale(${entrance})`} style={{ transformOrigin: '225px 380px' }}>
              {/* Outer Glow Card */}
              <rect
                x="30"
                y="50"
                width="390"
                height="620"
                rx="14"
                fill="rgba(16, 185, 129, 0.05)"
                stroke="#10b981"
                strokeWidth="2"
              />

              {/* Title Badge */}
              <rect x="50" y="70" width="350" height="42" rx="6" fill="rgba(16, 185, 129, 0.2)" />
              <text x="225" y="98" fill="#10b981" fontFamily="Bahnschrift, sans-serif" fontSize="20" fontWeight="bold" textAnchor="middle">
                CON MACRÓFAGOS (NATURAL)
              </text>

              {/* Cellular Microscope Circle */}
              <circle cx="225" cy="270" r="140" fill="rgba(6, 78, 59, 0.3)" stroke="#10b981" strokeWidth="1.5" />

              {/* Amoeboid Macrophage 1 */}
              <g transform="translate(195, 240)">
                <path
                  d={`M 0 ${pulse} Q 35 ${-20 - pulse} 65 5 Q 85 ${45 + pulse} 50 75 Q 15 90 -15 65 Q ${-35 - pulse} 25 0 ${pulse} Z`}
                  fill="url(#macroGrad)"
                  stroke="#6ee7b7"
                  strokeWidth="2.5"
                  opacity="0.9"
                />
                <circle cx="25" cy="35" r="14" fill="#064e3b" opacity="0.8" />
                <circle cx="28" cy="33" r="5" fill="#34d399" />
              </g>

              {/* Amoeboid Macrophage 2 (Smaller sweeper) */}
              <g transform="translate(270, 310)">
                <path
                  d="M 0 0 Q 25 -15 45 5 Q 55 35 30 50 Q 5 60 -15 40 Q -25 15 0 0 Z"
                  fill="url(#macroGrad)"
                  stroke="#6ee7b7"
                  strokeWidth="2"
                  opacity="0.85"
                />
                <circle cx="15" cy="22" r="8" fill="#064e3b" opacity="0.8" />
              </g>

              {/* Debris particles being engulfed */}
              {[-30, 20, 60, -50].map((dx, i) => (
                <circle
                  key={i}
                  cx={180 + dx + Math.sin(frame * 0.05 + i) * 15}
                  cy={280 + (i * 25) - Math.cos(frame * 0.05 + i) * 10}
                  r="4"
                  fill="#94a3b8"
                  opacity={0.5}
                />
              ))}

              {/* Floating label for Phagocytosis */}
              <text x="225" y="440" fill="#34d399" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold" textAnchor="middle">
                FAGOCITOSIS DE DESECHOS
              </text>
              <text x="225" y="465" fill="#94a3b8" fontFamily="Consolas, monospace" fontSize="13" textAnchor="middle">
                Degrada detritos sin liberar TGF-β
              </text>

              {/* Result Chip */}
              <g transform="translate(60, 520)">
                <rect width="330" height="120" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#10b981" strokeWidth="1.5" />
                <text x="16" y="32" fill="#10b981" fontFamily="Consolas, monospace" fontSize="14" fontWeight="bold">RESULTADO:</text>
                <text x="16" y="62" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="22" fontWeight="bold">
                  REVERSIÓN A BLASTEMA
                </text>
                <text x="16" y="92" fill="#34d399" fontFamily="Bahnschrift, sans-serif" fontSize="16">
                  ✓ Formación de pata completa (100%)
                </text>
              </g>
            </g>

            {/* ======================================= */}
            {/* RIGHT PANEL: SIN MACRÓFAGOS (FIBROSIS)  */}
            {/* ======================================= */}
            <g transform={`scale(${entrance})`} style={{ transformOrigin: '675px 380px' }}>
              {/* Outer Glow Card */}
              <rect
                x="480"
                y="50"
                width="390"
                height="620"
                rx="14"
                fill="rgba(244, 63, 94, 0.05)"
                stroke="#f43f5e"
                strokeWidth="2"
              />

              {/* Title Badge */}
              <rect x="500" y="70" width="350" height="42" rx="6" fill="rgba(244, 63, 94, 0.2)" />
              <text x="675" y="98" fill="#f43f5e" fontFamily="Bahnschrift, sans-serif" fontSize="20" fontWeight="bold" textAnchor="middle">
                BLOQUEO (MODELO HUMANO)
              </text>

              {/* Microscope Circle */}
              <circle cx="675" cy="270" r="140" fill="rgba(136, 19, 55, 0.3)" stroke="#f43f5e" strokeWidth="1.5" />

              {/* Tangled Collagen Scar Matrix */}
              <g transform="translate(565, 160)">
                {/* Thick collagen bands */}
                {[0, 30, 60, 90, 120, 150, 180].map((offset, i) => (
                  <path
                    key={i}
                    d={`M 15 ${offset} C 60 ${offset + 20} 140 ${offset - 20} 205 ${offset}`}
                    stroke="#f43f5e"
                    strokeWidth="4"
                    fill="none"
                    opacity="0.8"
                  />
                ))}
                {/* Cross fibers */}
                {[20, 55, 90, 125, 160, 195].map((cx, i) => (
                  <line
                    key={i}
                    x1={cx}
                    y1="10"
                    x2={cx + 20}
                    y2="210"
                    stroke="#fb7185"
                    strokeWidth="3"
                    strokeDasharray="4 2"
                    opacity="0.75"
                  />
                ))}

                {/* Dense Scar Plug Center */}
                <ellipse cx="110" cy="110" rx="65" ry="35" fill="url(#scarGrad)" opacity="0.9" stroke="#fda4af" strokeWidth="2" />
                <text x="110" y="117" fill="#ffffff" fontFamily="Consolas, monospace" fontSize="15" fontWeight="bold" textAnchor="middle">
                  COSTRA FIBROSA
                </text>
              </g>

              {/* Floating label */}
              <text x="675" y="440" fill="#fb7185" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold" textAnchor="middle">
                CICATRIZ DE COLÁGENO DENSO
              </text>
              <text x="675" y="465" fill="#94a3b8" fontFamily="Consolas, monospace" fontSize="13" textAnchor="middle">
                Bloquea señales regenerativas
              </text>

              {/* Result Chip */}
              <g transform="translate(510, 520)">
                <rect width="330" height="120" rx="10" fill="rgba(15, 23, 42, 0.9)" stroke="#f43f5e" strokeWidth="1.5" />
                <text x="16" y="32" fill="#f43f5e" fontFamily="Consolas, monospace" fontSize="14" fontWeight="bold">RESULTADO:</text>
                <text x="16" y="62" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="22" fontWeight="bold">
                  CICATRIZACIÓN PERMANENTE
                </text>
                <text x="16" y="92" fill="#f87171" fontFamily="Bahnschrift, sans-serif" fontSize="16">
                  ✗ La pata no vuelve a crecer jamás
                </text>
              </g>
            </g>
          </svg>
        </div>

        {/* Bottom Status Chip */}
        <div
          style={{
            backgroundColor: 'rgba(20, 26, 36, 0.95)',
            border: '1.5px solid #10b981',
            borderRadius: 10,
            padding: '12px 30px',
            fontFamily: 'Consolas, monospace',
            fontSize: 20,
            fontWeight: 800,
            color: '#10b981',
            letterSpacing: 2,
          }}
        >
          SIN MACRÓFAGOS, EL AJOLOTE CICATRIZA EXACTAMENTE IGUAL QUE UN HUMANO
        </div>
      </div>
    </div>
  );
};
