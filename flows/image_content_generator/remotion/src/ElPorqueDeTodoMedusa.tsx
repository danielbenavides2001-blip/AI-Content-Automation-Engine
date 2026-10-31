import React from 'react';
import {
  Audio,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import { DeepSeaBackground } from './components_medusa/DeepSeaBackground';
import { HeroMedusa, MedusaMorphState } from './components_medusa/HeroMedusa';
import { MEDUSA_TIMELINE } from './medusa_timeline';

export const ElPorqueDeTodoMedusa: React.FC = () => {
  const frame = useCurrentFrame();

  // Find active narrative beat
  const activeBeat =
    MEDUSA_TIMELINE.find(
      (b) => frame >= b.startFrame && frame < b.startFrame + b.durationFrames
    ) || MEDUSA_TIMELINE[MEDUSA_TIMELINE.length - 1];

  const beatIndex = MEDUSA_TIMELINE.findIndex((b) => b.id === activeBeat.id);

  // ========================================================
  // 1. DYNAMIC MORPHOLOGICAL STATES ACROSS THE NARRATIVE
  // ========================================================
  // Beat 1 (b1): Swimming adult hero
  // Beat 2 (b2): Crisis / Contracting into sphere
  // Beat 3 (b3): Seafloor Cyst / Transdifferentiation
  // Beat 4 (b4): Polyp colony with budding clones
  // Beat 5 (b5): Rejuvenated adult swimming to the surface (reborn)
  let morphState: MedusaMorphState = 'swimming';
  let stateProgress = 0;
  let showFloor = false;
  let floorProgress = 0;
  let cameraZoom = 1.0;
  let cameraOffsetY = 0;

  if (activeBeat.id === 'medusa_b1') {
    morphState = 'swimming';
    stateProgress = (frame - activeBeat.startFrame) / activeBeat.durationFrames;
    showFloor = false;
    cameraZoom = 1.0;
    cameraOffsetY = 0;
  } else if (activeBeat.id === 'medusa_b2') {
    // Medusa contracts and sinks toward seafloor
    morphState = 'contracting';
    const localP = (frame - activeBeat.startFrame) / activeBeat.durationFrames;
    stateProgress = localP;
    showFloor = true;
    floorProgress = interpolate(localP, [0.3, 0.9], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    // Camera descends with sinking medusa
    cameraOffsetY = interpolate(localP, [0.2, 1], [0, 220], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
  } else if (activeBeat.id === 'medusa_b3') {
    // Cyst resting on the ocean floor doing transdifferentiation
    morphState = 'cyst';
    stateProgress = (frame - activeBeat.startFrame) / activeBeat.durationFrames;
    showFloor = true;
    floorProgress = 1.0;
    cameraZoom = 1.15;
    cameraOffsetY = 140;
  } else if (activeBeat.id === 'medusa_b4') {
    // Polyp stage sprouting and budding baby medusae
    morphState = 'polyp';
    stateProgress = (frame - activeBeat.startFrame) / activeBeat.durationFrames;
    showFloor = true;
    floorProgress = 1.0;
    cameraZoom = 1.0;
    cameraOffsetY = 110;
  } else {
    // Beat 5: Rejuvenated adult medusa swimming upward into open ocean
    morphState = 'rebirth';
    const localP = (frame - activeBeat.startFrame) / activeBeat.durationFrames;
    stateProgress = localP;
    showFloor = false;
    cameraZoom = interpolate(localP, [0, 1], [0.95, 1.25], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    cameraOffsetY = interpolate(localP, [0, 1], [60, -80], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
  }

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: '#020611',
        position: 'relative',
        width: 1080,
        height: 1920,
        overflow: 'hidden',
      }}
    >
      {/* 1. DEEP SEA OCEANIC BACKGROUND */}
      <DeepSeaBackground frame={frame} showFloor={showFloor} floorOffset={floorProgress} />

      {/* 2. CAMERA WRAPPER FOR HERO CREATURE */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: 1080,
          height: 1920,
          transform: `scale(${cameraZoom}) translateY(${cameraOffsetY}px)`,
          transformOrigin: '540px 850px',
        }}
      >
        <HeroMedusa
          frame={frame}
          morphState={morphState}
          stateProgress={stateProgress}
        />
      </div>

      {/* ======================================================== */}
      {/* 3. REELS/SHORTS TOP SAFE ZONE (ABOVE y=160px)            */}
      {/* ======================================================== */}
      {/* Category & Scale Tag (Placed safely at top: 170px) */}
      <div
        style={{
          position: 'absolute',
          top: 170,
          left: 70,
          zIndex: 60,
          display: 'flex',
          flexDirection: 'column',
          gap: 6,
        }}
      >
        <div
          style={{
            fontFamily: 'Bahnschrift, Arial, sans-serif',
            fontSize: 22,
            fontWeight: 800,
            color: '#38bdf8',
            letterSpacing: 3,
            textTransform: 'uppercase',
            textShadow: '0 2px 10px rgba(0, 0, 0, 0.9)',
          }}
        >
          ENIGMAIQ  •  BIOLOGÍA
        </div>
        <div
          style={{
            fontFamily: 'Consolas, monospace',
            fontSize: 18,
            fontWeight: 600,
            color: '#94a3b8',
            letterSpacing: 1.5,
          }}
        >
          TAMAÑO: ~4.5 mm  |  TURRITOPSIS DOHRNII
        </div>
      </div>

      {/* Discrete Brand Icon (Top Right, safely at top: 165px) */}
      <div
        style={{
          position: 'absolute',
          top: 165,
          right: 70,
          zIndex: 60,
          display: 'flex',
          alignItems: 'center',
          gap: 10,
        }}
      >
        <div
          style={{
            width: 48,
            height: 48,
            borderRadius: '50%',
            border: '2px solid rgba(56, 189, 248, 0.7)',
            backgroundColor: '#020611',
            boxShadow: '0 0 16px rgba(56, 189, 248, 0.4)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <span
            style={{
              color: '#38bdf8',
              fontFamily: "'Bahnschrift', Arial, sans-serif",
              fontSize: 16,
              fontWeight: 900,
              letterSpacing: 1,
            }}
          >
            IQ
          </span>
        </div>
      </div>

      {/* ======================================================== */}
      {/* 4. REELS/SHORTS BOTTOM SAFE ZONE (CLEARED BOTTOM 310px)  */}
      {/* Container sits at bottom: 310px to avoid FB/IG handles   */}
      {/* ======================================================== */}
      <MedusaTypographyOverlay frame={frame} activeBeat={activeBeat} />

      {/* ======================================================== */}
      {/* 5. AUDIO SYNCHRONIZATION VIA REMOTION SEQUENCE           */}
      {/* ======================================================== */}
      {MEDUSA_TIMELINE.map((beat) => (
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

// ========================================================
// REELS-SAFE MINIMAL TYPOGRAPHY OVERLAY COMPONENT
// ========================================================
const MedusaTypographyOverlay: React.FC<{
  frame: number;
  activeBeat: (typeof MEDUSA_TIMELINE)[0];
}> = ({ frame, activeBeat }) => {
  if (!activeBeat) return null;

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
        bottom: 315, // STRICT SAFE ZONE: Leaves bottom 315px 100% free for Instagram/Facebook UI!
        left: 100, // Safe horizontal margin (leaves 100px on left, 100px on right for Reels action buttons)
        right: 100,
        zIndex: 100,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        textAlign: 'center',
        pointerEvents: 'none',
      }}
    >
      {/* Main Punchy Impact Hook */}
      <div
        style={{
          fontFamily: 'Bahnschrift, Arial, sans-serif',
          fontSize: 60,
          fontWeight: 900,
          color: '#ffffff',
          letterSpacing: 1.5,
          textTransform: 'uppercase',
          textShadow:
            '0 4px 20px rgba(0, 0, 0, 0.95), 0 2px 6px rgba(0, 0, 0, 0.9)',
          lineHeight: 1.1,
          marginBottom: 8,
        }}
      >
        {activeBeat.shortTitle}
      </div>

      {/* Scientific Subtitle */}
      <div
        style={{
          fontFamily: 'Consolas, monospace',
          fontSize: 26,
          fontWeight: 700,
          color: '#7dd3fc',
          letterSpacing: 2,
          textShadow: '0 2px 12px rgba(0, 0, 0, 0.9)',
          marginBottom: 18,
          textTransform: 'uppercase',
        }}
      >
        {activeBeat.subTitle}
      </div>

      {/* Narration Typewriter Ribbon (Sleek, transparent, modern glass) */}
      <div
        style={{
          backgroundColor: 'rgba(2, 10, 24, 0.88)',
          border: '1.5px solid rgba(56, 189, 248, 0.35)',
          borderRadius: 14,
          padding: '12px 28px',
          maxWidth: 860,
          fontFamily: 'Bahnschrift, Arial, sans-serif',
          fontSize: 28,
          lineHeight: 1.35,
          fontWeight: 600,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.85)',
          backdropFilter: 'blur(8px)',
        }}
      >
        <span style={{ color: '#ffffff' }}>{visibleText}</span>
        <span style={{ opacity: 0 }}>{hiddenText}</span>
      </div>
    </div>
  );
};
