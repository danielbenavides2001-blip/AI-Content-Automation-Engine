import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import React, { useMemo } from 'react';

interface Word {
  text: string;
  start: number;
  end: number;
}

interface LevelMarker {
  nivel: number;
  titulo: string;
  impacto: string;
  startTime: number;
  endTime: number;
}

const BRAND = {
  gold: '#FFD700',
  goldLight: '#FFED4A',
  goldDark: '#B8860B',
  dark: '#0D0D0D',
  darkOverlay: 'rgba(13, 13, 13, 0.85)',
  panelBg: 'rgba(13, 13, 13, 0.75)',
  textPrimary: '#FFFFFF',
  textSecondary: '#B8B8B8',
  borderGlow: 'rgba(255, 215, 0, 0.3)',
};

const impactoStyles: Record<string, { gradient: string; glow: string }> = {
  Bajo: {
    gradient: 'linear-gradient(135deg, #4CAF50, #2E7D32)',
    glow: 'rgba(76, 175, 80, 0.3)',
  },
  Medio: {
    gradient: 'linear-gradient(135deg, #FF9800, #E65100)',
    glow: 'rgba(255, 152, 0, 0.3)',
  },
  Alto: {
    gradient: 'linear-gradient(135deg, #f44336, #B71C1C)',
    glow: 'rgba(244, 67, 54, 0.4)',
  },
  Extremo: {
    gradient: 'linear-gradient(135deg, #9C27B0, #4A148C)',
    glow: 'rgba(156, 39, 176, 0.5)',
  },
};

const LevelProgressBar: React.FC<{
  currentLevel: number;
  totalLevels: number;
  currentImpact: string;
}> = ({ currentLevel, totalLevels, currentImpact }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = currentLevel / totalLevels;
  const smoothProgress = spring({
    frame,
    fps,
    config: { damping: 20, stiffness: 60 },
  });

  const pulseOpacity = interpolate(frame % 30, [0, 15, 30], [0.6, 1, 0.6]);

  const impactColor = impactoStyles[currentImpact]?.glow || 'rgba(255,215,0,0.3)';

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 30,
        left: '50%',
        transform: 'translateX(-50%)',
        width: '85%',
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        zIndex: 80,
      }}
    >
      <span
        style={{
          fontFamily: "'Segoe UI', Arial, sans-serif",
          fontSize: 12,
          fontWeight: 'bold',
          color: BRAND.gold,
          minWidth: 100,
          textAlign: 'right',
          textShadow: `0 0 10px ${impactColor}`,
          letterSpacing: 2,
        }}
      >
        NIVEL {currentLevel}/{totalLevels}
      </span>

      <div
        style={{
          flex: 1,
          height: 6,
          backgroundColor: 'rgba(255,255,255,0.1)',
          borderRadius: 3,
          overflow: 'hidden',
          position: 'relative',
        }}
      >
        <div
          style={{
            width: `${Math.min(smoothProgress, 1) * 100}%`,
            height: '100%',
            background: `linear-gradient(90deg, ${BRAND.gold}, #FFA500)`,
            borderRadius: 3,
            boxShadow: `0 0 8px ${impactColor}`,
          }}
        />
        <div
          style={{
            position: 'absolute',
            right: `${(1 - Math.min(smoothProgress, 1)) * 100}%`,
            top: -1,
            width: 3,
            height: 8,
            backgroundColor: '#FFF',
            borderRadius: 2,
            opacity: pulseOpacity,
            filter: 'blur(1px)',
          }}
        />
      </div>
    </div>
  );
};

