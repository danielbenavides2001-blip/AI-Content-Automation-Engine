import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderAjolote } from './HeaderAjolote';

export const Scene4MemoriaYAcidoRetinoico: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 90 },
  });

  // Glowing green pulse for GFP lineage tracing
  const gfpGlow = Math.sin(frame * 0.12) * 4 + 8;

  // Coordinate slider indicator moving along the limb axis
  const coordScan = (frame * 2.5) % 450;

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
        category="MEMORIA"
        categoryHighlight="POSICIONAL"
        bigMetric="COORDENADAS 3D"
        metricSubtitle="el ácido retinoico programa la longitud exacta a regenerar"
        badgeText="EXPERIMENTO GFP"
        badgeColor="#22c55e"
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
            color: '#22c55e',
            fontFamily: 'Consolas, monospace',
            fontSize: 16,
            letterSpacing: 2,
            display: 'flex',
            gap: 15,
          }}
        >
          <span>LINAJE CELULAR RESTRINGIDO</span>
          <span style={{ color: '#64748b' }}>|</span>
          <span style={{ color: '#fbbf24' }}>GRADIENTE QUÍMICO PROXIMO-DISTAL</span>
        </div>

        {/* Technical Diagram Stage */}
        <div style={{ width: '100%', height: 780, position: 'relative' }}>
          <svg width="100%" height="100%" viewBox="0 0 900 780">
            <defs>
              <linearGradient id="gfpGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#4ade80" />
                <stop offset="100%" stopColor="#22c55e" />
              </linearGradient>

              <linearGradient id="gradientRuler" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#ec4899" />
                <stop offset="50%" stopColor="#a855f7" />
                <stop offset="100%" stopColor="#38bdf8" />
              </linearGradient>
            </defs>

            <g transform={`scale(${entrance})`} style={{ transformOrigin: '450px 380px' }}>
              {/* ==================================================== */}
              {/* UPPER SECTION: EXPERIMENTO GFP (TRAZADO DE LINAJE)   */}
              {/* ==================================================== */}
              <g transform="translate(40, 40)">
                <rect width="820" height="270" rx="12" fill="rgba(34, 197, 94, 0.05)" stroke="#22c55e" strokeWidth="1.5" />

                {/* Section title */}
                <text x="24" y="36" fill="#22c55e" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold">
                  TEST 1: PROTEÍNA VERDE FLUORESCENTE (GFP) EN MÚSCULO
                </text>

                {/* Left: Donor Muscle Tagged */}
                <g transform="translate(40, 70)">
                  <rect width="180" height="90" rx="8" fill="rgba(15, 23, 42, 0.85)" stroke="#64748b" strokeWidth="1" />
                  <text x="14" y="28" fill="#94a3b8" fontFamily="Consolas, monospace" fontSize="12">ORIGEN DONANTE</text>
                  <rect x="20" y="42" width="140" height="30" rx="4" fill="url(#gfpGrad)" filter={`drop-shadow(0 0 ${gfpGlow}px #22c55e)`} />
                  <text x="90" y="62" fill="#052e16" fontFamily="Bahnschrift, sans-serif" fontSize="14" fontWeight="bold" textAnchor="middle">
                    MÚSCULO GFP
                  </text>
                  <text x="90" y="125" fill="#e2e8f0" fontFamily="Consolas, monospace" fontSize="13" textAnchor="middle">
                    Solo células musculares
                  </text>
                </g>

                {/* Center Arrow */}
                <g transform="translate(260, 110)">
                  <path d="M 0 0 L 50 0 L 40 -8 M 50 0 L 40 8" stroke="#22c55e" strokeWidth="3" fill="none" strokeLinecap="round" />
                  <text x="25" y="-14" fill="#86efac" fontFamily="Consolas, monospace" fontSize="12" textAnchor="middle">
                    REGENERACIÓN
                  </text>
                </g>

                {/* Right: Regenerated Limb Cross Section */}
                <g transform="translate(360, 65)">
                  <rect width="420" height="175" rx="8" fill="rgba(15, 23, 42, 0.9)" stroke="#22c55e" strokeWidth="1.5" />
                  <text x="20" y="30" fill="#22c55e" fontFamily="Bahnschrift, sans-serif" fontSize="16" fontWeight="bold">
                    RESULTADO EN EL BRAZO NUEVO:
                  </text>

                  {/* Layer 1: Skin (NOT green) */}
                  <rect x="20" y="45" width="380" height="24" rx="4" fill="rgba(251, 207, 232, 0.2)" stroke="#f472b6" strokeWidth="1" />
                  <text x="30" y="62" fill="#fbcfe8" fontFamily="Consolas, monospace" fontSize="12">PIEL: 0% VERDE (NO GFP)</text>

                  {/* Layer 2: Muscle (100% GFP GREEN GLOW) */}
                  <rect x="20" y="78" width="380" height="34" rx="4" fill="url(#gfpGrad)" filter={`drop-shadow(0 0 ${gfpGlow}px #22c55e)`} />
                  <text x="210" y="100" fill="#052e16" fontFamily="Bahnschrift, sans-serif" fontSize="15" fontWeight="bold" textAnchor="middle">
                    MÚSCULO: 100% VERDE (RETUVO SU IDENTIDAD)
                  </text>

                  {/* Layer 3: Bone / Cartilage (NOT green) */}
                  <rect x="20" y="122" width="380" height="24" rx="4" fill="rgba(241, 245, 249, 0.15)" stroke="#cbd5e1" strokeWidth="1" />
                  <text x="30" y="139" fill="#e2e8f0" fontFamily="Consolas, monospace" fontSize="12">HUESO: 0% VERDE (NO GFP)</text>
                </g>
              </g>

              {/* ==================================================== */}
              {/* LOWER SECTION: REGLA POSICIONAL & ÁCIDO RETINOICO   */}
              {/* ==================================================== */}
              <g transform="translate(40, 340)">
                <rect width="820" height="350" rx="12" fill="rgba(251, 191, 36, 0.05)" stroke="#fbbf24" strokeWidth="1.5" />

                {/* Title */}
                <text x="24" y="36" fill="#fbbf24" fontFamily="Consolas, monospace" fontSize="16" fontWeight="bold">
                  TEST 2: MEMORIA POSICIONAL Y ÁCIDO RETINOICO (VITAMINA A)
                </text>

                {/* Coordinate Ruler Along Limb */}
                <g transform="translate(60, 80)">
                  <rect width="700" height="14" rx="7" fill="url(#gradientRuler)" />

                  {/* Ticks and Coordinates */}
                  <line x1="40" y1="20" x2="40" y2="40" stroke="#ec4899" strokeWidth="2" />
                  <text x="40" y="60" fill="#f472b6" fontFamily="Consolas, monospace" fontSize="14" textAnchor="middle">
                    HOMBRO [0.0]
                  </text>

                  <line x1="350" y1="20" x2="350" y2="40" stroke="#a855f7" strokeWidth="2" />
                  <text x="350" y="60" fill="#c084fc" fontFamily="Consolas, monospace" fontSize="14" textAnchor="middle">
                    CODO [0.5]
                  </text>

                  <line x1="660" y1="20" x2="660" y2="40" stroke="#38bdf8" strokeWidth="2" />
                  <text x="660" y="60" fill="#38bdf8" fontFamily="Consolas, monospace" fontSize="14" textAnchor="middle">
                    MUÑECA [1.0]
                  </text>

                  {/* Scanning coordinate cursor */}
                  <line x1={40 + coordScan * 1.37} y1="-10" x2={40 + coordScan * 1.37} y2="25" stroke="#ffffff" strokeWidth="3" />
                </g>

                {/* Comparison Scenarios Grid */}
                <g transform="translate(40, 165)">
                  {/* Scenario A: Normal Wrist Cut */}
                  <g transform="translate(0, 0)">
                    <rect width="350" height="135" rx="8" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" strokeWidth="1.5" />
                    <text x="16" y="28" fill="#38bdf8" fontFamily="Consolas, monospace" fontSize="13" fontWeight="bold">CORTE EN MUÑECA:</text>
                    <text x="16" y="56" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="20" fontWeight="bold">
                      REGENERA SOLO LA MANO
                    </text>
                    <text x="16" y="84" fill="#94a3b8" fontFamily="Consolas, monospace" fontSize="13">
                      ✓ Coordenada distal detectada (1.0)
                    </text>
                    <text x="16" y="108" fill="#38bdf8" fontFamily="Consolas, monospace" fontSize="13">
                      No duplica húmero ni codo
                    </text>
                  </g>

                  {/* Scenario B: With Retinoic Acid (Vitamin A) */}
                  <g transform="translate(390, 0)">
                    <rect width="350" height="135" rx="8" fill="rgba(15, 23, 42, 0.9)" stroke="#f43f5e" strokeWidth="1.5" />
                    <text x="16" y="28" fill="#f43f5e" fontFamily="Consolas, monospace" fontSize="13" fontWeight="bold">+ ÁCIDO RETINOICO (VIT. A):</text>
                    <text x="16" y="56" fill="#fb7185" fontFamily="Bahnschrift, sans-serif" fontSize="20" fontWeight="bold">
                      CRECE UN BRAZO ENTERO EXTRA
                    </text>
                    <text x="16" y="84" fill="#94a3b8" fontFamily="Consolas, monospace" fontSize="13">
                      ! La vitamina A resetea el reloj a 0.0
                    </text>
                    <text x="16" y="108" fill="#f87171" fontFamily="Consolas, monospace" fontSize="13">
                      De la muñeca brota un brazo completo
                    </text>
                  </g>
                </g>
              </g>
            </g>
          </svg>
        </div>

        {/* Bottom Status Chip */}
        <div
          style={{
            backgroundColor: 'rgba(20, 26, 36, 0.95)',
            border: '1.5px solid #22c55e',
            borderRadius: 10,
            padding: '12px 30px',
            fontFamily: 'Consolas, monospace',
            fontSize: 20,
            fontWeight: 800,
            color: '#22c55e',
            letterSpacing: 2,
          }}
        >
          EL BLASTEMA SABE CON EXACTITUD MILIMÉTRICA CUÁNTO FALTA POR CONSTRUIR
        </div>
      </div>
    </div>
  );
};
