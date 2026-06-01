import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import React from 'react';

interface Word {
  text: string;
  start: number; // in ms
  end: number; // in ms
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

export const Trivias: React.FC<{
  words: Word[];
  intrigueHeader?: string;
  triviaScenes?: TriviaScene[];
}> = ({ words, intrigueHeader, triviaScenes = [] }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  // 1. Find the active scene in the timeline
  const activeScene = triviaScenes.find(
    (s) => currentTime >= s.start_time && currentTime < s.end_time
  );

  // 2. Phrase-by-phrase subtitles grouping (3 words per chunk for rapid viral style)
  const phrases: { words: Word[]; start: number; end: number }[] = [];
  for (let i = 0; i < words.length; i += 3) {
    const chunk = words.slice(i, i + 3);
    phrases.push({
      words: chunk,
      start: chunk[0].start,
      end: chunk[chunk.length - 1].end,
    });
  }

  // 3. Determine game stage if in a trivia scene with options
  let stage: 'question' | 'timer' | 'answer' = 'question';
  let relativeTime = 0;
  let timerRemaining = 3.0;

  if (activeScene && activeScene.options && activeScene.options.length > 0) {
    relativeTime = currentTime - activeScene.start_time;
    if (relativeTime < activeScene.q_dur) {
      stage = 'question';
    } else if (relativeTime < activeScene.q_dur + 3.0) {
      stage = 'timer';
      timerRemaining = Math.max(0, 3.0 - (relativeTime - activeScene.q_dur));
    } else {
      stage = 'answer';
    }
  }

  // Circular progress configuration for the timer ring
  const circleRadius = 50;
  const strokeWidth = 8;
  const circumference = 2 * Math.PI * circleRadius;
  const progressRatio = stage === 'timer' ? timerRemaining / 3.0 : 0;
  const strokeDashoffset = circumference * (1 - progressRatio);

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: 'transparent',
        position: 'relative',
        overflow: 'hidden',
        fontFamily: "'Outfit', 'Inter', sans-serif",
      }}
    >
      {/* 1. Global Intrigue / Category Header */}
      {intrigueHeader && (
        <div
          style={{
            position: 'absolute',
            top: 100,
            left: '50%',
            transform: 'translateX(-50%)',
            backgroundColor: 'rgba(10, 15, 30, 0.8)',
            border: '2px solid rgba(0, 242, 254, 0.6)',
            boxShadow: '0 8px 32px 0 rgba(0, 242, 254, 0.25)',
            padding: '12px 35px',
            borderRadius: '40px',
            zIndex: 100,
            width: '80%',
            textAlign: 'center',
            backdropFilter: 'blur(12px)',
          }}
        >
          <span
            style={{
              color: '#00f2fe',
              fontSize: 32,
              fontWeight: 900,
              letterSpacing: '4px',
              textTransform: 'uppercase',
              textShadow: '0 0 10px rgba(0, 242, 254, 0.5)',
            }}
          >
            {intrigueHeader}
          </span>
        </div>
      )}

      {/* 2. Trivia Interactive Dashboard */}
      {activeScene && activeScene.question && (
        <div
          style={{
            position: 'absolute',
            top: 240,
            left: '5%',
            width: '90%',
            display: 'flex',
            flexDirection: 'column',
            gap: '30px',
            zIndex: 80,
          }}
        >
          {/* Question Box (Frosted Glassmorphism) */}
          <div
            style={{
              backgroundColor: 'rgba(15, 23, 42, 0.85)',
              borderRadius: '24px',
              padding: '30px 25px',
              border: '2px solid rgba(255, 255, 255, 0.1)',
              boxShadow: '0 20px 40px rgba(0,0,0,0.5)',
              backdropFilter: 'blur(20px)',
              textAlign: 'center',
            }}
          >
            <h2
              style={{
                color: '#FFFFFF',
                fontSize: 36,
                fontWeight: 800,
                margin: 0,
                lineHeight: 1.3,
                letterSpacing: '-0.5px',
              }}
            >
              {activeScene.question}
            </h2>
          </div>

          {/* Options Grid/List */}
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '15px',
              position: 'relative',
            }}
          >
            {activeScene.options.map((option, index) => {
              const badgeColors = ['#f43f5e', '#3b82f6', '#10b981', '#f59e0b'];
              const badgeLetter = ['A', 'B', 'C', 'D'][index];
              const isCorrectOption = option === activeScene.correct_answer;

              // Styles according to game stage
              let cardBg = 'rgba(15, 23, 42, 0.8)';
              let cardBorder = '2px solid rgba(255, 255, 255, 0.08)';
              let cardShadow = '0 10px 25px rgba(0, 0, 0, 0.3)';
              let opacity = 1;
              let scale = 1;

              if (stage === 'answer') {
                if (isCorrectOption) {
                  cardBg = 'rgba(16, 185, 129, 0.25)';
                  cardBorder = '2.5px solid #10b981';
                  cardShadow = '0 0 25px rgba(16, 185, 129, 0.6)';
                  scale = 1.03; // Correct option jumps up slightly
                } else {
                  opacity = 0.35; // Dim incorrect options
                }
              }

              return (
                <div
                  key={index}
                  style={{
                    backgroundColor: cardBg,
                    border: cardBorder,
                    boxShadow: cardShadow,
                    opacity: opacity,
                    transform: `scale(${scale})`,
                    transition: 'all 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
                    borderRadius: '16px',
                    padding: '18px 24px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '20px',
                    backdropFilter: 'blur(16px)',
                  }}
                >
                  {/* Badge Circle (A, B, C, D) */}
                  <div
                    style={{
                      width: '48px',
                      height: '48px',
                      borderRadius: '50%',
                      backgroundColor: isCorrectOption && stage === 'answer' ? '#10b981' : badgeColors[index],
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
                      flexShrink: 0,
                      transition: 'background-color 0.3s ease',
                    }}
                  >
                    <span
                      style={{
                        color: '#FFFFFF',
                        fontSize: 24,
                        fontWeight: 900,
                      }}
                    >
                      {badgeLetter}
                    </span>
                  </div>

                  {/* Option Text */}
                  <span
                    style={{
                      color: isCorrectOption && stage === 'answer' ? '#10b981' : '#E2E8F0',
                      fontSize: 30,
                      fontWeight: isCorrectOption && stage === 'answer' ? 800 : 600,
                      lineHeight: 1.2,
                      transition: 'color 0.3s ease',
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

      {/* 3. Circular Countdown Overlay */}
      {stage === 'timer' && (
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 90,
          }}
        >
          {/* circular glassmorphic ring container */}
          <div
            style={{
              position: 'relative',
              width: '140px',
              height: '140px',
              borderRadius: '50%',
              backgroundColor: 'rgba(10, 15, 30, 0.85)',
              backdropFilter: 'blur(15px)',
              border: '2px solid rgba(255, 255, 255, 0.08)',
              boxShadow: '0 0 40px rgba(0, 0, 0, 0.6)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {/* SVG Ring */}
            <svg
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                transform: 'rotate(-90deg)',
              }}
              width="140"
              height="140"
            >
              {/* Trailing Track */}
              <circle
                cx="70"
                cy="70"
                r={circleRadius}
                fill="transparent"
                stroke="rgba(255,255,255,0.06)"
                strokeWidth={strokeWidth}
              />
              {/* Draining Ring */}
              <circle
                cx="70"
                cy="70"
                r={circleRadius}
                fill="transparent"
                stroke="#00f2fe"
                strokeWidth={strokeWidth}
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                style={{
                  filter: 'drop-shadow(0px 0px 8px rgba(0, 242, 254, 0.8))',
                  transition: 'stroke-dashoffset 0.05s linear',
                }}
              />
            </svg>

            {/* Pulsing Count Text */}
            <span
              style={{
                color: '#ffffff',
                fontSize: 64,
                fontWeight: 900,
                textAlign: 'center',
                textShadow: '0 0 15px rgba(0, 242, 254, 0.6)',
              }}
            >
              {Math.ceil(timerRemaining)}
            </span>
          </div>
        </div>
      )}

      {/* 4. Global Word-by-Word Narration Subtitles */}
      {phrases.map((phrase, pi) => {
        const startFrame = (phrase.start / 1000) * fps;
        const endFrame = (phrase.end / 1000) * fps;
        const isActivePhrase = frame >= startFrame && frame < endFrame;

        if (!isActivePhrase) return null;

        return (
          <div
            key={pi}
            style={{
              position: 'absolute',
              inset: 0,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'flex-end',
              paddingBottom: 220, // High enough so standard social widgets do not overlap
              zIndex: 99,
            }}
          >
            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                justifyContent: 'center',
                gap: '10px 25px',
                maxWidth: '90%',
                backgroundColor: 'rgba(15, 23, 42, 0.6)',
                padding: '12px 30px',
                borderRadius: '24px',
                backdropFilter: 'blur(8px)',
                border: '1px solid rgba(255, 255, 255, 0.05)',
              }}
            >
              {phrase.words.map((word, wi) => {
                const wStart = (word.start / 1000) * fps;
                const wEnd = (word.end / 1000) * fps;
                const isCurrentWord = frame >= wStart && frame < wEnd;

                return (
                  <span
                    key={wi}
                    style={{
                      fontSize: 56,
                      fontFamily: "'Outfit', 'Inter', sans-serif",
                      fontWeight: 900,
                      color: isCurrentWord ? '#FFFF00' : '#FFFFFF',
                      textTransform: 'uppercase',
                      display: 'inline-block',
                      lineHeight: 1.0,
                      textShadow: '4px 4px 6px rgba(0,0,0,0.8)',
                    }}
                  >
                    {word.text}
                  </span>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
};
