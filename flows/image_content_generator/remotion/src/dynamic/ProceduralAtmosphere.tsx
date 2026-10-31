import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';

export const ProceduralAtmosphere: React.FC<{
  primaryColor?: string;
  secondaryColor?: string;
  backgroundColor?: string;
}> = ({
  primaryColor = '#00f5ff',
  secondaryColor = '#38bdf8',
  backgroundColor = '#030814'
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  // Floating bioluminescent dust specks
  const particles = React.useMemo(() => {
    return Array.from({ length: 36 }).map((_, i) => ({
      x: ((i * 137.5) % width),
      baseY: ((i * 223.7) % height),
      size: 2 + (i % 3) * 1.6,
      speed: 0.35 + (i % 4) * 0.22,
      alpha: 0.2 + (i % 5) * 0.15,
      blur: (i % 3) === 0 ? 3 : 0,
    }));
  }, [width, height]);

  // Subtle ambient wave drift
  const waveShift = Math.sin(frame * 0.03) * 12;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundColor,
        overflow: 'hidden',
        pointerEvents: 'none',
      }}
    >
      {/* 1. Deep Oceanic / Atmospheric Radial Gradient (Top Center) */}
      <div
        style={{
          position: 'absolute',
          top: '20%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 1200,
          height: 1200,
          borderRadius: '50%',
          background: `radial-gradient(circle at 50% 50%, #08213b 0%, #031020 50%, transparent 80%)`,
          opacity: 0.85,
        }}
      />

      {/* 2. Secondary Primary Color Bloom (Center) */}
      <div
        style={{
          position: 'absolute',
          top: '45%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 900,
          height: 900,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${primaryColor}20 0%, ${secondaryColor}0a 45%, transparent 70%)`,
        }}
      />

      {/* 3. Bottom Horizon Ambient Light */}
      <div
        style={{
          position: 'absolute',
          bottom: '10%',
          left: '50%',
          transform: 'translate(-50%, 50%)',
          width: 1100,
          height: 700,
          borderRadius: '50%',
          background: `radial-gradient(ellipse, ${secondaryColor}15 0%, transparent 65%)`,
        }}
      />

      {/* 4. Elegant Topographic Organic Background Contours */}
      <svg
        width={width}
        height={height}
        style={{
          position: 'absolute',
          inset: 0,
          opacity: 0.14,
        }}
      >
        <path
          d={`M -50 450 Q 300 ${410 + waveShift} 650 470 T 1150 430`}
          fill="none"
          stroke={primaryColor}
          strokeWidth="1.5"
          strokeDasharray="6 6"
        />
        <path
          d={`M -50 780 Q 400 ${750 - waveShift} 750 810 T 1150 770`}
          fill="none"
          stroke={secondaryColor}
          strokeWidth="1.2"
        />
        <path
          d={`M -50 1150 Q 320 ${1180 + waveShift} 700 1130 T 1150 1160`}
          fill="none"
          stroke={primaryColor}
          strokeWidth="1.5"
          strokeDasharray="8 6"
        />
        <path
          d={`M -50 1480 Q 450 ${1450 - waveShift} 800 1510 T 1150 1470`}
          fill="none"
          stroke={secondaryColor}
          strokeWidth="1.2"
        />
      </svg>

      {/* 5. Floating Bioluminescent Ambient Specks */}
      <svg width={width} height={height} style={{ position: 'absolute', inset: 0 }}>
        <defs>
          <filter id="speckGlow">
            <feGaussianBlur stdDeviation="2.5" />
          </filter>
        </defs>
        {particles.map((p, i) => {
          const currentY = (p.baseY - frame * p.speed + height) % height;
          return (
            <circle
              key={i}
              cx={p.x}
              cy={currentY}
              r={p.size}
              fill={i % 2 === 0 ? primaryColor : secondaryColor}
              opacity={p.alpha}
              filter={p.blur > 0 ? 'url(#speckGlow)' : undefined}
            />
          );
        })}
      </svg>

      {/* 6. Cinematic Corner Vignette */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          boxShadow: 'inset 0 0 180px rgba(0, 3, 10, 0.92)',
        }}
      />
    </div>
  );
};