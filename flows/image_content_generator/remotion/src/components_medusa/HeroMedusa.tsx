import React from 'react';
import { interpolate, spring } from 'remotion';

export type MedusaMorphState = 'swimming' | 'contracting' | 'cyst' | 'polyp' | 'rebirth';

interface HeroMedusaProps {
  frame: number;
  morphState: MedusaMorphState;
  stateProgress?: number; // 0.0 to 1.0 within the state
  zoom?: number;
}

export const HeroMedusa: React.FC<HeroMedusaProps> = ({
  frame,
  morphState,
  stateProgress = 0,
}) => {
  // ========================================================
  // 1. SWIMMING JET-PROPULSION KINEMATICS (PULSE CYCLE)
  // ========================================================
  // 65-frame rhythmic pulse cycle:
  // 0 - 20: contraction (jet shoot)
  // 20 - 65: relaxation & glide
  const pulseCycle = (frame % 65) / 65;
  let bellScaleX = 1.0;
  let bellScaleY = 1.0;
  let jetOffset = 0;

  if (pulseCycle < 0.3) {
    // Sharp contraction: narrows & elongates
    const p = pulseCycle / 0.3;
    bellScaleX = interpolate(p, [0, 0.6, 1], [1.02, 0.84, 0.88]);
    bellScaleY = interpolate(p, [0, 0.6, 1], [0.98, 1.16, 1.12]);
    jetOffset = Math.sin(p * Math.PI) * -38;
  } else {
    // Gradual relaxation and glide
    const p = (pulseCycle - 0.3) / 0.7;
    bellScaleX = interpolate(p, [0, 0.4, 1], [0.88, 1.05, 1.0]);
    bellScaleY = interpolate(p, [0, 0.4, 1], [1.12, 0.95, 1.0]);
    jetOffset = interpolate(p, [0, 1], [-38, 0]);
  }

  // Vertical and horizontal gentle ocean drift
  const driftY = Math.sin(frame * 0.035) * 16 + jetOffset;
  const driftX = Math.cos(frame * 0.02) * 12;

  // ========================================================
  // 2. STATE TRANSITIONS & INTERPOLATIONS
  // ========================================================
  if (morphState === 'cyst') {
    return <CystStage frame={frame} progress={stateProgress} />;
  }

  if (morphState === 'polyp') {
    return <PolypStage frame={frame} progress={stateProgress} />;
  }

  // Contract progress (0 to 1) for 'contracting' state
  const isContracting = morphState === 'contracting';
  const contractFactor = isContracting ? Math.min(1, stateProgress) : 0;

  // Rebirth size multiplier
  const isRebirth = morphState === 'rebirth';
  const rebirthScale = isRebirth ? interpolate(stateProgress, [0, 1], [0.45, 0.95]) : 1.0;

  // ========================================================
  // 3. TENTACLES DEFINITION (28 FINE ORGANIC FILAMENTS)
  // ========================================================
  const tentacleCount = 28;
  const tentacles = React.useMemo(() => {
    const list = [];
    for (let i = 0; i < tentacleCount; i++) {
      const angleDeg = (i / tentacleCount) * 180; // Arc across front margin
      const rad = (angleDeg * Math.PI) / 180;
      // Ellipse rim: rx = 210, ry = 55
      const baseX = Math.cos(rad) * 210;
      const baseY = Math.sin(rad) * 45 + 230; // Margin base
      const length = 260 + (i % 6) * 45 + (i % 4) * 25;
      const waveFreq = 0.05 + (i % 5) * 0.012;
      const phase = i * 0.45;
      const zRank = Math.sin(rad); // Depth sorting
      list.push({ baseX, baseY, length, waveFreq, phase, zRank, id: i });
    }
    return list;
  }, []);

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: 1080,
        height: 1920,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          width: 800,
          height: 1200,
          position: 'relative',
          transform: `translate(${driftX}px, ${driftY}px) scale(${rebirthScale})`,
          transformOrigin: '400px 350px',
        }}
      >
        <svg
          viewBox="-400 -250 800 1200"
          width="800"
          height="1200"
          style={{ overflow: 'visible' }}
        >
          <defs>
            {/* Bell Translucent Gradient (Turritopsis dohrnii glassmorphism) */}
            <linearGradient id="bellGlassGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#bae6fd" stopOpacity="0.45" />
              <stop offset="35%" stopColor="#7dd3fc" stopOpacity="0.25" />
              <stop offset="75%" stopColor="#38bdf8" stopOpacity="0.20" />
              <stop offset="100%" stopColor="#0284c7" stopOpacity="0.40" />
            </linearGradient>

            {/* Subumbrella Inner Glow */}
            <radialGradient id="subumbrellaGlow" cx="50%" cy="40%" r="55%">
              <stop offset="0%" stopColor="#ffffff" stopOpacity="0.40" />
              <stop offset="50%" stopColor="#38bdf8" stopOpacity="0.15" />
              <stop offset="100%" stopColor="#0284c7" stopOpacity="0" />
            </radialGradient>

            {/* Crimson/Orange Stomach (Manubrium Core) */}
            <radialGradient id="manubriumCore" cx="50%" cy="45%" r="50%">
              <stop offset="0%" stopColor="#ffedd5" stopOpacity="1" />
              <stop offset="25%" stopColor="#ff4d00" stopOpacity="0.95" />
              <stop offset="70%" stopColor="#dc2626" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#991b1b" stopOpacity="0.85" />
            </radialGradient>

            {/* Glowing Canals */}
            <filter id="canalGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>

            {/* Bell Specular Edge Glow */}
            <filter id="rimGlow" x="-30%" y="-30%" width="160%" height="160%">
              <feGaussianBlur stdDeviation="6" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* ======================================================== */}
          {/* TENTACLES: BACK LAYER */}
          {/* ======================================================== */}
          <g opacity={1 - contractFactor * 0.95}>
            {tentacles
              .filter((t) => t.zRank <= 0.3)
              .map((t) => {
                const currentLength = t.length * (1 - contractFactor * 0.9);
                const curY = t.baseY + currentLength;
                const wave1 = Math.sin(frame * t.waveFreq + t.phase) * (35 * (1 - contractFactor));
                const wave2 = Math.cos(frame * t.waveFreq * 1.3 + t.phase) * (45 * (1 - contractFactor));

                return (
                  <path
                    key={t.id}
                    d={`M ${t.baseX} ${t.baseY} Q ${t.baseX + wave1} ${t.baseY + currentLength * 0.45} ${t.baseX + wave2} ${curY}`}
                    stroke="rgba(186, 230, 253, 0.45)"
                    strokeWidth="1.8"
                    fill="none"
                    strokeLinecap="round"
                  />
                );
              })}
          </g>

          {/* ======================================================== */}
          {/* HERO BELL (TRANSFORMED BY JET PULSE OR CONTRACTION) */}
          {/* ======================================================== */}
          <g
            transform={`scale(${isContracting ? 1 - contractFactor * 0.55 : bellScaleX}, ${
              isContracting ? 1 - contractFactor * 0.55 : bellScaleY
            })`}
          >
            {/* Outer Bell Dome (Campanula) */}
            <path
              d="M -210 230 C -225 100 -200 -120 -110 -200 C -55 -250 55 -250 110 -200 C 200 -120 225 100 210 230 C 120 265 -120 265 -210 230 Z"
              fill="url(#bellGlassGrad)"
              stroke="#7dd3fc"
              strokeWidth="2.5"
              filter="url(#rimGlow)"
            />

            {/* Inner Subumbrella Cavity */}
            <path
              d="M -180 225 C -190 110 -170 -90 -95 -165 C -45 -205 45 -205 95 -165 C 170 -90 190 110 180 225 C 100 250 -100 250 -180 225 Z"
              fill="url(#subumbrellaGlow)"
              opacity="0.85"
            />

            {/* 4 Radial Canals (Hydrovascular System) */}
            <g stroke="#38bdf8" strokeWidth="3" opacity="0.75" filter="url(#canalGlow)">
              {/* Central Front Canal */}
              <path d="M 0 -190 Q -5 20 0 240" fill="none" />
              {/* Left Lateral Canal */}
              <path d="M 0 -190 Q -110 15 -140 232" fill="none" />
              {/* Right Lateral Canal */}
              <path d="M 0 -190 Q 110 15 140 232" fill="none" />
              {/* Ring Canal at Margin */}
              <ellipse cx="0" cy="235" rx="200" ry="25" fill="none" strokeWidth="2.5" />
            </g>

            {/* Specular Light Reflection (Glass Curvature Highlighting) */}
            <path
              d="M -135 -140 C -80 -190 -20 -205 5 -205 C -30 -190 -90 -160 -125 -110 Z"
              fill="#ffffff"
              opacity="0.55"
            />

            {/* ======================================================== */}
            {/* TRADEMARK: BRIGHT CRIMSON/ORANGE MANUBRIUM (STOMACH) */}
            {/* ======================================================== */}
            <g transform="translate(0, 35)">
              {/* Stomach Core Glow */}
              <circle cx="0" cy="0" r="62" fill="url(#manubriumCore)" filter="url(#canalGlow)" />

              {/* 4 Manubrium Lobes (Tetraradial Symmetry) */}
              <ellipse cx="-22" cy="-18" rx="28" ry="36" fill="url(#manubriumCore)" />
              <ellipse cx="22" cy="-18" rx="28" ry="36" fill="url(#manubriumCore)" />
              <ellipse cx="-20" cy="22" rx="26" ry="32" fill="url(#manubriumCore)" />
              <ellipse cx="20" cy="22" rx="26" ry="32" fill="url(#manubriumCore)" />

              {/* Distal Mouth / Tube (Cruciform Tip) */}
              <path
                d="M -12 45 L 0 85 L 12 45 Q 0 52 -12 45 Z"
                fill="#f97316"
                stroke="#ffedd5"
                strokeWidth="1.5"
              />

              {/* Cellular Core Energy Particles */}
              {[0, 1, 2, 3].map((idx) => {
                const angle = (idx * Math.PI) / 2 + frame * 0.04;
                const r = 24 + Math.sin(frame * 0.08 + idx) * 8;
                return (
                  <circle
                    key={idx}
                    cx={Math.cos(angle) * r}
                    cy={Math.sin(angle) * r}
                    r="4.5"
                    fill="#fef08a"
                    opacity="0.9"
                    filter="drop-shadow(0 0 6px #f59e0b)"
                  />
                );
              })}
            </g>

            {/* Velum Shelf at Margin */}
            <ellipse
              cx="0"
              cy="235"
              rx="180"
              ry="18"
              fill="rgba(56, 189, 248, 0.15)"
              stroke="#bae6fd"
              strokeWidth="1.2"
            />
          </g>

          {/* ======================================================== */}
          {/* TENTACLES: FRONT LAYER */}
          {/* ======================================================== */}
          <g opacity={1 - contractFactor * 0.95}>
            {tentacles
              .filter((t) => t.zRank > 0.3)
              .map((t) => {
                const currentLength = t.length * (1 - contractFactor * 0.9);
                const curY = t.baseY + currentLength;
                const wave1 = Math.sin(frame * t.waveFreq + t.phase) * (42 * (1 - contractFactor));
                const wave2 = Math.cos(frame * t.waveFreq * 1.2 + t.phase) * (52 * (1 - contractFactor));

                return (
                  <path
                    key={t.id}
                    d={`M ${t.baseX} ${t.baseY} Q ${t.baseX + wave1} ${t.baseY + currentLength * 0.4} ${t.baseX + wave2} ${curY}`}
                    stroke="rgba(224, 242, 254, 0.75)"
                    strokeWidth="2.2"
                    fill="none"
                    strokeLinecap="round"
                    filter="drop-shadow(0 0 3px rgba(56, 189, 248, 0.4))"
                  />
                );
              })}
          </g>

          {/* Contracting / Inversion Resorption Particles (During Beat 2) */}
          {isContracting && contractFactor > 0.2 && (
            <g>
              {[...Array(16)].map((_, idx) => {
                const angle = (idx / 16) * Math.PI * 2 + frame * 0.05;
                const dist = (1 - contractFactor) * 220 + 30;
                return (
                  <circle
                    key={idx}
                    cx={Math.cos(angle) * dist}
                    cy={Math.sin(angle) * dist + 80}
                    r={3.5 + (idx % 3)}
                    fill="#38bdf8"
                    opacity={0.8}
                    filter="drop-shadow(0 0 6px #0284c7)"
                  />
                );
              })}
            </g>
          )}
        </svg>
      </div>
    </div>
  );
};

