import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { DynamicScene } from './types';

export const SceneCommunityPoll: React.FC<{
  scene: DynamicScene;
  primaryColor?: string;
  secondaryColor?: string;
  accentColor?: string;
}> = ({
  scene,
  primaryColor = '#00f5ff',
  secondaryColor = '#38bdf8',
  accentColor = '#f59e0b'
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14, stiffness: 85 } });
  const pulse = Math.sin(frame * 0.15) * 0.15 + 0.85;

  // Staggered percentage rise
  const voteA = interpolate(frame, [15, 60], [0, 57], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const voteB = interpolate(frame, [15, 60], [0, 43], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '110px 40px 320px 40px',
        boxSizing: 'border-box',
        fontFamily: "'Bahnschrift', 'Montserrat', Arial, sans-serif",
      }}
    >
      {/* 1. Top Debate Banner */}
      <div
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: 10,
          padding: '8px 24px',
          borderRadius: 30,
          backgroundColor: 'rgba(2, 9, 20, 0.88)',
          border: `1.5px solid ${accentColor}`,
          boxShadow: `0 0 25px ${accentColor}35`,
          marginBottom: 16,
        }}
      >
        <div
          style={{
            width: 10,
            height: 10,
            borderRadius: '50%',
            backgroundColor: accentColor,
            boxShadow: `0 0 12px ${accentColor}`,
            transform: `scale(${pulse})`,
          }}
        />
        <span
          style={{
            fontSize: 16,
            letterSpacing: 3,
            color: accentColor,
            fontWeight: 900,
            textTransform: 'uppercase',
          }}
        >
          DEBATE COMUNITARIO • ENIGMAIQ
        </span>
      </div>

      <div
        style={{
          fontSize: 34,
          fontWeight: 900,
          color: '#ffffff',
          textAlign: 'center',
          maxWidth: 920,
          lineHeight: 1.2,
          marginBottom: 35,
          textShadow: '0 4px 24px rgba(0,0,0,0.9)',
        }}
      >
        {scene.headline || '¿CUÁL ES TU POSTURA FRENTE A ESTE ENIGMA?'}
      </div>

      {/* 2. Dual Poll Options Container */}
      <div
        style={{
          width: '100%',
          maxWidth: 880,
          display: 'flex',
          flexDirection: 'column',
          gap: 20,
          transform: `scale(${entrance})`,
        }}
      >
        {/* Option A Card */}
        <div
          style={{
            padding: '24px 28px',
            borderRadius: 20,
            backgroundColor: 'rgba(2, 9, 22, 0.90)',
            border: `2px solid ${primaryColor}80`,
            boxShadow: `0 0 35px ${primaryColor}25`,
            display: 'flex',
            flexDirection: 'column',
            gap: 12,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
              <div
                style={{
                  width: 44,
                  height: 44,
                  borderRadius: 12,
                  backgroundColor: primaryColor,
                  color: '#020914',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 22,
                  fontWeight: 900,
                  boxShadow: `0 0 16px ${primaryColor}`,
                }}
              >
                A
              </div>
              <div style={{ fontSize: 22, fontWeight: 900, color: '#ffffff' }}>
                {scene.pollOptionA || 'OPCIÓN A'}
              </div>
            </div>
            <div style={{ fontSize: 28, fontWeight: 900, color: primaryColor }}>
              {Math.round(voteA)}%
            </div>
          </div>

          {/* Voting Bar Progress */}
          <div style={{ width: '100%', height: 12, backgroundColor: 'rgba(255,255,255,0.08)', borderRadius: 6, overflow: 'hidden' }}>
            <div
              style={{
                height: '100%',
                width: `${voteA}%`,
                backgroundColor: primaryColor,
                boxShadow: `0 0 16px ${primaryColor}`,
              }}
            />
          </div>
        </div>

        {/* Option B Card */}
        <div
          style={{
            padding: '24px 28px',
            borderRadius: 20,
            backgroundColor: 'rgba(2, 9, 22, 0.90)',
            border: `2px solid ${accentColor}80`,
            boxShadow: `0 0 35px ${accentColor}25`,
            display: 'flex',
            flexDirection: 'column',
            gap: 12,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
              <div
                style={{
                  width: 44,
                  height: 44,
                  borderRadius: 12,
                  backgroundColor: accentColor,
                  color: '#020914',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 22,
                  fontWeight: 900,
                  boxShadow: `0 0 16px ${accentColor}`,
                }}
              >
                B
              </div>
              <div style={{ fontSize: 22, fontWeight: 900, color: '#ffffff' }}>
                {scene.pollOptionB || 'OPCIÓN B'}
              </div>
            </div>
            <div style={{ fontSize: 28, fontWeight: 900, color: accentColor }}>
              {Math.round(voteB)}%
            </div>
          </div>

          {/* Voting Bar Progress */}
          <div style={{ width: '100%', height: 12, backgroundColor: 'rgba(255,255,255,0.08)', borderRadius: 6, overflow: 'hidden' }}>
            <div
              style={{
                height: '100%',
                width: `${voteB}%`,
                backgroundColor: accentColor,
                boxShadow: `0 0 16px ${accentColor}`,
              }}
            />
          </div>
        </div>
      </div>

      {/* 3. Bottom Call To Action Arrow */}
      <div
        style={{
          marginTop: 35,
          padding: '12px 28px',
          borderRadius: 24,
          backgroundColor: 'rgba(255, 255, 255, 0.08)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          display: 'flex',
          alignItems: 'center',
          gap: 12,
        }}
      >
        <span style={{ fontSize: 20 }}>👇</span>
        <span
          style={{
            color: '#ffffff',
            fontSize: 18,
            fontWeight: 800,
            letterSpacing: 1.5,
            textTransform: 'uppercase',
          }}
        >
          DEJA TU VOTO [A] O [B] EN LOS COMENTARIOS
        </span>
      </div>
    </div>
  );
};