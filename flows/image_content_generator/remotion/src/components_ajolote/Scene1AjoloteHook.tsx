import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderAjolote } from './HeaderAjolote';

export const Scene1AjoloteHook: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 90 },
  });

  // Gentle swimming oscillation
  const sway = Math.sin(frame * 0.04) * 8;
  const gillWave1 = Math.sin(frame * 0.08) * 4;
  const gillWave2 = Math.sin(frame * 0.08 + 1) * 4;
  const gillWave3 = Math.sin(frame * 0.08 + 2) * 4;

  // Wound closure animation
  const skinMigration = interpolate(frame, [35, 110], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
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
      <HeaderAjolote
        category="EL MILAGRO DEL"
        categoryHighlight="AJOLOTE"
        bigMetric="0 COSTRA"
        metricSubtitle="cierre epidérmico en horas · Xochimilco, México"
        badgeText="FENÓMENO ÚNICO"
        badgeColor="#ec4899"
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
            color: '#ec4899',
            fontFamily: 'Consolas, monospace',
            fontSize: 16,
            letterSpacing: 2,
            display: 'flex',
            gap: 15,
          }}
        >
          <span>AMBYSTOMA MEXICANUM</span>
          <span style={{ color: '#64748b' }}>|</span>
          <span style={{ color: '#38bdf8' }}>EPITELIO DE HERIDA ACTIVO</span>
        </div>

        {/* Axolotl Vector Stage */}
        <div style={{ width: '100%', height: 750, position: 'relative' }}>
          <svg width="100%" height="100%" viewBox="0 0 900 750">
            <defs>
              <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#f472b6" />
                <stop offset="50%" stopColor="#fb7185" />
                <stop offset="100%" stopColor="#f43f5e" />
              </linearGradient>

              <linearGradient id="tailGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="#fbcfe8" stopOpacity="0.85" />
                <stop offset="100%" stopColor="#f43f5e" stopOpacity="0.1" />
              </linearGradient>

              <radialGradient id="gillGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#fda4af" />
                <stop offset="100%" stopColor="#e11d48" />
              </radialGradient>
            </defs>

            {/* Overall animated transform - scaled larger for prominent presence */}
            <g transform={`translate(${450 + sway}, 300) scale(${entrance * 1.45})`}>
              {/* Caudal swimming fin */}
              <path
                d="M -35 120 Q -45 280 0 350 Q 45 280 35 120 Z"
                fill="url(#tailGrad)"
                stroke="#fda4af"
                strokeWidth="1.5"
              />

              {/* Hind Limbs */}
              <g transform="translate(-55, 140)">
                <path d="M 0 0 Q -45 20 -60 55 Q -40 65 -25 35" fill="#f472b6" stroke="#db2777" strokeWidth="2" />
                <circle cx="-60" cy="55" r="4" fill="#fda4af" />
                <circle cx="-55" cy="62" r="3" fill="#fda4af" />
                <circle cx="-67" cy="58" r="3" fill="#fda4af" />
              </g>

              <g transform="translate(55, 140)">
                <path d="M 0 0 Q 45 20 60 55 Q 40 65 25 35" fill="#f472b6" stroke="#db2777" strokeWidth="2" />
                <circle cx="60" cy="55" r="4" fill="#fda4af" />
                <circle cx="55" cy="62" r="3" fill="#fda4af" />
                <circle cx="67" cy="58" r="3" fill="#fda4af" />
              </g>

              {/* Left Front Limb (Intact) */}
              <g transform="translate(-65, -30)">
                <path d="M 0 0 Q -50 -10 -85 20 Q -65 35 -30 15" fill="#f472b6" stroke="#db2777" strokeWidth="2" />
                <circle cx="-85" cy="20" r="4" fill="#fda4af" />
                <circle cx="-92" cy="18" r="3" fill="#fda4af" />
                <circle cx="-85" cy="27" r="3" fill="#fda4af" />
                <circle cx="-77" cy="28" r="3" fill="#fda4af" />
              </g>

              {/* Right Front Limb: AMPUTATION & SKIN MIGRATION FOCUS */}
              <g transform="translate(65, -30)">
                {/* Stump base */}
                <path d="M 0 0 Q 25 -5 40 5 Q 35 20 0 15" fill="#f472b6" stroke="#db2777" strokeWidth="2" />

                {/* Amputation cut line */}
                <line x1="40" y1="2" x2="35" y2="20" stroke="#f43f5e" strokeWidth="3" strokeDasharray="3 3" />

                {/* Sliding epidermal skin flap */}
                <path
                  d={`M 35 2 Q ${40 + 10 * skinMigration} 11 35 20`}
                  stroke="#38bdf8"
                  strokeWidth={3 + 2 * skinMigration}
                  fill="rgba(56, 189, 248, 0.4)"
                />

                {/* Pulsing indicator tag */}
                <g transform="translate(65, -15)">
                  <rect x="0" y="0" width="160" height="46" rx="6" fill="rgba(15, 23, 42, 0.95)" stroke="#38bdf8" strokeWidth="1.5" />
                  <text x="12" y="19" fill="#38bdf8" fontFamily="Consolas, monospace" fontSize="12" fontWeight="bold">
                    SELLO EPIDÉRMICO
                  </text>
                  <text x="12" y="37" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="14" fontWeight="bold">
                    SIN COSTRA ({Math.round(skinMigration * 100)}%)
                  </text>
                </g>
              </g>

              {/* Main Body Torso */}
              <path
                d="M -50 -100 Q -65 0 -45 130 Q 0 170 45 130 Q 65 0 50 -100 Q 0 -130 -50 -100 Z"
                fill="url(#bodyGrad)"
                stroke="#db2777"
                strokeWidth="2.5"
              />

              {/* Coastal Grooves (Rib-like skin ridges) */}
              {[-50, -25, 0, 25, 50, 75, 100].map((y, idx) => (
                <path
                  key={idx}
                  d={`M -38 ${y} Q 0 ${y + 6} 38 ${y}`}
                  stroke="rgba(219, 39, 119, 0.4)"
                  strokeWidth="2"
                  fill="none"
                />
              ))}

              {/* Axolotl Head */}
              <ellipse cx="0" cy="-145" rx="80" ry="70" fill="url(#bodyGrad)" stroke="#db2777" strokeWidth="2.5" />

              {/* Nostrils */}
              <circle cx="-15" cy="-185" r="2.5" fill="#9d174d" />
              <circle cx="15" cy="-185" r="2.5" fill="#9d174d" />

              {/* Cute dark bead eyes */}
              <circle cx="-42" cy="-155" r="9" fill="#09090b" stroke="#db2777" strokeWidth="1" />
              <circle cx="-39" cy="-158" r="3" fill="#ffffff" />
              <circle cx="42" cy="-155" r="9" fill="#09090b" stroke="#db2777" strokeWidth="1" />
              <circle cx="45" cy="-158" r="3" fill="#ffffff" />

              {/* External Gills (Left side 3 rami) */}
              <g transform="translate(-65, -155)">
                {/* Branch 1 */}
                <path d={`M 0 0 Q -40 ${-20 + gillWave1} -95 -25`} stroke="url(#gillGlow)" strokeWidth="6" strokeLinecap="round" fill="none" />
                {[-15, -35, -55, -75].map((gx, gi) => (
                  <path key={gi} d={`M ${gx} ${gx * 0.25} L ${gx - 6} ${gx * 0.25 - 12}`} stroke="#e11d48" strokeWidth="2" strokeLinecap="round" />
                ))}

                {/* Branch 2 */}
                <path d={`M 0 10 Q -45 ${15 + gillWave2} -105 10`} stroke="url(#gillGlow)" strokeWidth="6" strokeLinecap="round" fill="none" />
                {[-20, -45, -70, -90].map((gx, gi) => (
                  <path key={gi} d={`M ${gx} 10 L ${gx - 6} 22`} stroke="#e11d48" strokeWidth="2" strokeLinecap="round" />
                ))}

                {/* Branch 3 */}
                <path d={`M 0 20 Q -40 ${45 + gillWave3} -90 55`} stroke="url(#gillGlow)" strokeWidth="6" strokeLinecap="round" fill="none" />
                {[-15, -40, -65].map((gx, gi) => (
                  <path key={gi} d={`M ${gx} ${gx * -0.5 + 20} L ${gx - 6} ${gx * -0.5 + 32}`} stroke="#e11d48" strokeWidth="2" strokeLinecap="round" />
                ))}
              </g>

              {/* External Gills (Right side 3 rami) */}
              <g transform="translate(65, -155)">
                {/* Branch 1 */}
                <path d={`M 0 0 Q 40 ${-20 + gillWave1} 95 -25`} stroke="url(#gillGlow)" strokeWidth="6" strokeLinecap="round" fill="none" />
                {[15, 35, 55, 75].map((gx, gi) => (
                  <path key={gi} d={`M ${gx} ${gx * -0.25} L ${gx + 6} ${gx * -0.25 - 12}`} stroke="#e11d48" strokeWidth="2" strokeLinecap="round" />
                ))}

                {/* Branch 2 */}
                <path d={`M 0 10 Q 45 ${15 + gillWave2} 105 10`} stroke="url(#gillGlow)" strokeWidth="6" strokeLinecap="round" fill="none" />
                {[20, 45, 70, 90].map((gx, gi) => (
                  <path key={gi} d={`M ${gx} 10 L ${gx + 6} 22`} stroke="#e11d48" strokeWidth="2" strokeLinecap="round" />
                ))}

                {/* Branch 3 */}
                <path d={`M 0 20 Q 40 ${45 + gillWave3} 90 55`} stroke="url(#gillGlow)" strokeWidth="6" strokeLinecap="round" fill="none" />
                {[15, 40, 65].map((gx, gi) => (
                  <path key={gi} d={`M ${gx} ${gx * 0.5 + 20} L ${gx + 6} ${gx * 0.5 + 32}`} stroke="#e11d48" strokeWidth="2" strokeLinecap="round" />
                ))}
              </g>
            </g>

            {/* Left Data Overlay Card */}
            <g transform="translate(35, 615)">
              <rect width="255" height="90" rx="8" fill="rgba(15, 23, 42, 0.9)" stroke="#ec4899" strokeWidth="1.5" />
              <text x="16" y="28" fill="#fda4af" fontFamily="Consolas, monospace" fontSize="13">ORIGEN EVOLUTIVO</text>
              <text x="16" y="52" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="18" fontWeight="bold">XOCHIMILCO · CDMX</text>
              <text x="16" y="75" fill="#94a3b8" fontFamily="Consolas, monospace" fontSize="12">Neotenia: conserva branquias</text>
            </g>

            {/* Right Data Overlay Card */}
            <g transform="translate(610, 615)">
              <rect width="255" height="90" rx="8" fill="rgba(15, 23, 42, 0.9)" stroke="#38bdf8" strokeWidth="1.5" />
              <text x="16" y="28" fill="#38bdf8" fontFamily="Consolas, monospace" fontSize="13">SELLADO TISULAR</text>
              <text x="16" y="52" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="18" fontWeight="bold">CERO COAGULACIÓN</text>
              <text x="16" y="75" fill="#94a3b8" fontFamily="Consolas, monospace" fontSize="12">Células basales forman AEC</text>
            </g>
          </svg>
        </div>

        {/* Bottom Status Chip */}
        <div
          style={{
            backgroundColor: 'rgba(20, 26, 36, 0.95)',
            border: '1.5px solid #ec4899',
            borderRadius: 10,
            padding: '12px 30px',
            fontFamily: 'Consolas, monospace',
            fontSize: 20,
            fontWeight: 800,
            color: '#ec4899',
            letterSpacing: 2,
          }}
        >
          LA PIEL SE DESLIZA Y PROTEGE EL MUÑÓN EN MENOS DE 24 HORAS
        </div>
      </div>
    </div>
  );
};
