import React from 'react';
import { interpolate, spring } from 'remotion';

interface HeroAxolotlProps {
  frame: number;
  limbState: 'intact' | 'cutting' | 'amputated' | 'macrophages' | 'blastema' | 'regrowing' | 'complete';
  cutProgress?: number;
  blastemaProgress?: number;
  regrowthProgress?: number;
  showGreenMuscle?: boolean;
  showXrayBones?: boolean;
  showNervePulses?: boolean;
  showScarSplit?: boolean;
}

export const HeroAxolotl: React.FC<HeroAxolotlProps> = ({
  frame,
  limbState,
  cutProgress = 0,
  blastemaProgress = 0,
  regrowthProgress = 0,
  showGreenMuscle = false,
  showXrayBones = false,
  showNervePulses = false,
  showScarSplit = false,
}) => {
  // Palette sampled from original reference
  const skin = '#d4b2a9';
  const skinDark = '#be958c';
  const skinBelly = '#ebd2cb';
  const gillStalk = '#b35b6b';
  const gillFilament = '#c84f64';
  const eyeColor = '#111111';

  // Body gentle swimming sway
  const bodySway = Math.sin(frame * 0.05) * 6;
  const baseHeadX = 540 + bodySway;
  const baseHeadY = 460;
  const baseBodyY = 750;
  const baseTailY = 1040;

  // Tail wave animation (traveling sine wave along the spine)
  const tailSteps = 24;
  const tailLen = 460;
  const tailPtsLeft: [number, number][] = [];
  const tailPtsRight: [number, number][] = [];
  const finPtsLeft: [number, number][] = [];
  const finPtsRight: [number, number][] = [];

  for (let i = 0; i <= tailSteps; i++) {
    const p = i / tailSteps;
    const curY = baseTailY + p * tailLen;
    // Traveling wave
    const wave = Math.sin(frame * 0.085 - p * 3.4) * (p * 60);
    const cx = baseHeadX + wave;

    // Muscular core tapers down to tail tip
    const thickness = (1 - p) * 32 + 3;
    tailPtsLeft.push([cx - thickness, curY]);
    tailPtsRight.push([cx + thickness, curY]);

    // Translucent fin membrane expands at mid-tail
    const finThick = Math.sin(p * Math.PI) * 46 + thickness * 0.85;
    finPtsLeft.push([cx - finThick, curY]);
    finPtsRight.push([cx + finThick, curY]);
  }

  const tailMusclePath = `M ${tailPtsLeft[0][0].toFixed(1)} ${tailPtsLeft[0][1].toFixed(1)} ` +
    tailPtsLeft.slice(1).map(pt => `L ${pt[0].toFixed(1)} ${pt[1].toFixed(1)}`).join(' ') +
    ` L ${tailPtsRight[tailPtsRight.length - 1][0].toFixed(1)} ${tailPtsRight[tailPtsRight.length - 1][1].toFixed(1)} ` +
    tailPtsRight.slice(0, -1).reverse().map(pt => `L ${pt[0].toFixed(1)} ${pt[1].toFixed(1)}`).join(' ') + ' Z';

  const tailFinPath = `M ${finPtsLeft[0][0].toFixed(1)} ${finPtsLeft[0][1].toFixed(1)} ` +
    finPtsLeft.slice(1).map(pt => `L ${pt[0].toFixed(1)} ${pt[1].toFixed(1)}`).join(' ') +
    ` L ${finPtsRight[finPtsRight.length - 1][0].toFixed(1)} ${finPtsRight[finPtsRight.length - 1][1].toFixed(1)} ` +
    finPtsRight.slice(0, -1).reverse().map(pt => `L ${pt[0].toFixed(1)} ${pt[1].toFixed(1)}`).join(' ') + ' Z';

  // Gill waving oscillations
  const gw1 = Math.sin(frame * 0.08) * 5;
  const gw2 = Math.sin(frame * 0.08 + 1.2) * 5;
  const gw3 = Math.sin(frame * 0.08 + 2.4) * 5;

  // Floating detached arm drift when cut
  const detachX = cutProgress > 0 ? cutProgress * 45 : 0;
  const detachY = cutProgress > 0 ? cutProgress * 25 : 0;
  const detachOpacity = Math.max(0, 1 - cutProgress * 1.2);

  // Electrical nerve pulse
  const nervePulseX = (frame * 5) % 110;

  // Green muscle pulse
  const greenGlow = Math.sin(frame * 0.12) * 3 + 8;

  return (
    <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{ position: 'absolute', top: 0, left: 0 }}>
      <defs>
        {/* Soft shadow filter */}
        <filter id="softShadow" x="-20%" y="-20%" width="150%" height="150%">
          <feDropShadow dx="18" dy="28" stdDeviation="16" floodColor="#080705" floodOpacity="0.45" />
        </filter>

        <linearGradient id="finGrad" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor={skinDark} stopOpacity="0.5" />
          <stop offset="70%" stopColor={skin} stopOpacity="0.35" />
          <stop offset="100%" stopColor={skinDark} stopOpacity="0.1" />
        </linearGradient>

        <radialGradient id="blastemaGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#67e8f9" stopOpacity="0.9" />
          <stop offset="60%" stopColor="#0284c7" stopOpacity="0.7" />
          <stop offset="100%" stopColor="#082f49" stopOpacity="0.2" />
        </radialGradient>
      </defs>

      <g filter="url(#softShadow)">
        {/* 1. TAIL FIN (Translucent wide membrane) */}
        <path d={tailFinPath} fill="url(#finGrad)" />

        {/* 2. TAIL CENTRAL MUSCLE COLUMN */}
        <path d={tailMusclePath} fill={skin} stroke={skinDark} strokeWidth="1" />

        {/* 3. HIND LIMBS */}
        {/* Left Hind Limb */}
        <g transform={`translate(${baseHeadX - 110}, 980)`}>
          <path d="M 0 0 C -50 20 -90 40 -120 90 C -90 105 -60 70 -30 35" fill={skin} stroke={skinDark} strokeWidth="2" />
          <line x1="-120" y1="90" x2="-145" y2="95" stroke={skin} strokeWidth="8" strokeLinecap="round" />
          <line x1="-120" y1="90" x2="-140" y2="115" stroke={skin} strokeWidth="8" strokeLinecap="round" />
          <line x1="-120" y1="90" x2="-120" y2="125" stroke={skin} strokeWidth="8" strokeLinecap="round" />
          <line x1="-120" y1="90" x2="-100" y2="120" stroke={skin} strokeWidth="8" strokeLinecap="round" />
        </g>
        {/* Right Hind Limb */}
        <g transform={`translate(${baseHeadX + 110}, 980)`}>
          <path d="M 0 0 C 50 20 90 40 120 90 C 90 105 60 70 30 35" fill={skin} stroke={skinDark} strokeWidth="2" />
          <line x1="120" y1="90" x2="145" y2="95" stroke={skin} strokeWidth="8" strokeLinecap="round" />
          <line x1="120" y1="90" x2="140" y2="115" stroke={skin} strokeWidth="8" strokeLinecap="round" />
          <line x1="120" y1="90" x2="120" y2="125" stroke={skin} strokeWidth="8" strokeLinecap="round" />
          <line x1="120" y1="90" x2="100" y2="120" stroke={skin} strokeWidth="8" strokeLinecap="round" />
        </g>

        {/* 4. MAIN TORSO */}
        <g transform={`translate(${baseHeadX}, ${baseBodyY})`}>
          <ellipse cx="0" cy="0" rx="122" ry="310" fill={skin} stroke={skinDark} strokeWidth="2.5" />
          {/* Lighter belly contour */}
          <ellipse cx="0" cy="15" rx="82" ry="260" fill={skinBelly} />

          {/* Costal Grooves (Rib ridges) */}
          <g stroke={skinDark} strokeWidth="2" opacity="0.55" fill="none">
            <path d="M -92 -160 C -40 -150 40 -150 92 -160" />
            <path d="M -97 -110 C -40 -100 40 -100 97 -110" />
            <path d="M -102 -60 C -40 -50 40 -50 102 -60" />
            <path d="M -102 -10 C -40 0 40 0 102 -10" />
            <path d="M -100 40 C -40 50 40 50 100 40" />
            <path d="M -97 90 C -40 100 40 100 97 90" />
            <path d="M -92 140 C -40 150 40 150 92 140" />
            <path d="M -82 190 C -40 200 40 200 82 190" />
          </g>
        </g>

        {/* 5. LEFT FRONT LIMB (Always intact) */}
        <g transform={`translate(${baseHeadX - 110}, 620)`}>
          <path d="M 0 0 C -60 -10 -120 -20 -180 30 C -150 50 -100 35 -30 20" fill={skin} stroke={skinDark} strokeWidth="2" />
          <line x1="-180" y1="30" x2="-215" y2="20" stroke={skin} strokeWidth="7" strokeLinecap="round" />
          <line x1="-180" y1="30" x2="-215" y2="45" stroke={skin} strokeWidth="7" strokeLinecap="round" />
          <line x1="-180" y1="30" x2="-195" y2="65" stroke={skin} strokeWidth="7" strokeLinecap="round" />
          <line x1="-180" y1="30" x2="-170" y2="70" stroke={skin} strokeWidth="7" strokeLinecap="round" />
        </g>

        {/* 6. RIGHT FRONT LIMB (DYNAMIC REGENERATION MORPHOLOGY) */}
        <g transform={`translate(${baseHeadX + 110}, 620)`}>
          {/* Base upper arm stump */}
          <path d="M 0 0 C 35 -5 65 -10 75 10 C 65 25 35 20 0 18 Z" fill={skin} stroke={skinDark} strokeWidth="2" />

          {/* Internal X-Ray Bones (when zoomed in) */}
          {showXrayBones && (
            <g opacity="0.85">
              {/* Humerus Bone */}
              <line x1="10" y1="10" x2="70" y2="10" stroke="#ffffff" strokeWidth="8" strokeLinecap="round" />
              {/* Muscle striations */}
              <line x1="15" y1="5" x2="65" y2="5" stroke="#ef4444" strokeWidth="2" strokeDasharray="4 2" />
              <line x1="15" y1="15" x2="65" y2="15" stroke="#ef4444" strokeWidth="2" strokeDasharray="4 2" />
            </g>
          )}

          {/* Nerve Pulses (Yellow glowing electric signal) */}
          {showNervePulses && (
            <g>
              <line x1="5" y1="10" x2="75" y2="10" stroke="#facc15" strokeWidth="3" strokeLinecap="round" />
              <circle
                cx={Math.min(75, 5 + nervePulseX)}
                cy="10"
                r="5"
                fill="#ffffff"
                filter="drop-shadow(0 0 8px #facc15)"
              />
            </g>
          )}

          {/* STATE A: INTACT WITH CUT LINE */}
          {limbState === 'intact' && (
            <g>
              <path d="M 75 10 C 115 10 155 10 185 50 C 160 65 125 50 75 15 Z" fill={skin} stroke={skinDark} strokeWidth="2" />
              <line x1="185" y1="50" x2="220" y2="40" stroke={skin} strokeWidth="7" strokeLinecap="round" />
              <line x1="185" y1="50" x2="220" y2="65" stroke={skin} strokeWidth="7" strokeLinecap="round" />
              <line x1="185" y1="50" x2="200" y2="85" stroke={skin} strokeWidth="7" strokeLinecap="round" />
              <line x1="185" y1="50" x2="175" y2="90" stroke={skin} strokeWidth="7" strokeLinecap="round" />

              {/* White Dashed Cut Line */}
              <line x1="75" y1="-8" x2="75" y2="28" stroke="#ffffff" strokeWidth="3.5" strokeDasharray="5 4" />
            </g>
          )}

          {/* STATE B: CUTTING / AMPUTATED (Detached forearm floating away) */}
          {(limbState === 'cutting' || limbState === 'amputated') && (
            <>
              {/* Floating detached forearm */}
              {detachOpacity > 0 && (
                <g transform={`translate(${75 + detachX}, ${detachY})`} opacity={detachOpacity}>
                  <path d="M 0 0 C 40 0 80 0 110 40 C 85 55 50 40 0 5 Z" fill={skin} stroke={skinDark} strokeWidth="1.5" />
                  <line x1="110" y1="40" x2="145" y2="30" stroke={skin} strokeWidth="7" strokeLinecap="round" />
                  <line x1="110" y1="40" x2="145" y2="55" stroke={skin} strokeWidth="7" strokeLinecap="round" />
                  <line x1="110" y1="40" x2="125" y2="75" stroke={skin} strokeWidth="7" strokeLinecap="round" />
                  <line x1="110" y1="40" x2="100" y2="80" stroke={skin} strokeWidth="7" strokeLinecap="round" />
                </g>
              )}

              {/* Sealed skin sliding over stump */}
              <path
                d="M 75 0 C 85 5 85 15 75 20"
                stroke="#38bdf8"
                strokeWidth="3.5"
                fill="none"
              />
            </>
          )}

          {/* STATE C: MACROPHAGES ACTIVE */}
          {limbState === 'macrophages' && (
            <g>
              {/* Smooth sealed skin edge */}
              <path d="M 75 0 C 86 5 86 15 75 20" stroke="#10b981" strokeWidth="3" fill="none" />
              {/* Tiny glowing amoeboid macrophages sweeping */}
              {[
                { x: 78, y: 3 },
                { x: 82, y: 10 },
                { x: 77, y: 17 },
              ].map((m, idx) => (
                <circle
                  key={idx}
                  cx={m.x + Math.sin(frame * 0.15 + idx) * 3}
                  cy={m.y}
                  r="4"
                  fill="#f472b6"
                  filter="drop-shadow(0 0 6px #ec4899)"
                />
              ))}
            </g>
          )}

          {/* STATE D: BLASTEMA DOME FORMATION */}
          {limbState === 'blastema' && (
            <g>
              {/* Blastema Bud Dome */}
              <path
                d={`M 75 0 C ${75 + 35 * blastemaProgress} 2 ${75 + 35 * blastemaProgress} 18 75 20`}
                fill="url(#blastemaGlow)"
                stroke="#67e8f9"
                strokeWidth="2.5"
              />
              {/* Mitotic Progenitor Cells */}
              {[
                { x: 82, y: 6 },
                { x: 88, y: 11 },
                { x: 83, y: 15 },
                { x: 94, y: 9 },
              ].map((c, idx) => (
                <circle
                  key={idx}
                  cx={c.x}
                  cy={c.y}
                  r="2.5"
                  fill="#ffffff"
                  opacity={blastemaProgress}
                />
              ))}
            </g>
          )}

          {/* STATE E: REGROWING & LINEAGE GFP */}
          {limbState === 'regrowing' && (
            <g>
              {/* Elongating regenerated forearm */}
              <path
                d={`M 75 0 C ${75 + 70 * regrowthProgress} 5 ${75 + 100 * regrowthProgress} 10 ${75 + 110 * regrowthProgress} ${20 + 20 * regrowthProgress} C ${75 + 85 * regrowthProgress} ${30 + 15 * regrowthProgress} ${75 + 40 * regrowthProgress} 25 75 20 Z`}
                fill={skin}
                stroke={skinDark}
                strokeWidth="2"
              />

              {/* GFP Green Muscle Cell Lineage (Fluorescent Green Glow) */}
              {showGreenMuscle && (
                <path
                  d={`M 80 6 C ${80 + 50 * regrowthProgress} 8 ${80 + 80 * regrowthProgress} 12 ${80 + 90 * regrowthProgress} 18`}
                  stroke="#22c55e"
                  strokeWidth="5"
                  fill="none"
                  strokeLinecap="round"
                  filter={`drop-shadow(0 0 ${greenGlow}px #22c55e)`}
                />
              )}

              {/* Sprouting tiny digits */}
              {regrowthProgress > 0.6 && (
                <g opacity={(regrowthProgress - 0.6) / 0.4}>
                  <line x1={75 + 110 * regrowthProgress} y1="40" x2={75 + 130 * regrowthProgress} y2="35" stroke={skin} strokeWidth="6" strokeLinecap="round" />
                  <line x1={75 + 110 * regrowthProgress} y1="40" x2={75 + 130 * regrowthProgress} y2="50" stroke={skin} strokeWidth="6" strokeLinecap="round" />
                  <line x1={75 + 110 * regrowthProgress} y1="40" x2={75 + 120 * regrowthProgress} y2="65" stroke={skin} strokeWidth="6" strokeLinecap="round" />
                </g>
              )}
            </g>
          )}

          {/* STATE F: COMPLETE NEW LIMB */}
          {limbState === 'complete' && (
            <g>
              <path d="M 75 10 C 115 10 155 10 185 50 C 160 65 125 50 75 15 Z" fill={skin} stroke={skinDark} strokeWidth="2" />
              <line x1="185" y1="50" x2="220" y2="40" stroke={skin} strokeWidth="7" strokeLinecap="round" />
              <line x1="185" y1="50" x2="220" y2="65" stroke={skin} strokeWidth="7" strokeLinecap="round" />
              <line x1="185" y1="50" x2="200" y2="85" stroke={skin} strokeWidth="7" strokeLinecap="round" />
              <line x1="185" y1="50" x2="175" y2="90" stroke={skin} strokeWidth="7" strokeLinecap="round" />
            </g>
          )}
        </g>

        {/* 7. AXOLOTL HEAD */}
        <g transform={`translate(${baseHeadX}, ${baseHeadY})`}>
          <path
            d="M -135 -30 C -150 40 -110 90 0 95 C 110 90 150 40 135 -30 C 120 -100 60 -130 0 -130 C -60 -130 -120 -100 -135 -30 Z"
            fill={skin}
            stroke={skinDark}
            strokeWidth="2.5"
          />
          <ellipse cx="0" cy="-10" rx="85" ry="90" fill={skinBelly} />

          {/* Nostrils */}
          <circle cx="-25" cy="-80" r="3.5" fill={skinDark} />
          <circle cx="25" cy="-80" r="3.5" fill={skinDark} />

          {/* Eyes with white reflection dot */}
          <circle cx="-80" cy="-25" r="14" fill={eyeColor} />
          <circle cx="-75" cy="-29" r="4.5" fill="#ffffff" />
          <circle cx="80" cy="-25" r="14" fill={eyeColor} />
          <circle cx="85" cy="-29" r="4.5" fill="#ffffff" />
        </g>

        {/* 8. EXTERNAL GILLS (6 Feathery Rami) */}
        {/* Left Side Gills */}
        <g transform={`translate(${baseHeadX - 100}, ${baseHeadY - 20})`}>
          {/* Ramus 1 */}
          <path d={`M 0 -20 C -70 ${-70 + gw1} -140 -60 -195 -75`} stroke={gillStalk} strokeWidth="9" fill="none" strokeLinecap="round" />
          {[-20, -50, -80, -110, -140, -170].map((gx, idx) => (
            <line key={idx} x1={gx} y1={-25 + gx * 0.25} x2={gx - 8} y2={-40 + gx * 0.25} stroke={gillFilament} strokeWidth="3" strokeLinecap="round" />
          ))}

          {/* Ramus 2 */}
          <path d={`M 0 0 C -80 ${-20 + gw2} -160 -10 -225 -20`} stroke={gillStalk} strokeWidth="9" fill="none" strokeLinecap="round" />
          {[-25, -60, -95, -130, -165, -200].map((gx, idx) => (
            <line key={idx} x1={gx} y1={gx * 0.1} x2={gx - 8} y2={gx * 0.1 + 16} stroke={gillFilament} strokeWidth="3" strokeLinecap="round" />
          ))}

          {/* Ramus 3 */}
          <path d={`M 0 20 C -70 ${20 + gw3} -140 45 -195 55`} stroke={gillStalk} strokeWidth="9" fill="none" strokeLinecap="round" />
          {[-20, -50, -80, -110, -140, -170].map((gx, idx) => (
            <line key={idx} x1={gx} y1={25 - gx * 0.15} x2={gx - 8} y2={40 - gx * 0.15} stroke={gillFilament} strokeWidth="3" strokeLinecap="round" />
          ))}
        </g>

        {/* Right Side Gills */}
        <g transform={`translate(${baseHeadX + 100}, ${baseHeadY - 20})`}>
          {/* Ramus 1 */}
          <path d={`M 0 -20 C 70 ${-70 + gw1} 140 -60 195 -75`} stroke={gillStalk} strokeWidth="9" fill="none" strokeLinecap="round" />
          {[20, 50, 80, 110, 140, 170].map((gx, idx) => (
            <line key={idx} x1={gx} y1={-25 - gx * 0.25} x2={gx + 8} y2={-40 - gx * 0.25} stroke={gillFilament} strokeWidth="3" strokeLinecap="round" />
          ))}

          {/* Ramus 2 */}
          <path d={`M 0 0 C 80 ${-20 + gw2} 160 -10 225 -20`} stroke={gillStalk} strokeWidth="9" fill="none" strokeLinecap="round" />
          {[25, 60, 95, 130, 165, 200].map((gx, idx) => (
            <line key={idx} x1={gx} y1={-gx * 0.1} x2={gx + 8} y2={-gx * 0.1 + 16} stroke={gillFilament} strokeWidth="3" strokeLinecap="round" />
          ))}

          {/* Ramus 3 */}
          <path d={`M 0 20 C 70 ${20 + gw3} 140 45 195 55`} stroke={gillStalk} strokeWidth="9" fill="none" strokeLinecap="round" />
          {[20, 50, 80, 110, 140, 170].map((gx, idx) => (
            <line key={idx} x1={gx} y1={25 + gx * 0.15} x2={gx + 8} y2={40 + gx * 0.15} stroke={gillFilament} strokeWidth="3" strokeLinecap="round" />
          ))}
        </g>
      </g>
    </svg>
  );
};
