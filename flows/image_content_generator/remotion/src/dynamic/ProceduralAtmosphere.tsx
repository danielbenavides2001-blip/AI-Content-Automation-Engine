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

  // Gentle floating particle field
  const particles = React.useMemo(() => {
    return Array.from({ length: 28 }).map((_, i) => ({
      x: ((i * 137.5) % width),
      baseY: ((i * 223.7) % height),
      size: 2 + (i % 3) * 1.5,
      speed: 0.4 + (i % 4) * 0.25,
      alpha: 0.15 + (i % 5) * 0.12,
    }));
  }, [width, height]);

  // Subtle grid pulse
  const gridAlpha = 0.08 + Math.sin(frame * 0.04) * 0.02;

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
      {/* Background Radial Glow */}
      <div
        style={{
          position: 'absolute',
          top: '25%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 900,
          height: 900,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${primaryColor}14 0%, transparent 70%)`,
        }}
      />
      
      {/* Secondary Bottom Glow */}
      <div
        style={{
          position: 'absolute',
          bottom: '15%',
          left: '50%',
          transform: 'translate(-50%, 50%)',
          width: 800,
          height: 600,
          borderRadius: '50%',
          background: `radial-gradient(ellipse, ${secondaryColor}10 0%, transparent 65%)`,
        }}
      />

      {/* Cybernetic Tech Grid */}
      <svg
        width={width}
        height={height}
        style={{ position: 'absolute', inset: 0, opacity: gridAlpha }}
      >
        <defs>
          <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
            <path
              d="M 60 0 L 0 0 0 60"
              fill="none"
              stroke={primaryColor}
              strokeWidth="0.8"
            />
            <circle cx="0" cy="0" r="1.5" fill={primaryColor} />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>

      {/* Floating Ambient Particles */}
      <svg width={width} height={height} style={{ position: 'absolute', inset: 0 }}>
        {particles.map((p, i) => {
          const currentY = (p.baseY - frame * p.speed + height) % height;
          return (
            <circle
              key={i}
              cx={p.x}
              cy={currentY}
              r={p.size}
              fill={primaryColor}
              opacity={p.alpha}
            />
          );
        })}
      </svg>

      {/* Deep Vignette */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          boxShadow: 'inset 0 0 160px rgba(0, 0, 0, 0.85)',
        }}
      />
    </div>
  );
};
