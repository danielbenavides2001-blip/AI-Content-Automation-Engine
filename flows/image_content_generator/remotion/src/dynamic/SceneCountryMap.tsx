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

  // Smooth entrance spring
  const scale = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 80, mass: 0.9 },
  });

  // Animated laser outline stroke-dashoffset
  const strokeProgress = interpolate(frame, [0, 45], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Holographic scan line sweep
  const scanY = (frame * 6) % 650;

  // Beacon pulse on coordinates
  const pulse = Math.sin(frame * 0.1) * 0.3 + 0.7;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '120px 40px 320px 40px',
        boxSizing: 'border-box',
        fontFamily: "'Bahnschrift', 'Montserrat', Arial, sans-serif",
      }}
    >
      {/* Top Scene Headline */}
      <div
        style={{
          textAlign: 'center',
          marginBottom: 30,
          opacity: Math.min(1, frame / 15),
          transform: `translateY(${interpolate(frame, [0, 15], [-20, 0], { extrapolateRight: 'clamp' })}px)`,
        }}
      >
        <div
          style={{
            fontSize: 22,
            letterSpacing: 4,
            color: primaryColor,
            fontWeight: 800,
            textTransform: 'uppercase',
            marginBottom: 8,
          }}
        >
          {scene.headline || 'ANOMALÍA CARTOGRÁFICA'}
        </div>
        <div
          style={{
            fontSize: 34,
            fontWeight: 900,
            color: '#ffffff',
            lineHeight: 1.15,
            maxWidth: 900,
            textShadow: '0 4px 20px rgba(0,0,0,0.8)',
          }}
        >
          {scene.subheadline || country.name.toUpperCase()}
        </div>
      </div>

      {/* Main Map Container */}
      <div
        style={{
          position: 'relative',
          width: '100%',
          maxWidth: 680,
          height: 680,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transform: `scale(${scale})`,
        }}
      >
        {/* Radar concentric rings behind map */}
        <svg
          width="680"
          height="680"
          style={{
            position: 'absolute',
            inset: 0,
            opacity: 0.25,
            transform: `rotate(${frame * 0.2}deg)`,
          }}
        >
          <circle cx="340" cy="340" r="150" fill="none" stroke={secondaryColor} strokeWidth="1" strokeDasharray="6 6" />
          <circle cx="340" cy="340" r="240" fill="none" stroke={primaryColor} strokeWidth="1.5" />
          <circle cx="340" cy="340" r="320" fill="none" stroke={secondaryColor} strokeWidth="1" strokeDasharray="8 8" />
          <line x1="20" y1="340" x2="660" y2="340" stroke={secondaryColor} strokeWidth="0.8" />
          <line x1="340" y1="20" x2="340" y2="660" stroke={secondaryColor} strokeWidth="0.8" />
        </svg>

        {/* Vector SVG Country Silhouette */}
        <svg
          viewBox={country.viewBox}
          style={{
            width: '85%',
            height: '85%',
            filter: `drop-shadow(0 0 35px ${primaryColor}70)`,
          }}
        >
          <defs>
            <linearGradient id={`grad-${country.name}`} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={`${primaryColor}35`} />
              <stop offset="100%" stopColor={`${secondaryColor}15`} />
            </linearGradient>
            <clipPath id="mapClip">
              <path d={country.path} />
            </clipPath>
          </defs>

          {/* Map Fill */}
          <path
            d={country.path}
            fill={`url(#grad-${country.name})`}
            stroke={primaryColor}
            strokeWidth="3.5"
            strokeDasharray="1600"
            strokeDashoffset={1600 * strokeProgress}
          />

          {/* Internal Topographic Contours inside map */}
          <g clipPath="url(#mapClip)" opacity={0.6}>
            <line
              x1="0"
              y1={scanY}
              x2="600"
              y2={scanY}
              stroke="#ffffff"
              strokeWidth="3"
              opacity={0.8}
            />
            <path
              d={country.path}
              fill="none"
              stroke={secondaryColor}
              strokeWidth="1.5"
              transform="scale(0.92) translate(25, 25)"
              strokeDasharray="4 4"
            />
          </g>
        </svg>

        {/* Telemetry Coordinate HUD Box */}
        <div
          style={{
            position: 'absolute',
            bottom: 20,
            left: 20,
            padding: '12px 18px',
            backgroundColor: 'rgba(2, 9, 20, 0.85)',
            border: `1px solid ${primaryColor}60`,
            borderRadius: 12,
            backdropFilter: 'blur(10px)',
            boxShadow: `0 0 25px ${primaryColor}25`,
            display: 'flex',
            flexDirection: 'column',
            gap: 4,
          }}
        >
          <div style={{ color: primaryColor, fontSize: 13, fontWeight: 800, letterSpacing: 1.5 }}>
            COORDS // {country.coordinates}
          </div>
          <div style={{ color: '#ffffff', fontSize: 18, fontWeight: 900 }}>
            {country.name.toUpperCase()} • CAPITAL: {country.capital.toUpperCase()}
          </div>
          {scene.metricLabel && (
            <div style={{ color: accentColor, fontSize: 15, fontWeight: 800, marginTop: 4 }}>
              ► {scene.metricLabel}: <span style={{ color: '#ffffff' }}>{scene.metricValA}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
