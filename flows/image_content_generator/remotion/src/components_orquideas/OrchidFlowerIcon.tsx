import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface OrchidFlowerProps {
  x: number;
  y: number;
  size?: number;
  delay?: number;
  colorScheme?: 'colombia' | 'ecuador';
}

export const OrchidFlowerIcon: React.FC<OrchidFlowerProps> = ({
  x,
  y,
  size = 36,
  delay = 0,
  colorScheme = 'colombia',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bloom = spring({
    frame: frame - delay,
    fps,
    config: { damping: 12, stiffness: 140 },
  });

  const scale = interpolate(bloom, [0, 1], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const petalColor = colorScheme === 'colombia' ? '#e879f9' : '#fb923c';
  const innerPetal = colorScheme === 'colombia' ? '#c026d3' : '#ea580c';
  const centerColor = '#facc15';

  if (scale <= 0.01) return null;

  return (
    <g
      transform={`translate(${x}, ${y}) scale(${scale})`}
      style={{ transformOrigin: `${x}px ${y}px` }}
    >
      {/* Outer 3 Sepals */}
      <ellipse cx={0} cy={-size * 0.35} rx={size * 0.22} ry={size * 0.38} fill={petalColor} opacity={0.95} />
      <ellipse cx={-size * 0.35} cy={size * 0.22} rx={size * 0.22} ry={size * 0.38} transform={`rotate(-40 ${-size * 0.35} ${size * 0.22})`} fill={petalColor} opacity={0.95} />
      <ellipse cx={size * 0.35} cy={size * 0.22} rx={size * 0.22} ry={size * 0.38} transform={`rotate(40 ${size * 0.35} ${size * 0.22})`} fill={petalColor} opacity={0.95} />

      {/* 2 Broad Lateral Petals */}
      <circle cx={-size * 0.32} cy={-size * 0.08} r={size * 0.28} fill={innerPetal} opacity={0.9} />
      <circle cx={size * 0.32} cy={-size * 0.08} r={size * 0.28} fill={innerPetal} opacity={0.9} />

      {/* Labellum (Lip) */}
      <ellipse cx={0} cy={size * 0.26} rx={size * 0.32} ry={size * 0.35} fill={innerPetal} />
      <ellipse cx={0} cy={size * 0.35} rx={size * 0.2} ry={size * 0.2} fill="#9333ea" />

      {/* Center column (Pollen) */}
      <circle cx={0} cy={0} r={size * 0.12} fill={centerColor} />
    </g>
  );
};
