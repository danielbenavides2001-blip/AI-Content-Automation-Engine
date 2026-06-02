import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import React, { useMemo } from 'react';

interface Word {
  text: string;
  start: number;
  end: number;
}

interface TriviaScene {
  scene_number: number;
  question: string;
  options: string[];
  correct_answer: string;
  q_dur: number;
  a_dur: number;
  start_time: number;
  end_time: number;
}

interface Particle {
  x: number;
  y: number;
  size: number;
  opacity: number;
  speed: number;
  delay: number;
}

export const Trivias: React.FC<{
  words: Word[];
  intrigueHeader?: string;
  triviaScenes?: TriviaScene[];
}> = ({ words, intrigueHeader, triviaScenes = [] }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const currentTime = frame / fps;

  const activeScene = triviaScenes.find(
    (s) => currentTime >= s.start_time && currentTime < s.end_time
  );

  // If current scene has no question (intro/outro), show the nearest question
  // scene immediately so the viewer never sees blank screen with voice only.
  let displayScene = activeScene;
  if (!displayScene || !displayScene.question) {
    const nextQs = triviaScenes.find(
      (s) => s.question && s.end_time > currentTime
    );
    if (nextQs) displayScene = nextQs;
  }

  let stage: 'question' | 'timer' | 'answer' = 'question';
  let relativeTime = 0;
  let timerRemaining = 3.0;

  if (displayScene && displayScene.options && displayScene.options.length > 0) {
    relativeTime = currentTime - displayScene.start_time;
    if (relativeTime < displayScene.q_dur) {
      stage = 'question';
    } else if (relativeTime < displayScene.q_dur + 3.0) {
      stage = 'timer';
      timerRemaining = Math.max(0, 3.0 - (relativeTime - displayScene.q_dur));
    } else {
      stage = 'answer';
    }
  }

  const circleRadius = 60;
  const strokeWidth = 8;
  const circumference = 2 * Math.PI * circleRadius;
  const progressRatio = stage === 'timer' ? timerRemaining / 3.0 : 0;
  const strokeDashoffset = circumference * (1 - progressRatio);

  const timerPulse = stage === 'timer'
    ? 1 + 0.08 * Math.sin(frame * 0.4)
    : 1;

  const particles = useMemo(() => {
    const items: Particle[] = [];
    for (let i = 0; i < 30; i++) {
      items.push({
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: 1.5 + Math.random() * 3,
        opacity: 0.15 + Math.random() * 0.35,
        speed: 0.2 + Math.random() * 0.5,
        delay: Math.random() * 100,
      });
    }
    return items;
  }, []);

  const optionLabels = ['A', 'B', 'C', 'D'];

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: 'transparent',
        position: 'relative',
        overflow: 'hidden',
        fontFamily: "'Inter', 'Segoe UI', sans-serif",
      }}
    >
      {/* Particles overlay */}
      <div style={{ position: 'absolute', inset: 0, zIndex: 1, pointerEvents: 'none' }}>
        {particles.map((p, i) => {
          const yOffset = (frame * p.speed + p.delay * 10) % 1200 - 100;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: `${p.x}%`,
                top: `${(yOffset / 1200) * 100}%`,
                width: p.size,
                height: p.size,
                borderRadius: '50%',
                backgroundColor: 'rgba(255, 255, 255, 0.6)',
                opacity: p.opacity * (0.5 + 0.5 * Math.sin(frame * 0.02 + p.delay)),
                boxShadow: `0 0 ${p.size * 2}px rgba(255, 255, 255, 0.3)`,
              }}
            />
          );
        })}
      </div>

      {/* Intrigue header */}
      {intrigueHeader && (
        <div
          style={{
            position: 'absolute',
            top: 40,
            left: '50%',
            transform: 'translateX(-50%)',
            zIndex: 10,
            padding: '8px 24px',
            borderRadius: 20,
            backgroundColor: 'rgba(255, 255, 255, 0.15)',
            backdropFilter: 'blur(8px)',
          }}
        >
          <span
            style={{
              color: '#ffffff',
              fontSize: 22,
              fontWeight: 700,
              letterSpacing: 2,
              textTransform: 'uppercase',
              textShadow: '0 2px 8px rgba(0,0,0,0.3)',
            }}
          >
            {intrigueHeader}
          </span>
        </div>
      )}

      {/* Quiz content */}
      {displayScene && displayScene.question && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 5,
            padding: '0 24px',
          }}
        >
          {/* Question box */}
          <div
            style={{
              width: '100%',
              maxWidth: 620,
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              borderRadius: 28,
              padding: '36px 40px',
              boxShadow: '0 12px 48px rgba(0,0,0,0.2)',
              marginBottom: 48,
            }}
          >
            <h2
              style={{
                color: '#1a1a2e',
                fontSize: 52,
                fontWeight: 800,
                margin: 0,
                lineHeight: 1.3,
                textAlign: 'center',
                letterSpacing: '-0.5px',
              }}
            >
              {displayScene.question}
            </h2>
          </div>

          {/* Timer circle */}
          {stage === 'timer' && (
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: 48,
                transform: `scale(${timerPulse})`,
              }}
            >
              <div
                style={{
                  position: 'relative',
                  width: 170,
                  height: 170,
                  borderRadius: '50%',
                  backgroundColor: 'rgba(255, 255, 255, 0.15)',
                  backdropFilter: 'blur(16px)',
                  border: '3px solid rgba(255, 255, 255, 0.25)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <svg
                  style={{ position: 'absolute', top: 0, left: 0, transform: 'rotate(-90deg)' }}
                  width="170"
                  height="170"
                >
                  <circle
                    cx="85"
                    cy="85"
                    r={circleRadius}
                    fill="transparent"
                    stroke="rgba(255,255,255,0.1)"
                    strokeWidth={strokeWidth}
                  />
                  <circle
                    cx="85"
                    cy="85"
                    r={circleRadius}
                    fill="transparent"
                    stroke="#fbbf24"
                    strokeWidth={strokeWidth}
                    strokeDasharray={circumference}
                    strokeDashoffset={strokeDashoffset}
                    strokeLinecap="round"
                    style={{
                      filter: 'drop-shadow(0px 0px 12px rgba(251, 191, 36, 0.7))',
                      transition: 'stroke-dashoffset 0.05s linear',
                    }}
                  />
                </svg>
                <span
                  style={{
                    color: '#ffffff',
                    fontSize: 68,
                    fontWeight: 900,
                    textShadow: '0 0 24px rgba(251, 191, 36, 0.6)',
                  }}
                >
                  {Math.ceil(timerRemaining)}
                </span>
              </div>
            </div>
          )}

          {/* Options */}
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: 20,
              width: '100%',
              maxWidth: 620,
            }}
          >
            {displayScene.options.map((option, index) => {
              const isCorrectOption = option === displayScene.correct_answer;
              const isRevealed = stage === 'answer';

              let bg = 'rgba(255, 255, 255, 0.92)';
              let borderColor = 'rgba(0, 0, 0, 0.1)';
              let textColor = '#1a1a2e';
              let badgeBg = '#e2e8f0';
              let badgeText = '#1a1a2e';

              if (isRevealed) {
                if (isCorrectOption) {
                  bg = 'rgba(251, 191, 36, 0.95)';
                  borderColor = '#f59e0b';
                  badgeBg = '#ffffff';
                  badgeText = '#1a1a2e';
                  textColor = '#1a1a2e';
                } else {
                  bg = 'rgba(255, 255, 255, 0.3)';
                  borderColor = 'rgba(0, 0, 0, 0.05)';
                  textColor = 'rgba(26, 26, 46, 0.3)';
                  badgeBg = 'rgba(226, 232, 240, 0.3)';
                  badgeText = 'rgba(26, 26, 46, 0.3)';
                }
              }

              return (
                <div
                  key={index}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 20,
                    backgroundColor: bg,
                    borderRadius: 20,
                    padding: '24px 28px',
                    border: `3px solid ${borderColor}`,
                    boxShadow: isRevealed && isCorrectOption
                      ? '0 0 32px rgba(251, 191, 36, 0.6)'
                      : '0 6px 16px rgba(0,0,0,0.1)',
                    transition: 'all 0.4s ease',
                  }}
                >
                  <div
                    style={{
                      width: 60,
                      height: 60,
                      borderRadius: '50%',
                      backgroundColor: badgeBg,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0,
                    }}
                  >
                    <span
                      style={{
                        color: badgeText,
                        fontSize: 28,
                        fontWeight: 800,
                      }}
                    >
                      {optionLabels[index]}
                    </span>
                  </div>
                  <span
                    style={{
                      color: textColor,
                      fontSize: 40,
                      fontWeight: 700,
                      lineHeight: 1.2,
                    }}
                  >
                    {option.replace(/^[A-D]\)\s*/i, '')}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
