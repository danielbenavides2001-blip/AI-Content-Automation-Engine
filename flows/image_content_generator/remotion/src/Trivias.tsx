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
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -60%)', // Centered vertically & horizontally
            width: '90%',
            display: 'flex',
            flexDirection: 'column',
            gap: '40px',
            zIndex: 80,
          }}
        >
          {/* Question Box (Frosted Glassmorphism) */}
          <div
            style={{
              backgroundColor: 'rgba(15, 23, 42, 0.9)',
              borderRadius: '30px',
              padding: '40px 35px',
              border: '2.5px solid rgba(255, 255, 255, 0.15)',
              boxShadow: '0 25px 50px rgba(0,0,0,0.6)',
              backdropFilter: 'blur(25px)',
              textAlign: 'center',
            }}
          >
            <h2
              style={{
                color: '#FFFFFF',
                fontSize: 48, // Increased from 36
                fontWeight: 900,
                margin: 0,
                lineHeight: 1.35,
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
              gap: '20px',
              position: 'relative',
            }}
          >
            {activeScene.options.map((option, index) => {
              const badgeColors = ['#f43f5e', '#3b82f6', '#10b981', '#f59e0b'];
              const badgeLetter = ['A', 'B', 'C', 'D'][index];
              const isCorrectOption = option === activeScene.correct_answer;

              // Styles according to game stage
              let cardBg = 'rgba(15, 23, 42, 0.88)';
              let cardBorder = '2px solid rgba(255, 255, 255, 0.1)';
              let cardShadow = '0 12px 30px rgba(0, 0, 0, 0.4)';
              let opacity = 1;
              let scale = 1;

              if (stage === 'answer') {
                if (isCorrectOption) {
                  cardBg = 'rgba(16, 185, 129, 0.35)';
                  cardBorder = '3px solid #10b981';
                  cardShadow = '0 0 35px rgba(16, 185, 129, 0.7)';
                  scale = 1.05; // Correct option jumps up slightly
                } else {
                  opacity = 0.25; // Dim incorrect options
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
                    borderRadius: '20px',
                    padding: '24px 30px', // Extra padding
                    display: 'flex',
                    alignItems: 'center',
                    gap: '25px',
                    backdropFilter: 'blur(20px)',
                  }}
                >
                  {/* Badge Circle (A, B, C, D) */}
                  <div
                    style={{
                      width: '60px',
                      height: '60px',
                      borderRadius: '50%',
                      backgroundColor: isCorrectOption && stage === 'answer' ? '#10b981' : badgeColors[index],
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      boxShadow: '0 5px 15px rgba(0, 0, 0, 0.4)',
                      flexShrink: 0,
                      transition: 'background-color 0.3s ease',
                    }}
                  >
                    <span
                      style={{
                        color: '#FFFFFF',
                        fontSize: 32, // Increased from 24
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
                      fontSize: 38, // Increased from 30
                      fontWeight: isCorrectOption && stage === 'answer' ? 900 : 700,
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

      {/* 3. Circular Countdown Overlay — Below options, right-aligned */}
      {stage === 'timer' && (
        <div
          style={{
            position: 'absolute',
            bottom: 260,
            right: 40,
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
              width: '100px',
              height: '100px',
              borderRadius: '50%',
              backgroundColor: 'rgba(10, 15, 30, 0.85)',
              backdropFilter: 'blur(20px)',
              border: '2px solid rgba(255, 255, 255, 0.1)',
              boxShadow: '0 0 30px rgba(0, 0, 0, 0.7)',
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
              width="100"
              height="100"
            >
              {/* Trailing Track */}
              <circle
                cx="50"
                cy="50"
                r={38}
                fill="transparent"
                stroke="rgba(255,255,255,0.06)"
                strokeWidth={6}
              />
              {/* Draining Ring */}
              <circle
                cx="50"
                cy="50"
                r={38}
                fill="transparent"
                stroke="#00f2fe"
                strokeWidth={6}
                strokeDasharray={2 * Math.PI * 38}
                strokeDashoffset={2 * Math.PI * 38 * (1 - progressRatio)}
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
                fontSize: 42,
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
        // Compensate subtitle timing dynamically (delaying text sync to align perfectly with speech)
        const delayMs = 350; 
        const startFrame = ((phrase.start + delayMs) / 1000) * fps;
        const endFrame = ((phrase.end + delayMs) / 1000) * fps;
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
                const wStart = ((word.start + delayMs) / 1000) * fps;
                const wEnd = ((word.end + delayMs) / 1000) * fps;
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
