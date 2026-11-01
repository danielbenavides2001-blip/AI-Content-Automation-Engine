import React from 'react';
import { interpolate, OffthreadVideo, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { DynamicScene } from './types';

export const SceneStockFootage: React.FC<{
  scene: DynamicScene;
  primaryColor?: string;
  secondaryColor?: string;
  accentColor?: string;
}> = ({
  scene,
  primaryColor = '#00f5ff',
  secondaryColor = '#38bdf8',
  accentColor = '#f59e0b',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Subtle slow Ken Burns zoom
  const scale = interpolate(frame, [0, scene.durationFrames], [1.0, 1.06], {
    extrapolateRight: 'clamp',
  });

  // Smooth entrance for cards
  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 80, mass: 0.9 },
  });

  const cardTranslateY = interpolate(entrance, [0, 1], [-40, 0]);
  const cardOpacity = interpolate(entrance, [0, 1], [0, 1]);

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        overflow: 'hidden',
        fontFamily: "'Bahnschrift', 'Montserrat', Arial, sans-serif",
      }}
    >
      {/* 1. High Resolution Stock Video Background */}
      {scene.stockVideoPath && (
        <OffthreadVideo
          src={staticFile(scene.stockVideoPath)}
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transform: `scale(${scale})`,
          }}
        />
      )}

      {/* 2. Cinematic Contrast Overlay */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background:
            'linear-gradient(to bottom, rgba(2,9,20,0.7) 0%, rgba(2,9,20,0.2) 40%, rgba(2,9,20,0.4) 65%, rgba(2,9,20,0.88) 100%)',
        }}
      />

      {/* 3. Upper Hook / Explanatory Card (Navy + Gold Border) */}
      <div
        style={{
          position: 'absolute',
          top: 210,
          left: 55,
          right: 55,
          padding: '28px 24px',
          backgroundColor: 'rgba(11, 23, 42, 0.92)',
          border: `3px solid ${accentColor}`,
          borderRadius: 22,
          boxShadow: `0 0 35px ${accentColor}40`,
          textAlign: 'center',
          transform: `translateY(${cardTranslateY}px)`,
          opacity: cardOpacity,
          zIndex: 40,
        }}
      >
        <div
          style={{
            fontSize: 32,
            fontWeight: 900,
            color: '#ffffff',
            letterSpacing: 1.5,
            marginBottom: 8,
            textTransform: 'uppercase',
          }}
        >
          {scene.headline}
        </div>
        <div
          style={{
            fontSize: 22,
            fontWeight: 800,
            color: accentColor,
            letterSpacing: 1.5,
            textTransform: 'uppercase',
          }}
        >
          {scene.subheadline}
        </div>
      </div>

      {/* 4. Middle Metric Callout Badge (if metricValA is provided) */}
      {scene.metricValA && (
        <div
          style={{
            position: 'absolute',
            top: 720,
            left: 70,
            right: 70,
            padding: '26px 20px',
            backgroundColor: 'rgba(11, 23, 42, 0.90)',
            border: `2px solid ${primaryColor}`,
            borderRadius: 20,
            boxShadow: `0 0 35px ${primaryColor}35`,
            textAlign: 'center',
            transform: `scale(${entrance})`,
            opacity: cardOpacity,
            zIndex: 40,
          }}
        >
          <div
            style={{
              fontSize: 60,
              fontWeight: 900,
              color: accentColor,
              letterSpacing: 2,
              lineHeight: 1.1,
            }}
          >
            {scene.metricValA}
          </div>
          <div
            style={{
              fontSize: 22,
              fontWeight: 800,
              color: '#e2e8f0',
              letterSpacing: 2,
              marginTop: 10,
              textTransform: 'uppercase',
            }}
          >
            {scene.metricLabel || scene.subheadline}
          </div>
        </div>
      )}
    </div>
  );
};
