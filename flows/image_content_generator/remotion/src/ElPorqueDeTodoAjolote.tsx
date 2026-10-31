import React from 'react';
import {
  Audio,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { HeroAxolotl } from './components_ajolote/HeroAxolotl';
import { WatermarkLogo } from './components_mundo_insolito/WatermarkLogo';
import { AJOLOTE_TIMELINE, AJOLOTE_TOTAL_FRAMES } from './ajolote_timeline';

export const ElPorqueDeTodoAjolote: React.FC = () => {
  const frame = useCurrentFrame();

  // ==========================================
  // CINEMATIC CAMERA SYSTEM (DIRECTED ZOOMS)
  // Focus point: Right Shoulder / Stump (670px, 590px)
  // ==========================================
  let zoom = 1.0;

  if (frame < 90) {
    // Shot 1A: Full Overview of swimming axolotl
    zoom = 1.0;
  } else if (frame < 140) {
    // Smooth zoom in directly toward the right limb amputation
    const p = (frame - 90) / 50;
    zoom = interpolate(p, [0, 1], [1.0, 2.15], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
  } else if (frame < 406) {
    // Beat 1: Hold on zoomed limb, skin seals without scab
    zoom = 2.15;
  } else if (frame < 737) {
    // Beat 2: Zoom on stump with X-ray bones & macrophages
    zoom = 2.3;
  } else if (frame < 1196) {
    // Beat 3: Blastema formation up close
    zoom = 2.45;
  } else if (frame < 1693) {
    // Beat 4: Regrowth & green muscle cells
    zoom = 2.05;
  } else if (frame < 1765) {
    // Beat 5: Smooth Zoom-Out back to full body overview!
    const p = (frame - 1693) / 72;
    zoom = interpolate(p, [0, 1], [2.05, 1.0], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
  } else {
    // Hold on full swimming axolotl with fully regenerated limb!
    zoom = 1.0;
  }

  // ==========================================
  // DYNAMIC MORPHOLOGY STATES
  // ==========================================
  let limbState: 'intact' | 'cutting' | 'amputated' | 'macrophages' | 'blastema' | 'regrowing' | 'complete' = 'intact';
  let cutProgress = 0;
  let blastemaProgress = 0;
  let regrowthProgress = 0;
  let dayText = 'DÍA 0';
  let scaleText = '1 cm';

  if (frame < 80) {
    limbState = 'intact';
    dayText = 'DÍA 0';
    scaleText = '1 cm';
  } else if (frame < 140) {
    limbState = 'cutting';
    cutProgress = Math.min(1, (frame - 80) / 45);
    dayText = 'DÍA 0';
    scaleText = '5 mm';
  } else if (frame < 406) {
    limbState = 'amputated';
    cutProgress = 1.0;
    dayText = 'DÍA 1';
    scaleText = '5 mm';
  } else if (frame < 737) {
    limbState = 'macrophages';
    dayText = 'DÍA 3';
    scaleText = '200 µm';
  } else if (frame < 1196) {
    limbState = 'blastema';
    blastemaProgress = Math.min(1, (frame - 737) / 250);
    dayText = 'DÍA 7';
    scaleText = '500 µm';
  } else if (frame < 1693) {
    limbState = 'regrowing';
    regrowthProgress = Math.min(1, (frame - 1196) / 450);
    dayText = 'DÍA 21';
    scaleText = '5 mm';
  } else {
    limbState = 'complete';
    dayText = 'DÍA 45  //  REGENERACIÓN 100%';
    scaleText = '1 cm';
  }

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: '#24201a',
        position: 'relative',
        width: 1080,
        height: 1920,
        overflow: 'hidden',
      }}
    >
      {/* 1. MUDDY POND BOTTOM BACKGROUND WITH PEBBLES & CAUSTICS */}
      <PondBackground frame={frame} />

      {/* 2. CAMERA TRANSFORM WRAPPER FOR THE HERO AXOLOTL */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: 1080,
          height: 1920,
          transform: `scale(${zoom})`,
          transformOrigin: '670px 590px',
        }}
      >
        <HeroAxolotl
          frame={frame}
          limbState={limbState}
          cutProgress={cutProgress}
          blastemaProgress={blastemaProgress}
          regrowthProgress={regrowthProgress}
          showGreenMuscle={frame >= 1196 && frame < 1693}
          showXrayBones={frame >= 406 && frame < 737}
          showNervePulses={frame >= 737 && frame < 1196}
        />
      </div>

      {/* 3. MINIMAL TECHNICAL HUD OVERLAYS */}
      {/* Day Counter (Top-Left) */}
      <div
        style={{
          position: 'absolute',
          top: 70,
          left: 65,
          fontFamily: 'Consolas, monospace',
          fontSize: 34,
          fontWeight: 800,
          color: '#ffffff',
          letterSpacing: 2,
          textShadow: '0 2px 10px rgba(0, 0, 0, 0.8)',
          zIndex: 50,
        }}
      >
        {dayText}
      </div>

      {/* Brand Watermark (Top-Right) */}
      <WatermarkLogo />

      {/* Scale Bar (Bottom-Left) */}
      <div
        style={{
          position: 'absolute',
          bottom: 75,
          left: 65,
          zIndex: 50,
        }}
      >
        <div
          style={{
            width: scaleText === '1 cm' ? 120 : scaleText === '5 mm' ? 80 : 50,
            height: 4,
            backgroundColor: '#ffffff',
            boxShadow: '0 2px 8px rgba(0,0,0,0.8)',
          }}
        />
        <div
          style={{
            fontFamily: 'Consolas, monospace',
            fontSize: 20,
            color: '#ffffff',
            marginTop: 6,
            fontWeight: 700,
            textShadow: '0 2px 8px rgba(0,0,0,0.8)',
          }}
        >
          {scaleText}
        </div>
      </div>

      {/* 4. HIGH-IMPACT MINIMAL TYPOGRAPHY OVERLAY */}
      <MinimalTypographyOverlay frame={frame} />

      {/* 5. AUDIO SYNCHRONIZATION */}
      {AJOLOTE_TIMELINE.map((beat) => (
        <Sequence
          key={beat.id}
          from={beat.startFrame}
          durationInFrames={beat.durationFrames}
        >
          <Audio src={staticFile(beat.audioPath)} volume={1.0} />
        </Sequence>
      ))}
    </div>
  );
};

