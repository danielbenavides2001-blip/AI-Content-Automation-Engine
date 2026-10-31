import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderAjolote } from './HeaderAjolote';

export const Scene5DedosHumanosPoll: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 90 },
  });

  const barAnim = spring({
    frame: frame - 25,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  const pollPulse = Math.sin(frame * 0.1) * 3;

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
        category="MISTERIO EN"
        categoryHighlight="HUMANOS"
        bigMetric="LECHO UNGUEAL"
        metricSubtitle="células de la uña en niños · regeneración real de falange"
        badgeText="DEBATE CIENTÍFICO"
        badgeColor="#f59e0b"
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
            color: '#f59e0b',
            fontFamily: 'Consolas, monospace',
            fontSize: 16,
            letterSpacing: 2,
            display: 'flex',
            gap: 15,
          }}
        >
          <span>LÍMITE REGENERATIVO HUMANO</span>
          <span style={{ color: '#64748b' }}>|</span>
          <span style={{ color: '#ec4899' }}>SONDEO COMUNITARIO</span>
        </div>

        {/* Stage Content */}
        <div style={{ width: '100%', height: 780, position: 'relative' }}>
          <svg width="100%" height="100%" viewBox="0 0 900 780">
            <defs>
              <linearGradient id="barYesGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#10b981" />
                <stop offset="100%" stopColor="#34d399" />
              </linearGradient>

              <linearGradient id="barNoGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#ef4444" />
                <stop offset="100%" stopColor="#f87171" />
              </linearGradient>
            </defs>

            <g transform={`scale(${entrance})`} style={{ transformOrigin: '450px 380px' }}>
              {/* ======================================================= */}
              {/* UPPER SECTION: HUMAN FINGERTIP REGENERATION ANATOMY     */}
              {/* ======================================================= */}
              <g transform="translate(40, 30)">
                <rect width="820" height="280" rx="12" fill="rgba(245, 158, 11, 0.05)" stroke="#f59e0b" strokeWidth="1.5" />

                <text x="24" y="36" fill="#f59e0b" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold">
                  EVIDENCIA CLÍNICA: PUNTA DE DEDO EN NIÑOS PEQUEÑOS
                </text>

                {/* Finger Anatomical Illustration */}
                <g transform="translate(40, 65)">
                  {/* Finger Flesh */}
                  <path
                    d="M 30 50 L 320 50 C 370 50 390 80 390 100 C 390 120 370 150 320 150 L 30 150 Z"
                    fill="rgba(251, 207, 232, 0.25)"
                    stroke="#f472b6"
                    strokeWidth="2"
                  />

                  {/* Distal Phalanx Bone */}
                  <path
                    d="M 60 85 L 280 85 C 310 85 330 95 330 100 C 330 105 310 115 280 115 L 60 115 Z"
                    fill="#f1f5f9"
                    stroke="#94a3b8"
                    strokeWidth="2"
                  />
                  <text x="90" y="105" fill="#475569" fontFamily="Consolas, monospace" fontSize="13">FALANGE DISTAL</text>

                  {/* Nail Plate (Top) */}
                  <path
                    d="M 230 46 L 360 46 C 370 46 375 52 375 60 L 230 60 Z"
                    fill="#fed7aa"
                    stroke="#f97316"
                    strokeWidth="2"
                  />
                  <text x="260" y="40" fill="#f97316" fontFamily="Consolas, monospace" fontSize="12" fontWeight="bold">UÑA</text>

                  {/* Cut Boundary 1: Subungual (Regenerates!) */}
                  <line x1="335" y1="20" x2="335" y2="175" stroke="#10b981" strokeWidth="3" strokeDasharray="4 3" />
                  <g transform="translate(345, 18)">
                    <rect width="170" height="42" rx="6" fill="rgba(6, 78, 59, 0.9)" stroke="#10b981" strokeWidth="1.5" />
                    <text x="10" y="18" fill="#34d399" fontFamily="Consolas, monospace" fontSize="11" fontWeight="bold">CORTE A NIVEL UÑA</text>
                    <text x="10" y="34" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="13" fontWeight="bold">✓ VUELVE A CRECER</text>
                  </g>

                  {/* Cut Boundary 2: Proximal (Scars!) */}
                  <line x1="190" y1="20" x2="190" y2="175" stroke="#ef4444" strokeWidth="3" strokeDasharray="4 3" />
                  <g transform="translate(85, 18)">
                    <rect width="180" height="42" rx="6" fill="rgba(127, 29, 29, 0.9)" stroke="#ef4444" strokeWidth="1.5" />
                    <text x="10" y="18" fill="#fca5a5" fontFamily="Consolas, monospace" fontSize="11" fontWeight="bold">CORTE MÁS ARRIBA</text>
                    <text x="10" y="34" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="13" fontWeight="bold">✗ SOLO CICATRIZ</text>
                  </g>
                </g>

                {/* Subtext info */}
                <text x="40" y="255" fill="#94a3b8" fontFamily="Consolas, monospace" fontSize="13">
                  Las células madre de la matriz de la uña (Wnt) envían la señal embrionaria. Sin esa señal, gana la fibrosis.
                </text>
              </g>

              {/* ======================================================= */}
              {/* LOWER SECTION: INTERACTIVE COMMUNITY POLL CARD          */}
              {/* ======================================================= */}
              <g transform="translate(40, 345)">
                <rect width="820" height="360" rx="14" fill="rgba(15, 23, 42, 0.95)" stroke="#38bdf8" strokeWidth="2" />

                {/* Question Header */}
                <rect x="25" y="25" width="770" height="60" rx="8" fill="rgba(56, 189, 248, 0.15)" />
                <text x="410" y="62" fill="#ffffff" fontFamily="Bahnschrift, Arial, sans-serif" fontSize="23" fontWeight="bold" textAnchor="middle">
                  ¿LOGRAREMOS REGENERAR EXTREMIDADES EN HUMANOS?
                </text>

                {/* Option 1: SÍ */}
                <g transform="translate(45, 115)">
                  <rect width="730" height="85" rx="10" fill="rgba(16, 185, 129, 0.1)" stroke="#10b981" strokeWidth="1.5" />

                  {/* Progress Bar Fill */}
                  <rect
                    x="10"
                    y="10"
                    width={Math.min(710, 710 * 0.74 * Math.max(0, barAnim))}
                    height="65"
                    rx="8"
                    fill="url(#barYesGrad)"
                    opacity="0.35"
                  />

                  {/* Option Label */}
                  <text x="30" y="50" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="24" fontWeight="bold">
                    SÍ, CON BIOMEDICINA Y GENÉTICA
                  </text>

                  {/* Percentage */}
                  <text x="700" y="52" fill="#34d399" fontFamily="Bahnschrift, sans-serif" fontSize="32" fontWeight="900" textAnchor="end">
                    74%
                  </text>
                </g>

                {/* Option 2: NO */}
                <g transform="translate(45, 220)">
                  <rect width="730" height="85" rx="10" fill="rgba(239, 68, 68, 0.1)" stroke="#ef4444" strokeWidth="1.5" />

                  {/* Progress Bar Fill */}
                  <rect
                    x="10"
                    y="10"
                    width={Math.min(710, 710 * 0.26 * Math.max(0, barAnim))}
                    height="65"
                    rx="8"
                    fill="url(#barNoGrad)"
                    opacity="0.35"
                  />

                  {/* Option Label */}
                  <text x="30" y="50" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="24" fontWeight="bold">
                    NO, LA CICATRIZ ES INEVITABLE
                  </text>

                  {/* Percentage */}
                  <text x="700" y="52" fill="#f87171" fontFamily="Bahnschrift, sans-serif" fontSize="32" fontWeight="900" textAnchor="end">
                    26%
                  </text>
                </g>

                {/* Micro CTA */}
                <text x="410" y="335" fill="#38bdf8" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold" textAnchor="middle">
                  👉 COMENTA "SÍ" O "NO" EN LOS COMENTARIOS 👈
                </text>
              </g>
            </g>
          </svg>
        </div>

        {/* Bottom Status Chip */}
        <div
          style={{
            backgroundColor: 'rgba(20, 26, 36, 0.95)',
            border: '1.5px solid #f59e0b',
            borderRadius: 10,
            padding: '12px 30px',
            fontFamily: 'Consolas, monospace',
            fontSize: 20,
            fontWeight: 800,
            color: '#f59e0b',
            letterSpacing: 2,
          }}
        >
          COMENTA TU OPINIÓN SIN LEER LAS RESPUESTAS DE LOS DEMÁS
        </div>
      </div>
    </div>
  );
};
