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
  const pulse = Math.sin(frame * 0.12) * 0.15 + 0.85;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '120px 45px 320px 45px',
        boxSizing: 'border-box',
        fontFamily: "'Bahnschrift', 'Montserrat', Arial, sans-serif",
      }}
    >
      {/* Top Banner */}
      <div
        style={{
          padding: '8px 24px',
          borderRadius: 30,
          backgroundColor: 'rgba(2, 9, 20, 0.85)',
          border: `1.5px solid ${accentColor}`,
          color: accentColor,
          fontSize: 16,
          fontWeight: 900,
          letterSpacing: 3,
          textTransform: 'uppercase',
          marginBottom: 20,
          boxShadow: `0 0 25px ${accentColor}30`,
        }}
      >
        DEBATE COMUNITARIO • ENIGMAIQ
      </div>

      <div
        style={{
          fontSize: 34,
          fontWeight: 900,
          color: '#ffffff',
          textAlign: 'center',
          maxWidth: 900,
          lineHeight: 1.2,
          marginBottom: 40,
        }}
      >
        {scene.headline || '¿CUÁL ES TU POSTURA FRENTE A ESTE ENIGMA?'}
      </div>

      {/* Poll Options Container */}
      <div
        style={{
          width: '100%',
          maxWidth: 820,
          display: 'flex',
          flexDirection: 'column',
          gap: 20,
          transform: `scale(${entrance})`,
        }}
      >
        {/* Option A */}
        <div
          style={{
            padding: '22px 28px',
            borderRadius: 18,
            backgroundColor: 'rgba(2, 9, 22, 0.85)',
            border: `2px solid ${primaryColor}`,
            display: 'flex',
            alignItems: 'center',
            gap: 20,
            boxShadow: `0 0 30px ${primaryColor}25`,
          }}
        >
          <div
            style={{
              width: 48,
              height: 48,
              borderRadius: 12,
              backgroundColor: primaryColor,
              color: '#020914',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 24,
              fontWeight: 900,
            }}
          >
            A
          </div>
          <div style={{ color: '#ffffff', fontSize: 22, fontWeight: 800 }}>
            {scene.pollOptionA || 'Opción A: Fenómeno de mayor impacto'}
          </div>
        </div>

        {/* Option B */}
        <div
          style={{
            padding: '22px 28px',
            borderRadius: 18,
            backgroundColor: 'rgba(2, 9, 22, 0.85)',
            border: `2px solid ${secondaryColor}`,
            display: 'flex',
            alignItems: 'center',
            gap: 20,
            boxShadow: `0 0 30px ${secondaryColor}25`,
          }}
        >
          <div
            style={{
              width: 48,
              height: 48,
              borderRadius: 12,
              backgroundColor: secondaryColor,
              color: '#020914',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 24,
              fontWeight: 900,
            }}
          >
            B
          </div>
          <div style={{ color: '#ffffff', fontSize: 22, fontWeight: 800 }}>
            {scene.pollOptionB || 'Opción B: Mayor misterio para la ciencia'}
          </div>
        </div>
      </div>

      {/* Bottom CTA */}
      <div
        style={{
          marginTop: 35,
          color: '#ffffff',
          fontSize: 20,
          fontWeight: 800,
          letterSpacing: 1.5,
          textAlign: 'center',
          opacity: pulse,
        }}
      >
        👇 COMENTA <span style={{ color: primaryColor }}>'A'</span> O <span style={{ color: secondaryColor }}>'B'</span> Y DIME DE DÓNDE ERES 👇
      </div>
    </div>
  );
};