// ==========================================
// POND BACKGROUND COMPONENT
// ==========================================
const PondBackground: React.FC<{ frame: number }> = ({ frame }) => {
  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: 1080,
        height: 1920,
        background: 'radial-gradient(ellipse at 50% 40%, #2a251e 0%, #1c1813 60%, #110f0c 100%)',
      }}
    >
      <svg width="1080" height="1920" style={{ position: 'absolute', top: 0, left: 0 }}>
        {/* Subtle scattered riverbed pebbles */}
        <g opacity="0.22" fill="#0c0a08">
          <ellipse cx="180" cy="220" rx="45" ry="35" />
          <ellipse cx="880" cy="310" rx="55" ry="40" />
          <ellipse cx="120" cy="740" rx="35" ry="25" />
          <ellipse cx="940" cy="850" rx="40" ry="30" />
          <ellipse cx="150" cy="1350" rx="50" ry="38" />
          <ellipse cx="890" cy="1480" rx="42" ry="32" />
          <ellipse cx="250" cy="1720" rx="38" ry="28" />
          <ellipse cx="760" cy="1820" rx="48" ry="36" />
        </g>

        {/* Moving Water Caustics */}
        <g stroke="rgba(255, 255, 255, 0.035)" strokeWidth="3" fill="none">
          {[0, 1, 2, 3, 4, 5].map((idx) => {
            const yBase = (idx * 340 + frame * 0.9) % 2100 - 100;
            return (
              <path
                key={idx}
                d={`M 0 ${yBase} C 270 ${yBase + Math.sin(frame * 0.04 + idx) * 35} 540 ${yBase - Math.sin(frame * 0.04 + idx) * 35} 810 ${yBase + Math.cos(frame * 0.04 + idx) * 30} L 1080 ${yBase}`}
              />
            );
          })}
        </g>
      </svg>
    </div>
  );
};