// ========================================================
// CYST STAGE (TRANSDIFFERENTIATION ON SEAFLOOR)
// ========================================================
const CystStage: React.FC<{ frame: number; progress: number }> = ({ frame }) => {
  // Deep-sea floor cyst (spherical ball of reprogrammed tissue)
  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: 1080,
        height: 1920,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          width: 800,
          height: 1000,
          position: 'relative',
          marginTop: 150, // Situated near the lower seafloor
        }}
      >
        <svg viewBox="-400 -300 800 600" width="800" height="600" style={{ overflow: 'visible' }}>
          <defs>
            <radialGradient id="cystGradient" cx="45%" cy="40%" r="55%">
              <stop offset="0%" stopColor="#fef08a" stopOpacity="0.95" />
              <stop offset="25%" stopColor="#34d399" stopOpacity="0.9" />
              <stop offset="65%" stopColor="#059669" stopOpacity="0.85" />
              <stop offset="100%" stopColor="#064e3b" stopOpacity="0.95" />
            </radialGradient>
            <filter id="cystPulseGlow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="14" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* Seafloor substrate anchor */}
          <ellipse cx="0" cy="190" rx="260" ry="50" fill="#030712" opacity="0.9" />

          {/* Bioluminescent reprogramming rings */}
          {[0, 1, 2].map((ring) => {
            const r = 160 + ring * 45 + Math.sin(frame * 0.08 + ring) * 12;
            const op = 0.35 - ring * 0.1;
            return (
              <circle
                key={ring}
                cx="0"
                cy="110"
                r={r}
                fill="none"
                stroke="#10b981"
                strokeWidth="2"
                strokeDasharray="12 18"
                opacity={op}
                transform={`rotate(${frame * (1.5 - ring * 0.5)} 0 110)`}
              />
            );
          })}

          {/* Spherical Cyst Ball */}
          <circle
            cx="0"
            cy="110"
            r={135 + Math.sin(frame * 0.09) * 6}
            fill="url(#cystGradient)"
            stroke="#6ee7b7"
            strokeWidth="4"
            filter="url(#cystPulseGlow)"
          />

          {/* Internal Genetic Reprogramming Swirl (Transdifferentiation) */}
          {[...Array(14)].map((_, idx) => {
            const rot = (idx / 14) * 360 + frame * 1.8;
            const rad = (rot * Math.PI) / 180;
            const dist = 35 + (idx % 4) * 22;
            const cx = Math.cos(rad) * dist;
            const cy = 110 + Math.sin(rad) * dist;
            return (
              <g key={idx}>
                <circle
                  cx={cx}
                  cy={cy}
                  r={5 + (idx % 3)}
                  fill="#ffffff"
                  filter="drop-shadow(0 0 6px #34d399)"
                />
                <line
                  x1="0"
                  y1="110"
                  x2={cx}
                  y2={cy}
                  stroke="rgba(255, 255, 255, 0.4)"
                  strokeWidth="1.5"
                />
              </g>
            );
          })}

          {/* Label: Epigenetic Reset */}
          <text
            x="0"
            y="-40"
            textAnchor="middle"
            fill="#a7f3d0"
            fontSize="26"
            fontFamily="Consolas, monospace"
            fontWeight="800"
            letterSpacing="3"
            filter="drop-shadow(0 2px 8px rgba(0,0,0,0.9))"
          >
            [ REINICIO EPIGENÉTICO : 0 AÑOS ]
          </text>
        </svg>
      </div>
    </div>
  );
};

