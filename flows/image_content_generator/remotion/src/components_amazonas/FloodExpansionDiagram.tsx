import React from 'react';
import { interpolate } from 'remotion';

interface FloodExpansionProps {
  frame: number;
  progress: number; // 0 (dry season) to 1 (monsoon flood)
}

export const FloodExpansionDiagram: React.FC<FloodExpansionProps> = ({
  frame,
  progress,
}) => {
  // Water rise: +0m to +15m
  const waterRiseMeters = interpolate(progress, [0, 1], [0, 15]);
  // River width: 5km to 48km
  const riverWidthKm = interpolate(progress, [0, 1], [5, 48]);

  // Visual dimensions
  const waterLevelY = interpolate(progress, [0, 1], [1050, 820]);
  const waterWidth = interpolate(progress, [0, 1], [240, 960]);

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: 1080,
        height: 1920,
        backgroundColor: '#020b17',
        overflow: 'hidden',
      }}
    >
      {/* 1. Rainforest & Storm Atmosphere Background */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: 1080,
          height: 1920,
          background:
            'radial-gradient(circle at 50% 30%, #062038 0%, #031020 60%, #01070e 100%)',
        }}
      />

      {/* Rain animation particles in rainy season */}
      <svg
        width="1080"
        height="1920"
        style={{ position: 'absolute', top: 0, left: 0, pointerEvents: 'none' }}
      >
        {progress > 0.3 && (
          <g opacity={Math.min(1, (progress - 0.3) * 2)}>
            {[...Array(40)].map((_, idx) => {
              const rx = (idx * 27 + frame * 4) % 1080;
              const ry = (idx * 53 + frame * 32) % 1920;
              return (
                <line
                  key={idx}
                  x1={rx}
                  y1={ry}
                  x2={rx - 6}
                  y2={ry + 28}
                  stroke="#38bdf8"
                  strokeWidth="1.5"
                  opacity="0.4"
                />
              );
            })}
          </g>
        )}
      </svg>

      {/* 2. Cross-Section Diagram Container */}
      <div
        style={{
          position: 'absolute',
          top: 360,
          left: 40,
          width: 1000,
          height: 900,
        }}
      >
        <svg viewBox="0 0 1000 900" width="1000" height="900" style={{ overflow: 'visible' }}>
          <defs>
            {/* Water gradient */}
            <linearGradient id="amazonWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.85" />
              <stop offset="30%" stopColor="#0284c7" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#082f49" stopOpacity="0.98" />
            </linearGradient>

            {/* Muddy Riverbed gradient */}
            <linearGradient id="mudBedGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#78350f" />
              <stop offset="40%" stopColor="#451a03" />
              <stop offset="100%" stopColor="#1c1917" />
            </linearGradient>
          </defs>

          {/* Deep Underground Sediment Bed */}
          <path
            d="M 0 550 Q 200 530 380 580 Q 500 680 620 580 Q 800 530 1000 550 L 1000 900 L 0 900 Z"
            fill="url(#mudBedGrad)"
          />

          {/* Flooded Rainforest Trees on the Banks */}
          {[
            { x: 80, y: 530, h: 90 },
            { x: 160, y: 535, h: 105 },
            { x: 240, y: 545, h: 80 },
            { x: 760, y: 545, h: 85 },
            { x: 840, y: 535, h: 100 },
            { x: 920, y: 530, h: 95 },
          ].map((tree, idx) => {
            const submerged = waterLevelY < 550;
            return (
              <g key={idx} transform={`translate(${tree.x}, ${tree.y})`}>
                {/* Trunk */}
                <rect x="-4" y={-tree.h} width="8" height={tree.h} fill="#713f12" />
                {/* Foliage */}
                <circle cx="0" cy={-tree.h - 15} r="26" fill="#15803d" opacity="0.9" />
                <circle cx="-12" cy={-tree.h - 8} r="20" fill="#166534" opacity="0.85" />
                <circle cx="12" cy={-tree.h - 8} r="20" fill="#14532d" opacity="0.85" />
              </g>
            );
          })}

          {/* EXPANDING WATER MASS */}
          {/* Main water polygon */}
          <path
            d={`M ${500 - waterWidth / 2} ${waterLevelY - 300} 
               Q 500 ${waterLevelY - 305 + Math.sin(frame * 0.08) * 4} ${500 + waterWidth / 2} ${waterLevelY - 300} 
               L ${500 + waterWidth / 2} 650 
               Q 500 700 ${500 - waterWidth / 2} 650 Z`}
            fill="url(#amazonWaterGrad)"
          />

          {/* Surface Water Caustics / Waves */}
          <line
            x1={500 - waterWidth / 2}
            y1={waterLevelY - 300}
            x2={500 + waterWidth / 2}
            y2={waterLevelY - 300}
            stroke="#bae6fd"
            strokeWidth="3.5"
            strokeLinecap="round"
          />

          {/* 15m Rise Indicator (Vertical Ruler) */}
          <g transform={`translate(${500 + waterWidth / 2 + 15}, ${waterLevelY - 300})`}>
            <line x1="0" y1="0" x2="35" y2="0" stroke="#f59e0b" strokeWidth="2.5" />
            <line x1="20" y1="0" x2="20" y2="120" stroke="#f59e0b" strokeWidth="2" strokeDasharray="4 4" />
            <text
              x="45"
              y="6"
              fill="#fbbf24"
              fontSize="20"
              fontFamily="Consolas, monospace"
              fontWeight="900"
            >
              +{waterRiseMeters.toFixed(0)}m NIVEL
            </text>
          </g>

          {/* Horizontal River Width Indicator */}
          <g transform={`translate(500, ${waterLevelY - 340})`}>
            <line
              x1={-waterWidth / 2}
              y1="0"
              x2={waterWidth / 2}
              y2="0"
              stroke="#38bdf8"
              strokeWidth="2.5"
            />
            {/* Arrows on edges */}
            <polygon
              points={`${-waterWidth / 2},0 ${-waterWidth / 2 + 12},-6 ${-waterWidth / 2 + 12},6`}
              fill="#38bdf8"
            />
            <polygon
              points={`${waterWidth / 2},0 ${waterWidth / 2 - 12},-6 ${waterWidth / 2 - 12},6`}
              fill="#38bdf8"
            />
            {/* Width Badge */}
            <rect
              x="-110"
              y="-28"
              width="220"
              height="34"
              rx="8"
              fill="rgba(3, 15, 30, 0.9)"
              stroke="#38bdf8"
              strokeWidth="1.5"
            />
            <text
              x="0"
              y="-6"
              textAnchor="middle"
              fill="#ffffff"
              fontSize="18"
              fontFamily="Consolas, monospace"
              fontWeight="800"
            >
              ANCHO: ~{riverWidthKm.toFixed(0)} KM
            </text>
          </g>
        </svg>
      </div>

      {/* Floating Badge / Comparison Overlay */}
      <div
        style={{
          position: 'absolute',
          top: 250,
          left: 100,
          right: 100,
          display: 'flex',
          justifyContent: 'center',
          zIndex: 50,
          pointerEvents: 'none',
        }}
      >
        <div
          style={{
            backgroundColor: 'rgba(5, 15, 30, 0.92)',
            border: '1.5px solid rgba(56, 189, 248, 0.4)',
            borderRadius: 14,
            padding: '10px 24px',
            boxShadow: '0 8px 30px rgba(0, 0, 0, 0.9)',
            display: 'flex',
            alignItems: 'center',
            gap: 16,
          }}
        >
          <div
            style={{
              fontFamily: 'Consolas, monospace',
              fontSize: 22,
              fontWeight: 800,
              color: progress < 0.5 ? '#38bdf8' : '#64748b',
            }}
          >
            SEQUÍA: 5 KM
          </div>
          <div style={{ color: '#94a3b8', fontSize: 20 }}>➔</div>
          <div
            style={{
              fontFamily: 'Consolas, monospace',
              fontSize: 24,
              fontWeight: 900,
              color: progress >= 0.5 ? '#f59e0b' : '#64748b',
            }}
          >
            LLUVIAS: HASTA 50 KM
          </div>
        </div>
      </div>
    </div>
  );
};