// ==========================================
// MINIMAL TYPOGRAPHY OVERLAY (LIKE ORIGINAL)
// ==========================================
const MinimalTypographyOverlay: React.FC<{ frame: number }> = ({ frame }) => {
  const activeBeat = AJOLOTE_TIMELINE.find(
    (b) => frame >= b.startFrame && frame < b.startFrame + b.durationFrames
  );

  if (!activeBeat) return null;

  let bigHeadline = '';
  let subText = '';

  if (activeBeat.id === 'ajolote_b1') {
    if (frame < 140) {
      bigHeadline = 'LE VUELVE A CRECER';
      subText = 'la pata entera, sin cicatriz';
    } else {
      bigHeadline = 'SELLA EN HORAS';
      subText = 'la piel se desliza sin formar costra';
    }
  } else if (activeBeat.id === 'ajolote_b2') {
    bigHeadline = 'LOS MACRÓFAGOS LIMPIAN';
    subText = 'sin ellos, cicatriza igual que un humano';
  } else if (activeBeat.id === 'ajolote_b3') {
    bigHeadline = 'EL BLASTEMA';
    subText = 'células adultas que regresan en el tiempo';
  } else if (activeBeat.id === 'ajolote_b4') {
    bigHeadline = 'MEMORIA EXACTA';
    subText = 'la vitamina A marca la coordenada espacial';
  } else if (activeBeat.id === 'ajolote_b5') {
    bigHeadline = '¿REGENERACIÓN EN HUMANOS?';
    subText = 'escribe SÍ o NO en los comentarios';
  }

  // Typewriter reveal of narration
  const localFrame = frame - activeBeat.startFrame;
  const audioDurationFrames = Math.round(activeBeat.audioDuration * 30);
  const text = activeBeat.text;
  const progress = Math.min(1, Math.max(0, localFrame / (audioDurationFrames * 0.95)));
  const visibleCharsCount = Math.floor(progress * text.length);
  const visibleText = text.slice(0, visibleCharsCount);
  const hiddenText = text.slice(visibleCharsCount);

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 120,
        left: 60,
        right: 60,
        zIndex: 100,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        textAlign: 'center',
        pointerEvents: 'none',
      }}
    >
      {/* Big Impact Hook (Like Reference Screenshot) */}
      <div
        style={{
          fontFamily: 'Bahnschrift, Arial, sans-serif',
          fontSize: 62,
          fontWeight: 900,
          color: '#ffffff',
          letterSpacing: 1,
          textTransform: 'uppercase',
          textShadow: '0 4px 18px rgba(0, 0, 0, 0.95), 0 2px 6px rgba(0, 0, 0, 0.9)',
          lineHeight: 1.1,
          marginBottom: 8,
        }}
      >
        {bigHeadline}
      </div>

      {/* Subtitle Line */}
      <div
        style={{
          fontFamily: 'Consolas, monospace',
          fontSize: 30,
          fontWeight: 700,
          color: '#e2e8f0',
          letterSpacing: 1.5,
          textShadow: '0 2px 10px rgba(0, 0, 0, 0.9)',
          marginBottom: 20,
        }}
      >
        {subText}
      </div>

      {/* Narration Typewriter Ribbon (Sleek, transparent, no heavy card) */}
      <div
        style={{
          backgroundColor: 'rgba(15, 13, 10, 0.88)',
          border: '1px solid rgba(255, 255, 255, 0.15)',
          borderRadius: 12,
          padding: '12px 28px',
          maxWidth: 960,
          fontFamily: 'Bahnschrift, Arial, sans-serif',
          fontSize: 27,
          lineHeight: 1.3,
          fontWeight: 600,
          boxShadow: '0 6px 24px rgba(0, 0, 0, 0.7)',
        }}
      >
        <span style={{ color: '#ffffff' }}>{visibleText}</span>
        <span style={{ opacity: 0 }}>{hiddenText}</span>
      </div>
    </div>
  );
};