// ========================================================
// POLYP STAGE (HYDROID COLONY WITH BUDDING CLONES)
// ========================================================
const PolypStage: React.FC<{ frame: number; progress: number }> = ({ frame }) => {
  // The cyst has sprouted a hydrozoan polyp stolon with medusa buds
  const sproutHeight = interpolate(frame % 300, [0, 80], [120, 320], {
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: 1080,
        height: 1920,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          width: 800,
          height: 1100,
          position: 'relative',
          marginTop: 180,
        }}
      >
        <svg viewBox="-400 -400 800 800" width="800" height="800" style={{ overflow: 'visible' }}>
          <defs>
            <linearGradient id="polypStolonGrad" x1="0%" y1="100%" x2="0%" y2="0%">
              <stop offset="0%" stopColor="#047857" />
              <stop offset="50%" stopColor="#10b981" />
              <stop offset="100%" stopColor="#6ee7b7" />
            </linearGradient>
            <radialGradient id="budGlowGrad" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#ffffff" />
              <stop offset="40%" stopColor="#ff4d00" />
              <stop offset="90%" stopColor="#0284c7" />
              <stop offset="100%" stopColor="#0369a1" />
            </radialGradient>
          </defs>

          {/* Seafloor Base */}
          <path
            d="M -350 320 Q 0 280 350 320 L 350 360 L -350 360 Z"
            fill="#050d1a"
            stroke="#0f2b48"
            strokeWidth="3"
          />

          {/* Main Polyp Stem */}
          <path
            d={`M 0 300 C -25 180 30 60 0 ${300 - sproutHeight}`}
            stroke="url(#polypStolonGrad)"
            strokeWidth="14"
            fill="none"
            strokeLinecap="round"
          />

          {/* Branch 1 (Left) */}
          <path
            d="M -8 180 C -80 140 -130 90 -160 30"
            stroke="url(#polypStolonGrad)"
            strokeWidth="9"
            fill="none"
            strokeLinecap="round"
          />

          {/* Branch 2 (Right) */}
          <path
            d="M 5 120 C 70 80 140 50 175 -20"
            stroke="url(#polypStolonGrad)"
            strokeWidth="9"
            fill="none"
            strokeLinecap="round"
          />

          {/* Feeding Tentacles on Polyp Heads */}
          {[-160, 0, 175].map((tipX, idx) => {
            const tipY = idx === 0 ? 30 : idx === 1 ? 300 - sproutHeight : -20;
            return (
              <g key={idx} transform={`translate(${tipX}, ${tipY})`}>
                {/* Waving crown of hydranth tentacles */}
                {[...Array(8)].map((_, tIdx) => {
                  const angle = (tIdx / 8) * Math.PI * 2;
                  const wave = Math.sin(frame * 0.1 + tIdx + idx) * 8;
                  const tx = Math.cos(angle) * (35 + wave);
                  const ty = Math.sin(angle) * (35 + wave);
                  return (
                    <line
                      key={tIdx}
                      x1="0"
                      y1="0"
                      x2={tx}
                      y2={ty}
                      stroke="#a7f3d0"
                      strokeWidth="2.5"
                      strokeLinecap="round"
                    />
                  );
                })}
                {/* Hydranth mouth */}
                <circle cx="0" cy="0" r="10" fill="#34d399" />
              </g>
            );
          })}

          {/* Medusa Bud 1 (Growing on left branch) */}
          <g
            transform={`translate(-110, 100) scale(${0.75 + Math.sin(frame * 0.12) * 0.08})`}
            filter="drop-shadow(0 0 12px rgba(56, 189, 248, 0.7))"
          >
            <circle cx="0" cy="0" r="26" fill="url(#budGlowGrad)" />
            <circle cx="0" cy="0" r="12" fill="#ffedd5" />
          </g>

          {/* Medusa Bud 2 (Budding off right branch into open water!) */}
          {(() => {
            const detachingFrame = frame % 90;
            const detachY = interpolate(detachingFrame, [0, 90], [0, -220]);
            const detachX = interpolate(detachingFrame, [0, 90], [0, 45]);
            const detachScale = interpolate(detachingFrame, [0, 90], [0.65, 0.95]);
            return (
              <g
                transform={`translate(${140 + detachX}, ${10 + detachY}) scale(${detachScale})`}
                filter="drop-shadow(0 0 16px #38bdf8)"
              >
                {/* Mini Baby Medusa Bell */}
                <path
                  d="M -30 25 C -35 5 -25 -25 0 -30 C 25 -25 35 5 30 25 Z"
                  fill="rgba(56, 189, 248, 0.6)"
                  stroke="#7dd3fc"
                  strokeWidth="2"
                />
                <circle cx="0" cy="0" r="9" fill="#ff4d00" />
                {/* Mini tentacles */}
                <line x1="-18" y1="25" x2="-22" y2="48" stroke="#bae6fd" strokeWidth="1.5" />
                <line x1="0" y1="25" x2="0" y2="52" stroke="#bae6fd" strokeWidth="1.5" />
                <line x1="18" y1="25" x2="22" y2="48" stroke="#bae6fd" strokeWidth="1.5" />
              </g>
            );
          })()}

          {/* Text Tag: Gemación Clonal */}
          <text
            x="0"
            y="-260"
            textAnchor="middle"
            fill="#7dd3fc"
            fontSize="24"
            fontFamily="Consolas, monospace"
            fontWeight="800"
            letterSpacing="2"
            filter="drop-shadow(0 2px 8px rgba(0,0,0,0.9))"
          >
            [ GEMACIÓN : MEDUSAS CLONADAS ]
          </text>
        </svg>
      </div>
    </div>
  );
};