const StepIndicator: React.FC<{
  levelMarkers: LevelMarker[];
  currentMs: number;
  activeNivel: number | null;
}> = ({ levelMarkers, currentMs, activeNivel }) => {
  return (
    <div
      style={{
        display: 'flex',
        gap: 5,
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 6,
      }}
    >
      {levelMarkers.map((lm, i) => {
        const isCompleted = lm.endTime <= currentMs;
        const isActive = lm.nivel === activeNivel;
        return (
          <div
            key={i}
            style={{
              width: isActive ? 22 : 8,
              height: 3,
              borderRadius: 2,
              backgroundColor: isActive
                ? BRAND.gold
                : isCompleted
                ? BRAND.goldDark
                : 'rgba(255,255,255,0.12)',
              boxShadow: isActive ? `0 0 6px ${BRAND.gold}` : 'none',
              transition: 'none',
            }}
          />
        );
      })}
    </div>
  );
};

export const Subtitles: React.FC<{
  words: Word[];
  intrigueHeader?: string;
  levelMarkers?: LevelMarker[];
}> = ({ words, intrigueHeader, levelMarkers }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentMs = (frame / fps) * 1000;
  const delayMs = 100;

  // Build visible words: all started words, capped to a rolling window
  const visibleWords = useMemo(() => {
    const result: { word: Word; wStart: number; wEnd: number; }[] = [];
    for (const w of words) {
      const wStart = ((w.start + delayMs) / 1000) * fps;
      const wEnd = ((w.end + delayMs) / 1000) * fps;
      if (frame >= wStart) {
        result.push({ word: w, wStart, wEnd });
      }
    }
    // Show last ~25 words max to avoid clutter
    if (result.length > 25) {
      return result.slice(-25);
    }
    return result;
  }, [words, frame, fps]);

  const activeLevel = levelMarkers?.find(
    (l) => currentMs >= l.startTime && currentMs < l.endTime
  );

  // --- Intrigue Header timing ---
  const INTRIGUE_HOLD_FRAMES = 4 * fps;
  const INTRIGUE_FADE_FRAMES = Math.round(0.5 * fps);
  const totalIntrigueFrames = INTRIGUE_HOLD_FRAMES + INTRIGUE_FADE_FRAMES;

  const headerEntrance = spring({
    frame: Math.min(frame, INTRIGUE_FADE_FRAMES),
    fps,
    config: { damping: 15, mass: 0.4, stiffness: 120 },
  });

  const headerScale = interpolate(
    Math.min(frame, INTRIGUE_FADE_FRAMES),
    [0, INTRIGUE_FADE_FRAMES],
    [1.3, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const headerOpacity =
    frame < INTRIGUE_FADE_FRAMES
      ? interpolate(frame, [0, INTRIGUE_FADE_FRAMES], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        })
      : frame > INTRIGUE_HOLD_FRAMES
      ? interpolate(
          frame,
          [INTRIGUE_HOLD_FRAMES, totalIntrigueFrames],
          [1, 0],
          { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
        )
      : 1;

  const showIntrigueBig = frame < totalIntrigueFrames && headerOpacity > 0;

  const miniBarOpacity =
    frame > INTRIGUE_HOLD_FRAMES
      ? interpolate(
          frame,
          [INTRIGUE_HOLD_FRAMES, totalIntrigueFrames],
          [0, 0.7],
          { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
        )
      : 0;

  const showMiniBar = frame > INTRIGUE_HOLD_FRAMES - 5;

  // --- Level transition animation ---
  const [prevLevel, setPrevLevel] = React.useState<number | null>(null);
  const [isTransitioning, setIsTransitioning] = React.useState(false);

  React.useEffect(() => {
    if (activeLevel && activeLevel.nivel !== prevLevel) {
      setIsTransitioning(true);
      const timeout = setTimeout(() => {
        setPrevLevel(activeLevel.nivel);
        setIsTransitioning(false);
      }, 250);
      return () => clearTimeout(timeout);
    }
  }, [activeLevel, prevLevel]);

  const levelExitOpacity = isTransitioning
    ? interpolate(frame % 8, [0, 8], [1, 0], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      })
    : 1;

  const levelEnterOpacity = isTransitioning
    ? interpolate(frame % 8, [0, 8], [0, 1], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      })
    : 1;

  const levelSlideOffset = isTransitioning
    ? interpolate(frame % 8, [0, 8], [20, 0], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      })
    : 0;

  const currentLevelEntry = activeLevel && !isTransitioning;
  const transitioningToNew = isTransitioning;

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: 'transparent',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* === Subtle letterbox gradients === */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: 500,
          background:
            'linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.25) 40%, transparent 100%)',
          zIndex: 2,
          pointerEvents: 'none',
        }}
      />
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: 120,
          background:
            'linear-gradient(to bottom, rgba(0,0,0,0.5) 0%, transparent 100%)',
          zIndex: 2,
          pointerEvents: 'none',
        }}
      />

      {/* === Intrigue Header — Big Reveal === */}
      {showIntrigueBig && intrigueHeader && (
        <div
          style={{
            position: 'absolute',
            top: 280,
            left: '50%',
            transform: `translateX(-50%) scale(${headerScale})`,
            opacity: headerOpacity * headerEntrance,
            zIndex: 100,
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              backgroundColor: BRAND.darkOverlay,
              padding: '16px 48px',
              borderRadius: '12px',
              border: `2px solid ${BRAND.borderGlow}`,
              boxShadow: `0 8px 32px rgba(0,0,0,0.5), 0 0 40px ${BRAND.gold}22`,
              textAlign: 'center',
            }}
          >
            <span
              style={{
                color: BRAND.textPrimary,
                fontFamily: "'Arial Black', Impact, sans-serif",
                fontSize: 64,
                textTransform: 'uppercase',
                letterSpacing: 6,
                textShadow: `0 0 30px ${BRAND.gold}44, 2px 2px 0 ${BRAND.dark}`,
                lineHeight: 1.1,
              }}
            >
              {intrigueHeader}
            </span>
          </div>
        </div>
      )}

      {/* === Intrigue Header — Persistent Mini Bar === */}
      {showMiniBar && intrigueHeader && (
        <div
          style={{
            position: 'absolute',
            top: 16,
            left: '50%',
            transform: 'translateX(-50%)',
            opacity: miniBarOpacity,
            zIndex: 100,
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              padding: '4px 20px',
              backgroundColor: 'rgba(0,0,0,0.5)',
              borderRadius: '20px',
              border: `1px solid ${BRAND.borderGlow}`,
              backdropFilter: 'blur(4px)',
            }}
          >
            <span
              style={{
                fontSize: 14,
                color: BRAND.gold,
                letterSpacing: 4,
                fontFamily: "'Segoe UI', Arial, sans-serif",
                fontWeight: 'bold',
                textTransform: 'uppercase',
              }}
            >
              {intrigueHeader}
            </span>
          </div>
        </div>
      )}

      {/* === Level Badge === */}
      {activeLevel && (
        <div
          style={{
            position: 'absolute',
            top: 200,
            left: '50%',
            transform: `translateX(-50%)`,
            zIndex: 90,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '6px',
            opacity: transitioningToNew ? levelEnterOpacity : levelExitOpacity,
          }}
        >
          {transitioningToNew && (
            <div
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '6px',
                opacity: levelExitOpacity,
                transform: `translateY(-${levelSlideOffset}px)`,
              }}
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  backgroundColor: BRAND.panelBg,
                  padding: '8px 20px',
                  borderRadius: '50px',
                  border: `2px solid ${BRAND.borderGlow}`,
                }}
              >
                <span
                  style={{
                    fontFamily: "'Arial Black', Impact, sans-serif",
                    fontSize: 46,
                    color: BRAND.gold,
                    textShadow: '2px 2px 0 #000',
                  }}
                >
                  NIVEL {prevLevel}
                </span>
              </div>
            </div>
          )}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              backgroundColor: BRAND.panelBg,
              padding: '8px 20px',
              borderRadius: '50px',
              border: `2px solid ${BRAND.borderGlow}`,
              opacity: transitioningToNew ? levelEnterOpacity : 1,
              transform: transitioningToNew
                ? `translateY(${levelSlideOffset}px)`
                : 'translateY(0)',
            }}
          >
            <span
              style={{
                fontFamily: "'Arial Black', Impact, sans-serif",
                fontSize: 46,
                color: BRAND.gold,
                textShadow: '2px 2px 0 #000',
              }}
            >
              NIVEL {activeLevel.nivel}
            </span>
            <span
              style={{
                fontFamily: "'Segoe UI', Arial, sans-serif",
                fontSize: 11,
                fontWeight: 'bold',
                color: '#FFFFFF',
                background: impactoStyles[activeLevel.impacto]?.gradient || '#666',
                padding: '3px 10px',
                borderRadius: '20px',
                textTransform: 'uppercase',
                letterSpacing: 1,
                boxShadow: `0 0 12px ${
                  impactoStyles[activeLevel.impacto]?.glow || 'transparent'
                }`,
              }}
            >
              {activeLevel.impacto}
            </span>
          </div>
          {activeLevel.titulo && (
            <span
              style={{
                fontFamily: "'Segoe UI', Arial, sans-serif",
                fontSize: 22,
                color: BRAND.textSecondary,
                textShadow: '2px 2px 3px rgba(0,0,0,1)',
                backgroundColor: 'rgba(0,0,0,0.5)',
                padding: '3px 14px',
                borderRadius: '20px',
                maxWidth: '80%',
                textAlign: 'center',
                lineHeight: 1.3,
              }}
            >
              {activeLevel.titulo}
            </span>
          )}

          {/* Step indicator dots */}
          {levelMarkers && levelMarkers.length > 0 && (
            <StepIndicator
              levelMarkers={levelMarkers}
              currentMs={currentMs}
              activeNivel={activeLevel.nivel}
            />
          )}
        </div>
      )}

      {/* === Subtitles: Word-by-word karaoke === */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-end',
          paddingBottom: 130,
          zIndex: 50,
          pointerEvents: 'none',
        }}
      >
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
            gap: '6px 16px',
            maxWidth: '92%',
          }}
        >
          {visibleWords.map((item, i) => {
            const isCurrent = frame >= item.wStart && frame < item.wEnd;
            const isPast = frame >= item.wEnd;
            const framesSinceEnd = frame - item.wEnd;

            // Entrance spring
            const wordFrame = Math.max(0, frame - item.wStart);
            const entrance = spring({
              frame: wordFrame,
              fps,
              config: { damping: 14, mass: 0.4, stiffness: 120 },
            });

            // Opacity: fade in at start, fade out gradually after end
            let opacity: number;
            if (isCurrent) {
              opacity = interpolate(entrance, [0, 1], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
            } else {
              opacity = interpolate(framesSinceEnd, [0, 8], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
            }

            if (opacity <= 0.02) return null;

            const scale = isCurrent
              ? interpolate(entrance, [0, 1], [0.88, 1], { extrapolateLeft: 'clamp' })
              : 0.96;

            return (
              <span
                key={i}
                style={{
                  fontSize: 56,
                  fontFamily: "'Arial Black', Impact, sans-serif",
                  fontWeight: 'bold',
                  color: isCurrent ? BRAND.gold : BRAND.textPrimary,
                  textTransform: 'uppercase',
                  display: 'inline-block',
                  lineHeight: 1.5,
                  letterSpacing: '1px',
                  textShadow: isCurrent
                    ? `0 0 20px ${BRAND.gold}66, 2px 2px 8px rgba(0,0,0,0.9)`
                    : '2px 2px 8px rgba(0,0,0,0.9)',
                  opacity,
                  transform: `scale(${scale})`,
                }}
              >
                {item.word.text}
              </span>
            );
          })}
        </div>
      </div>

      {/* === Progress Bar === */}
      {levelMarkers && levelMarkers.length > 0 && activeLevel && (
        <LevelProgressBar
          currentLevel={activeLevel.nivel}
          totalLevels={levelMarkers.length}
          currentImpact={activeLevel.impacto}
        />
      )}
    </div>
  );
};