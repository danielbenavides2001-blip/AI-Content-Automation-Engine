import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import { DynamicScene } from './types';

export const SceneTelemetryGauge: React.FC<{
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

  const progress = interpolate(frame, [0, 50], [0, 82], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const angle = (progress / 100) * 260 - 130;
  const oscWave = (frame * 6) % 360;

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
            border: `1.5px solid ${accentColor}80`,
            boxShadow: `0 0 20px ${accentColor}30`,
            marginBottom: 8,
          }}
        >
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              backgroundColor: accentColor,
              boxShadow: `0 0 10px ${accentColor}`,
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
            {scene.headline || 'DATOS CRÍTICOS & TELEMETRÍA CUANTITATIVA'}
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
          {scene.subheadline || 'REGISTRO DE MAGNITUDES FÍSICAS EXTREMAS'}
        </div>
      </div>

      {/* 2. Main Dial Presentation Container */}
      <div
        style={{
          position: 'relative',
          width: '100%',
          maxWidth: 720,
          height: 600,
          backgroundColor: '#020b18',
          borderRadius: 24,
          border: `2px solid ${primaryColor}80`,
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: `0 0 45px ${primaryColor}25`,
        }}
      >
        <svg width="600" height="420" viewBox="0 0 600 420" style={{ overflow: 'visible' }}>
          <defs>
            <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="60%" stopColor={primaryColor} />
              <stop offset="85%" stopColor={accentColor} />
              <stop offset="100%" stopColor="#ef4444" />
            </linearGradient>

            <filter id="gaugeGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* Background Track Arc */}
          <circle
            cx="300"
            cy="270"
            r="190"
            fill="none"
            stroke="rgba(255,255,255,0.08)"
            strokeWidth="24"
            strokeDasharray="995"
            strokeDashoffset="278"
            strokeLinecap="round"
            transform="rotate(140 300 270)"
          />

          {/* Active Multicolor Gauge Arc */}
          <circle
            cx="300"
            cy="270"
            r="190"
            fill="none"
            stroke="url(#gaugeGradient)"
            strokeWidth="24"
            strokeDasharray="995"
            strokeDashoffset={995 - (progress / 100) * 717}
            strokeLinecap="round"
            transform="rotate(140 300 270)"
            filter="url(#gaugeGlow)"
          />

          {/* Tick marks around gauge */}
          {Array.from({ length: 19 }).map((_, i) => {
            const tickAngle = -130 + i * (260 / 18);
            return (
              <g key={i} transform={`rotate(${tickAngle} 300 270)`}>
                <line
                  x1="300"
                  y1="56"
                  x2="300"
                  y2={i % 3 === 0 ? "42" : "48"}
                  stroke={i > 15 ? "#ef4444" : "#ffffff"}
                  strokeWidth={i % 3 === 0 ? "2.5" : "1.2"}
                  opacity={i % 3 === 0 ? "0.9" : "0.4"}
                />
              </g>
            );
          })}

          {/* Needle Indicator */}
          <g transform={`rotate(${angle} 300 270)`}>
            <line x1="300" y1="270" x2="300" y2="95" stroke={accentColor} strokeWidth="5" strokeLinecap="round" filter="url(#gaugeGlow)" />
            <circle cx="300" cy="270" r="18" fill="#020914" stroke={accentColor} strokeWidth="4" />
            <circle cx="300" cy="270" r="6" fill="#ffffff" />
          </g>

          {/* Realtime Oscilloscope Waveform at Bottom of Gauge */}
          <g transform="translate(150, 360)">
            <rect x="0" y="0" width="300" height="40" rx="8" fill="rgba(2,9,20,0.8)" stroke={`${primaryColor}40`} strokeWidth="1" />
            <path
              d={`M 10 20 Q 50 ${20 + Math.sin(oscWave * 0.05) * 12} 80 20 T 150 ${20 - Math.sin(oscWave * 0.05) * 12} T 220 20 T 290 20`}
              fill="none"
              stroke={primaryColor}
              strokeWidth="2"
              opacity="0.85"
            />
          </g>
        </svg>

        {/* Big Digital Readout in Center */}
        <div style={{ textAlign: 'center', marginTop: -40, zIndex: 10 }}>
          <div style={{ fontSize: 44, fontWeight: 900, color: '#ffffff', textShadow: `0 0 25px ${primaryColor}` }}>
            {scene.metricValA || `${Math.round(progress)}%`}
          </div>
          <div style={{ fontSize: 16, fontWeight: 900, color: accentColor, letterSpacing: 2, textTransform: 'uppercase', marginTop: 2 }}>
            {scene.metricLabel || 'VALOR CUANTIFICADO'}
          </div>
        </div>
      </div>
    </div>
  );
};