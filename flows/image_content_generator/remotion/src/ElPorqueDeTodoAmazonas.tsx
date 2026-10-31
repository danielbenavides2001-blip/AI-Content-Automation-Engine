import React from 'react';
import {
  Audio,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import { AmazonasMap } from './components_amazonas/AmazonasMap';
import { FloodExpansionDiagram } from './components_amazonas/FloodExpansionDiagram';
import { GeotechnicalCrossSection } from './components_amazonas/GeotechnicalCrossSection';
import { RainforestLogistics } from './components_amazonas/RainforestLogistics';
import { AMAZONAS_TIMELINE } from './amazonas_timeline';

export const ElPorqueDeTodoAmazonas: React.FC = () => {
  const frame = useCurrentFrame();

  // Find active narrative beat
  const activeBeat =
    AMAZONAS_TIMELINE.find(
      (b) => frame >= b.startFrame && frame < b.startFrame + b.durationFrames
    ) || AMAZONAS_TIMELINE[AMAZONAS_TIMELINE.length - 1];

  const localFrame = frame - activeBeat.startFrame;
  const localProgress = Math.min(1, Math.max(0, localFrame / activeBeat.durationFrames));

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: '#020914',
        position: 'relative',
        width: 1080,
        height: 1920,
        overflow: 'hidden',
      }}
    >
      {/* ======================================================== */}
      {/* 1. DYNAMIC VISUAL SCENES BY NARRATIVE BEAT               */}
      {/* ======================================================== */}
      {activeBeat.id === 'amazonas_b1' && (
        <AmazonasMap
          frame={frame}
          zoomProgress={interpolate(localProgress, [0.1, 0.6], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          })}
          scanProgress={interpolate(localProgress, [0.35, 0.95], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          })}
        />
      )}

      {activeBeat.id === 'amazonas_b2' && (
        <FloodExpansionDiagram
          frame={frame}
          progress={interpolate(localProgress, [0.2, 0.85], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          })}
        />
      )}

      {activeBeat.id === 'amazonas_b3' && (
        <GeotechnicalCrossSection frame={frame} />
      )}

      {activeBeat.id === 'amazonas_b4' && (
        <RainforestLogistics frame={frame} mode="logistics" />
      )}

      {activeBeat.id === 'amazonas_b5' && (
        <RainforestLogistics frame={frame} mode="ponte_negro" />
      )}

      {/* ======================================================== */}
      {/* 2. REELS/SHORTS TOP SAFE ZONE (ABOVE y=160px)            */}
      {/* ======================================================== */}
      {/* Category Tag (Placed safely at top: 170px) */}
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
          ENIGMAIQ  •  GEOGRAFÍA
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
          LONGITUD: 6.400 KM  |  RÍO AMAZONAS
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
            backgroundColor: '#020914',
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
      {/* 3. REELS/SHORTS BOTTOM SAFE ZONE (CLEARED BOTTOM 315px)  */}
      {/* Container sits at bottom: 315px to avoid FB/IG handles   */}
      {/* ======================================================== */}
      <AmazonasTypographyOverlay frame={frame} activeBeat={activeBeat} />

      {/* ======================================================== */}
      {/* 4. AUDIO SYNCHRONIZATION VIA REMOTION SEQUENCE           */}
      {/* ======================================================== */}
      {AMAZONAS_TIMELINE.map((beat) => (
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
const AmazonasTypographyOverlay: React.FC<{
  frame: number;
  activeBeat: (typeof AMAZONAS_TIMELINE)[0];
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
        bottom: 315, // STRICT SAFE ZONE: Clears the bottom 315px for Instagram/Facebook UI!
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
          fontSize: 58,
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

      {/* Subtitle Line */}
      <div
        style={{
          fontFamily: 'Consolas, monospace',
          fontSize: 26,
          fontWeight: 700,
          color: '#38bdf8',
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
          backgroundColor: 'rgba(2, 9, 20, 0.88)',
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
