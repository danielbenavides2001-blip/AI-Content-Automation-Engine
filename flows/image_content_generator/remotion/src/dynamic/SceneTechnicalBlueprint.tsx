import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { DynamicScene } from './types';

export const SceneTechnicalBlueprint: React.FC<{
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

  const rotSun = (frame * 1.8) % 360;
  const rotPlanet = (-frame * 2.4) % 360;
  const pistonTravel = Math.sin(frame * 0.1) * 35;
  const fluidFlow = (frame * 4) % 180;
  const pulse = Math.sin(frame * 0.12) * 0.2 + 0.8;

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
      {/* 1. Top Scene Headline */}
      <div
        style={{
          textAlign: 'center',
          marginBottom: 20,
          opacity: Math.min(1, frame / 12),
          transform: `translateY(${interpolate(frame, [0, 12], [-16, 0], { extrapolateRight: 'clamp' })}px)`,
        }}
      >
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 10,
            padding: '6px 18px',
            borderRadius: 20,
            backgroundColor: 'rgba(2, 9, 20, 0.85)',
            border: `1.5px solid ${primaryColor}80`,
            boxShadow: `0 0 20px ${primaryColor}30`,
            marginBottom: 8,
          }}
        >
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              backgroundColor: primaryColor,
              boxShadow: `0 0 10px ${primaryColor}`,
            }}
          />
          <span
            style={{
              fontSize: 18,
              letterSpacing: 3,
              color: '#ffffff',
              fontWeight: 800,
              textTransform: 'uppercase',
            }}
          >
            {scene.headline || 'ESQUEMA TÉCNICO & MECÁNICA INTERNA'}
          </span>
        </div>

        <div
          style={{
            fontSize: 34,
            fontWeight: 900,
            color: '#ffffff',
            lineHeight: 1.15,
            maxWidth: 960,
            textShadow: '0 4px 24px rgba(0,0,0,0.9)',
          }}
        >
          {scene.subheadline || 'DISEÑO CINEMÁTICO & TOLERANCIAS DE PRECISIÓN'}
        </div>
      </div>

      {/* 2. Main High-Precision Blueprint Schematic Canvas */}
      <div
        style={{
          position: 'relative',
          width: '100%',
          maxWidth: 960,
          height: 620,
          backgroundColor: '#020b18',
          borderRadius: 24,
          border: `2px solid ${primaryColor}80`,
          overflow: 'hidden',
          boxShadow: `0 0 45px ${primaryColor}25`,
        }}
      >
        <svg width="100%" height="100%" viewBox="0 0 960 620" style={{ overflow: 'visible' }}>
          <defs>
            {/* Blueprint Fine Grid Pattern */}
            <pattern id="bpGrid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke={`${primaryColor}20`} strokeWidth="0.8" />
              <circle cx="0" cy="0" r="1.2" fill={`${primaryColor}40`} />
            </pattern>

            {/* Glowing Metal & Neon Filters */}
            <filter id="bpGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* Blueprint Millimeter Background Grid */}
          <rect width="100%" height="100%" fill="url(#bpGrid)" />

          {/* Center Blueprint Crosshair Lines */}
          <line x1="480" y1="20" x2="480" y2="600" stroke={primaryColor} strokeWidth="1" strokeDasharray="6 4" opacity="0.4" />
          <line x1="20" y1="310" x2="940" y2="310" stroke={primaryColor} strokeWidth="1" strokeDasharray="6 4" opacity="0.4" />

          {/* Outer Dimension Ring */}
          <circle cx="360" cy="310" r="230" fill="none" stroke={secondaryColor} strokeWidth="1.2" strokeDasharray="8 6" opacity="0.5" />
          <circle cx="360" cy="310" r="190" fill="none" stroke={primaryColor} strokeWidth="2" opacity="0.7" />

          {/* ---------------------------------------------------- */}
          {/* PLANETARY TRANSMISSION ASSEMBLY (LEFT / CENTER) */}
          {/* ---------------------------------------------------- */}
          <g transform="translate(360, 310)">
            {/* Outer Ring Gear Teeth */}
            <g stroke={secondaryColor} strokeWidth="1.5" opacity="0.8">
              {Array.from({ length: 24 }).map((_, i) => (
                <line
                  key={i}
                  x1="0"
                  y1="180"
                  x2="0"
                  y2="195"
                  transform={`rotate(${i * 15})`}
                />
              ))}
            </g>

            {/* Rotating Sun Gear (Center) */}
            <g transform={`rotate(${rotSun})`}>
              <circle cx="0" cy="0" r="65" fill="#031526" stroke={primaryColor} strokeWidth="3" filter="url(#bpGlow)" />
              <circle cx="0" cy="0" r="45" fill="none" stroke={secondaryColor} strokeWidth="1.5" strokeDasharray="6 4" />
              {Array.from({ length: 8 }).map((_, i) => (
                <rect
                  key={i}
                  x="-10"
                  y="-75"
                  width="20"
                  height="16"
                  fill={primaryColor}
                  rx="3"
                  transform={`rotate(${i * 45})`}
                />
              ))}
              <circle cx="0" cy="0" r="20" fill="#020914" stroke={primaryColor} strokeWidth="2" />
            </g>

            {/* Orbiting Planet Gears (3 satellite gears) */}
            {[0, 120, 240].map((angle, idx) => {
              const rad = (angle * Math.PI) / 180;
              const px = Math.cos(rad) * 125;
              const py = Math.sin(rad) * 125;
              return (
                <g key={idx} transform={`translate(${px}, ${py}) rotate(${rotPlanet})`}>
                  <circle cx="0" cy="0" r="45" fill="#041a2e" stroke={accentColor} strokeWidth="2.5" />
                  <circle cx="0" cy="0" r="28" fill="none" stroke="#ffffff" strokeWidth="1" strokeDasharray="4 4" opacity="0.6" />
                  {Array.from({ length: 6 }).map((_, i) => (
                    <rect
                      key={i}
                      x="-8"
                      y="-52"
                      width="16"
                      height="12"
                      fill={accentColor}
                      rx="2"
                      transform={`rotate(${i * 60})`}
                    />
                  ))}
                  <circle cx="0" cy="0" r="12" fill="#020914" stroke={accentColor} strokeWidth="1.8" />
                </g>
              );
            })}
          </g>

          {/* ---------------------------------------------------- */}
          {/* HYDRAULIC PRESSURE PISTON ACTUATOR (RIGHT) */}
          {/* ---------------------------------------------------- */}
          <g transform="translate(680, 310)">
            {/* Actuator Cylinder Body */}
            <rect x="0" y="-80" width="220" height="160" rx="10" fill="#03162b" stroke={primaryColor} strokeWidth="2.5" />
            <rect x="15" y="-65" width="190" height="130" fill="#020d1c" stroke={secondaryColor} strokeWidth="1.2" strokeDasharray="4 4" />

            {/* Moving Piston Head */}
            <g transform={`translate(${pistonTravel}, 0)`}>
              {/* Piston Rod */}
              <line x1="-120" y1="0" x2="30" y2="0" stroke="#ffffff" strokeWidth="18" strokeLinecap="round" />
              {/* Piston Head Seals */}
              <rect x="20" y="-60" width="35" height="120" rx="4" fill={accentColor} stroke="#ffffff" strokeWidth="2" filter="url(#bpGlow)" />
              {/* High-Pressure Fluid Chamber (Left of Piston) */}
              <rect x="55" y="-60" width="130" height="120" fill={`${primaryColor}30`} />
            </g>

            {/* Fluid Intake Conduits with Animated Flow */}
            <path d="M 110 -80 L 110 -150 L 180 -150" fill="none" stroke="#00f5ff" strokeWidth="3.5" />
            <circle cx={110} cy={-150 + (fluidFlow % 70)} r="4" fill="#ffffff" filter="url(#bpGlow)" />
            <text x="120" y="-130" fill="#00f5ff" fontSize="12" fontWeight="900">
              FLUJO HIDRÁULICO ► 350 BAR
            </text>

            <path d="M 110 80 L 110 150 L 180 150" fill="none" stroke="#38bdf8" strokeWidth="3.5" />
            <text x="120" y="140" fill="#38bdf8" fontSize="12" fontWeight="900">
              RETORNO TÉRMICO ◄
            </text>
          </g>

          {/* ---------------------------------------------------- */}
          {/* TECHNICAL MEASUREMENT ANNOTATION CALLOUTS */}
          {/* ---------------------------------------------------- */}
          {/* Gear diameter callout */}
          <line x1="130" y1="310" x2="130" y2="550" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="4 4" />
          <line x1="590" y1="310" x2="590" y2="550" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="4 4" />
          <line x1="130" y1="540" x2="590" y2="540" stroke="#f59e0b" strokeWidth="2" />
          <polygon points="130,540 144,535 144,545" fill="#f59e0b" />
          <polygon points="590,540 576,535 576,545" fill="#f59e0b" />
          <text x="360" y="532" textAnchor="middle" fill="#fbbf24" fontSize="15" fontWeight="900" letterSpacing="1">
            DIÁMETRO NOMINAL Ø 460 mm [ TOLERANCIA ±0.012 ]
          </text>
        </svg>

        {/* Technical HUD Telemetry Badge */}
        <div
          style={{
            position: 'absolute',
            top: 20,
            left: 20,
            padding: '12px 18px',
            backgroundColor: 'rgba(2, 9, 22, 0.92)',
            border: `1.5px solid ${primaryColor}80`,
            borderRadius: 14,
            backdropFilter: 'blur(12px)',
            boxShadow: `0 0 25px ${primaryColor}25`,
            display: 'flex',
            flexDirection: 'column',
            gap: 4,
          }}
        >
          <div style={{ color: primaryColor, fontSize: 13, fontWeight: 900, letterSpacing: 1.5 }}>
            ESPECIFICACIÓN // SISTEMA EN ACCIÓN
          </div>
          <div style={{ color: '#ffffff', fontSize: 18, fontWeight: 900 }}>
            {scene.metricLabel || 'EFICIENCIA CINEMÁTICA'}:{' '}
            <span style={{ color: accentColor }}>{scene.metricValA || '99.4%'}</span>
          </div>
        </div>
      </div>
    </div>
  );
};