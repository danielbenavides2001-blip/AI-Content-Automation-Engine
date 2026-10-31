import React from 'react';

interface DeepSeaBackgroundProps {
  frame: number;
  showFloor?: boolean;
  floorOffset?: number; // 0 to 1 progress of floor visibility
}

export const DeepSeaBackground: React.FC<DeepSeaBackgroundProps> = ({
  frame,
  showFloor = false,
  floorOffset = 0,
}) => {
  // Deterministic marine snow particles
  const particles = React.useMemo(() => {
    const list = [];
    for (let i = 0; i < 45; i++) {
      const seedX = (i * 137.5) % 1080;
      const seedY = (i * 223.1) % 1920;
      const size = 2 + (i % 5) * 1.5;
      const speed = 0.4 + (i % 4) * 0.3;
      const opacity = 0.2 + (i % 5) * 0.15;
      const swayPeriod = 60 + (i % 40);
      list.push({ seedX, seedY, size, speed, opacity, swayPeriod, id: i });
    }
    return list;
  }, []);

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: 1080,
        height: 1920,
        backgroundColor: '#020611',
        overflow: 'hidden',
      }}
    >
      {/* 1. Deep Ocean Lighting Gradient */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: 1080,
          height: 1920,
          background:
            'radial-gradient(ellipse 900px 1200px at 50% 25%, #082142 0%, #031126 55%, #010612 100%)',
        }}
      />

      {/* 2. Soft Ambient Oceanic God-Rays (Subsurface Light Beams) */}
      <svg
        width="1080"
        height="1920"
        style={{ position: 'absolute', top: 0, left: 0, pointerEvents: 'none' }}
      >
        <defs>
          <linearGradient id="rayGrad1" x1="0%" y1="0%" x2="40%" y2="100%">
            <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.12" />
            <stop offset="60%" stopColor="#0284c7" stopOpacity="0.04" />
            <stop offset="100%" stopColor="#031126" stopOpacity="0" />
          </linearGradient>
          <linearGradient id="rayGrad2" x1="100%" y1="0%" x2="60%" y2="100%">
            <stop offset="0%" stopColor="#06b6d4" stopOpacity="0.09" />
            <stop offset="70%" stopColor="#0369a1" stopOpacity="0.02" />
            <stop offset="100%" stopColor="#031126" stopOpacity="0" />
          </linearGradient>
        </defs>

        {/* Ray 1 */}
        <polygon
          points={`180,0 360,0 ${460 + Math.sin(frame * 0.02) * 40},1920 ${200 + Math.sin(frame * 0.02) * 40},1920`}
          fill="url(#rayGrad1)"
        />

        {/* Ray 2 */}
        <polygon
          points={`680,0 840,0 ${960 + Math.cos(frame * 0.018) * 35},1920 ${720 + Math.cos(frame * 0.018) * 35},1920`}
          fill="url(#rayGrad2)"
        />

        {/* Ray 3 (Center subtle pulse) */}
        <polygon
          points={`480,0 600,0 ${650 + Math.sin(frame * 0.025 + 1) * 30},1920 ${510 + Math.sin(frame * 0.025 + 1) * 30},1920`}
          fill="url(#rayGrad1)"
          opacity="0.75"
        />

        {/* Floating Marine Snow / Bioluminescent Particles */}
        {particles.map((p) => {
          const currentY = (p.seedY - frame * p.speed + 1920 * 10) % 1920;
          const currentX = p.seedX + Math.sin(frame / p.swayPeriod) * 18;
          const pulseOpacity = p.opacity * (0.8 + 0.3 * Math.sin(frame * 0.05 + p.id));
          return (
            <circle
              key={p.id}
              cx={currentX}
              cy={currentY}
              r={p.size}
              fill="#7dd3fc"
              opacity={pulseOpacity}
              filter="drop-shadow(0 0 4px rgba(56, 189, 248, 0.4))"
            />
          );
        })}

        {/* Optional Seafloor Bed (Rocky Substrate & Sand) */}
        {showFloor && (
          <g opacity={Math.min(1, floorOffset)}>
            {/* Rocky base gradient */}
            <path
              d="M 0 1620 Q 240 1560 480 1600 T 840 1580 Q 980 1590 1080 1570 L 1080 1920 L 0 1920 Z"
              fill="#060c18"
            />
            <path
              d="M 0 1680 Q 300 1640 600 1670 T 1080 1650 L 1080 1920 L 0 1920 Z"
              fill="#03070f"
            />
            {/* Sediment rocks */}
            <ellipse cx="280" cy="1660" rx="90" ry="40" fill="#0c1626" />
            <ellipse cx="760" cy="1670" rx="110" ry="45" fill="#0a1422" />
            <ellipse cx="520" cy="1720" rx="140" ry="50" fill="#050a12" />
          </g>
        )}
      </svg>

      {/* Subtle Deep-Sea Vignette */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: 1080,
          height: 1920,
          boxShadow: 'inset 0 0 160px rgba(0, 0, 0, 0.85)',
          pointerEvents: 'none',
        }}
      />
    </div>
  );
};
