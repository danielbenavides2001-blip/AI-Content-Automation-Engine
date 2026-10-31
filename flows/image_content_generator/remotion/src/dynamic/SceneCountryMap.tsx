import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { COUNTRY_SILHOUETTES, SilhouetteData } from '../country_silhouettes';
import { DynamicScene } from './types';

export const SceneCountryMap: React.FC<{
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

  // Country lookup with fallback
  const cKey = (scene.countryA || 'colombia').toLowerCase();
  const country: SilhouetteData = COUNTRY_SILHOUETTES[cKey] || COUNTRY_SILHOUETTES['colombia'];

  const themePrimary = country.primary || primaryColor;
  const themeAccent = country.accent || accentColor;

  // Smooth cinematic entrance spring
  const scale = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 75, mass: 0.9 },
  });

  // Laser contour outline stroke-dashoffset animation
  const strokeProgress = interpolate(frame, [0, 50], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Scanning laser beam sweeping down
  const scanY = (frame * 7) % 700;

  // Radar pulse animations
  const pulseA = Math.sin(frame * 0.12) * 0.3 + 0.7;
  const pulseRadius = 12 + (frame % 35) * 1.2;
  const pulseAlpha = Math.max(0, 1 - (frame % 35) / 35);

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
      {/* 1. Ambient Background Glows */}
      <div
        style={{
          position: 'absolute',
          top: '35%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 850,
          height: 850,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${themePrimary}22 0%, ${themeAccent}08 45%, transparent 70%)`,
          pointerEvents: 'none',
        }}
      />

      {/* 2. Top Scene Headline & Category Banner */}
      <div
        style={{
          textAlign: 'center',
          marginBottom: 24,
          opacity: Math.min(1, frame / 12),
          transform: `translateY(${interpolate(frame, [0, 12], [-18, 0], { extrapolateRight: 'clamp' })}px)`,
          zIndex: 10,
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
            border: `1.5px solid ${themeAccent}80`,
            boxShadow: `0 0 20px ${themeAccent}30`,
            marginBottom: 10,
          }}
        >
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              backgroundColor: themeAccent,
              boxShadow: `0 0 10px ${themeAccent}`,
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
            {scene.headline || 'ANOMALÍA CARTOGRÁFICA REGISTRADA'}
          </span>
        </div>

        <div
          style={{
            fontSize: 34,
            fontWeight: 900,
            color: '#ffffff',
            lineHeight: 1.15,
            maxWidth: 940,
            textShadow: '0 4px 24px rgba(0,0,0,0.9)',
          }}
        >
          {scene.subheadline || country.name.toUpperCase()}
        </div>
      </div>

      {/* 3. Main Map Presentation Canvas */}
      <div
        style={{
          position: 'relative',
          width: '100%',
          maxWidth: 720,
          height: 720,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transform: `scale(${scale})`,
        }}
      >
        {/* Holographic Radar Concentric Target Rings */}
        <svg
          width="720"
          height="720"
          style={{
            position: 'absolute',
            inset: 0,
            opacity: 0.35,
            transform: `rotate(${frame * 0.15}deg)`,
            pointerEvents: 'none',
          }}
        >
          <circle cx="360" cy="360" r="160" fill="none" stroke={secondaryColor} strokeWidth="1" strokeDasharray="6 6" />
          <circle cx="360" cy="360" r="260" fill="none" stroke={themePrimary} strokeWidth="1.5" />
          <circle cx="360" cy="360" r="340" fill="none" stroke={themeAccent} strokeWidth="1" strokeDasharray="10 8" />
          <line x1="20" y1="360" x2="700" y2="360" stroke={secondaryColor} strokeWidth="0.8" strokeDasharray="4 4" />
          <line x1="360" y1="20" x2="360" y2="700" stroke={secondaryColor} strokeWidth="0.8" strokeDasharray="4 4" />
        </svg>

        {/* High-Precision Country Vector Map */}
        <svg
          viewBox={country.viewBox}
          style={{
            width: '90%',
            height: '90%',
            filter: `drop-shadow(0 0 35px ${themePrimary}80) drop-shadow(0 0 70px ${themeAccent}30)`,
          }}
        >
          <defs>
            {/* Rich Biome Gradient */}
            <linearGradient id={`biome-${country.name}`} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={`${themePrimary}55`} />
              <stop offset="50%" stopColor={`${secondaryColor}30`} />
              <stop offset="100%" stopColor={`${themeAccent}25`} />
            </linearGradient>

            {/* Glowing Map Contour Filter */}
            <filter id="neonStrokeGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3.5" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>

            {/* Clip path inside country for interior elevation and scanlines */}
            <clipPath id={`mapClip-${country.name}`}>
              <path d={country.path} />
            </clipPath>
          </defs>

          {/* Underlay Biome Fill */}
          <path
            d={country.path}
            fill={`url(#biome-${country.name})`}
          />

          {/* Interior Topographic Elevation Bands & Scanlines */}
          <g clipPath={`url(#mapClip-${country.name})`}>
            {/* Horizontal Scan Laser Line */}
            <line
              x1="0"
              y1={scanY}
              x2="700"
              y2={scanY}
              stroke="#ffffff"
              strokeWidth="3.5"
              opacity="0.9"
              filter="url(#neonStrokeGlow)"
            />
            <rect
              x="0"
              y={Math.max(0, scanY - 60)}
              width="700"
              height="60"
              fill={`linear-gradient(to top, ${themePrimary}35, transparent)`}
              opacity="0.6"
            />

            {/* Concentric Topographic Inner Elevation Contours */}
            <path
              d={country.path}
              fill="none"
              stroke={themePrimary}
              strokeWidth="1.2"
              transform="scale(0.88) translate(45, 45)"
              strokeDasharray="5 5"
              opacity="0.5"
            />
            <path
              d={country.path}
              fill="none"
              stroke={themeAccent}
              strokeWidth="1.0"
              transform="scale(0.74) translate(110, 110)"
              strokeDasharray="4 6"
              opacity="0.4"
            />

            {/* Organic River / Geological Spine Flowing inside territory */}
            <path
              d="M 180 520 Q 320 420 370 310 T 520 180"
              fill="none"
              stroke="#38bdf8"
              strokeWidth="2.5"
              strokeDasharray="8 4"
              opacity="0.7"
            />
          </g>

          {/* Crisp Laser Outer Stroke */}
          <path
            d={country.path}
            fill="none"
            stroke={themePrimary}
            strokeWidth="3.5"
            strokeDasharray="2400"
            strokeDashoffset={2400 * strokeProgress}
            filter="url(#neonStrokeGlow)"
          />

          {/* Landmark Geo-Beacon Pin */}
          {country.landmark && (
            <g transform={`translate(${country.landmark.x}, ${country.landmark.y})`}>
              {/* Expanding radar ring */}
              <circle
                cx="0"
                cy="0"
                r={pulseRadius}
                fill="none"
                stroke={themeAccent}
                strokeWidth="2"
                opacity={pulseAlpha}
              />
              {/* Center point */}
              <circle
                cx="0"
                cy="0"
                r="6"
                fill={themeAccent}
                stroke="#ffffff"
                strokeWidth="1.8"
                filter="url(#neonStrokeGlow)"
              />
              {/* Vertical callout leader line */}
              <line
                x1="0"
                y1="0"
                x2="35"
                y2="-35"
                stroke={themeAccent}
                strokeWidth="2"
              />
              <line
                x1="35"
                y1="-35"
                x2="160"
                y2="-35"
                stroke={themeAccent}
                strokeWidth="2"
              />

              {/* Landmark Callout Box */}
              <g transform="translate(40, -60)">
                <rect
                  x="0"
                  y="0"
                  width="180"
                  height="42"
                  rx="6"
                  fill="rgba(2, 9, 20, 0.92)"
                  stroke={themeAccent}
                  strokeWidth="1.5"
                />
                <text
                  x="10"
                  y="18"
                  fill={themeAccent}
                  fontSize="12"
                  fontWeight="900"
                  letterSpacing="1"
                >
                  {country.landmark.name}
                </text>
                <text
                  x="10"
                  y="34"
                  fill="#ffffff"
                  fontSize="10"
                  fontWeight="700"
                  opacity="0.9"
                >
                  {country.landmark.detail}
                </text>
              </g>
            </g>
          )}
        </svg>

        {/* Telemetry Coordinate HUD Box */}
        <div
          style={{
            position: 'absolute',
            bottom: 15,
            left: 20,
            padding: '14px 20px',
            backgroundColor: 'rgba(2, 9, 22, 0.88)',
            border: `1.5px solid ${themePrimary}70`,
            borderRadius: 14,
            backdropFilter: 'blur(12px)',
            boxShadow: `0 0 30px ${themePrimary}30`,
            display: 'flex',
            flexDirection: 'column',
            gap: 5,
            zIndex: 20,
          }}
        >
          {/* Flag Ribbon Accent */}
          <div style={{ display: 'flex', gap: 3, marginBottom: 2 }}>
            {country.flagColors?.map((col, i) => (
              <div
                key={i}
                style={{
                  width: 22,
                  height: 4,
                  backgroundColor: col,
                  borderRadius: 2,
                }}
              />
            ))}
          </div>

          <div style={{ color: themePrimary, fontSize: 13, fontWeight: 900, letterSpacing: 2 }}>
            COORDS // {country.coordinates}
          </div>
          <div style={{ color: '#ffffff', fontSize: 20, fontWeight: 900, display: 'flex', alignItems: 'center', gap: 8 }}>
            <span>{country.name.toUpperCase()}</span>
            <span style={{ fontSize: 14, color: themeAccent, fontWeight: 800 }}>[{country.iso}]</span>
          </div>
          <div style={{ color: '#94a3b8', fontSize: 14, fontWeight: 700 }}>
            CAPITAL: <span style={{ color: '#ffffff' }}>{country.capital.toUpperCase()}</span>
          </div>

          {scene.metricLabel && (
            <div
              style={{
                marginTop: 6,
                padding: '6px 12px',
                borderRadius: 8,
                backgroundColor: `${themeAccent}18`,
                border: `1px solid ${themeAccent}50`,
                display: 'inline-flex',
                alignItems: 'center',
                gap: 6,
              }}
            >
              <span style={{ color: themeAccent, fontSize: 13, fontWeight: 900 }}>► {scene.metricLabel}:</span>
              <span style={{ color: '#ffffff', fontSize: 15, fontWeight: 900 }}>{scene.metricValA}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};