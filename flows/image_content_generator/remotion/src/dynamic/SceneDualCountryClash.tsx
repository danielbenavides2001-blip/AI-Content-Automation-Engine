import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { COUNTRY_SILHOUETTES, SilhouetteData } from '../country_silhouettes';
import { DynamicScene } from './types';

export const SceneDualCountryClash: React.FC<{
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

  const cKeyA = (scene.countryA || 'colombia').toLowerCase();
  const cKeyB = (scene.countryB || 'ecuador').toLowerCase();

  const countryA: SilhouetteData = COUNTRY_SILHOUETTES[cKeyA] || COUNTRY_SILHOUETTES['colombia'];
  const countryB: SilhouetteData = COUNTRY_SILHOUETTES[cKeyB] || COUNTRY_SILHOUETTES['ecuador'];

  const colorA = countryA.primary || primaryColor;
  const colorB = countryB.accent || secondaryColor;

  // Staggered entrances
  const springA = spring({ frame, fps, config: { damping: 13, stiffness: 85 } });
  const springB = spring({ frame: Math.max(0, frame - 8), fps, config: { damping: 13, stiffness: 85 } });

  // Progress bar fill animation
  const barProgress = interpolate(frame, [15, 55], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const vsPulse = Math.sin(frame * 0.18) * 0.2 + 0.8;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '110px 35px 320px 35px',
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
            {scene.headline || 'CARA A CARA GEOGRÁFICO & COMPARATIVA'}
          </span>
        </div>

        <div
          style={{
            fontSize: 34,
            fontWeight: 900,
            color: '#ffffff',
            lineHeight: 1.15,
            textShadow: '0 4px 24px rgba(0,0,0,0.9)',
          }}
        >
          <span style={{ color: colorA }}>{countryA.name.toUpperCase()}</span>{' '}
          <span style={{ color: accentColor, margin: '0 8px' }}>VS</span>{' '}
          <span style={{ color: colorB }}>{countryB.name.toUpperCase()}</span>
        </div>
      </div>

      {/* 2. Side-by-Side Dual Country Cards */}
      <div
        style={{
          position: 'relative',
          display: 'flex',
          gap: 20,
          width: '100%',
          maxWidth: 980,
          justifyContent: 'center',
          alignItems: 'stretch',
        }}
      >
        {/* Country A Card */}
        <div
          style={{
            flex: 1,
            backgroundColor: 'rgba(2, 9, 22, 0.90)',
            border: `2px solid ${colorA}80`,
            borderRadius: 22,
            padding: '24px 20px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            boxShadow: `0 0 35px ${colorA}25`,
            transform: `scale(${springA})`,
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          {/* Flag Ribbon */}
          <div style={{ display: 'flex', gap: 3, width: '100%', marginBottom: 12 }}>
            {countryA.flagColors?.map((c, i) => (
              <div key={i} style={{ flex: 1, height: 4, backgroundColor: c, borderRadius: 2 }} />
            ))}
          </div>

          <div style={{ fontSize: 22, fontWeight: 900, color: '#ffffff', marginBottom: 6 }}>
            {countryA.name.toUpperCase()}
          </div>
          <div style={{ fontSize: 13, fontWeight: 800, color: colorA, letterSpacing: 1.5, marginBottom: 12 }}>
            [{countryA.iso}] • {countryA.capital.toUpperCase()}
          </div>

          {/* SVG Silhouette A */}
          <div
            style={{
              width: '100%',
              height: 270,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              position: 'relative',
            }}
          >
            {/* Soft Ambient Spotlight behind country */}
            <div
              style={{
                position: 'absolute',
                width: 180,
                height: 180,
                borderRadius: '50%',
                background: `radial-gradient(circle, ${colorA}30 0%, transparent 70%)`,
              }}
            />
            <svg
              viewBox={countryA.viewBox}
              style={{
                maxWidth: '92%',
                maxHeight: '92%',
                filter: `drop-shadow(0 0 25px ${colorA}90)`,
              }}
            >
              <defs>
                <linearGradient id={`gradA-${countryA.name}`} x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor={`${colorA}75`} />
                  <stop offset="100%" stopColor={`${colorA}25`} />
                </linearGradient>
              </defs>
              <path
                d={countryA.path}
                fill={`url(#gradA-${countryA.name})`}
                stroke={colorA}
                strokeWidth="3.5"
              />
              {/* Inner concentric contour */}
              <path
                d={countryA.path}
                fill="none"
                stroke={colorA}
                strokeWidth="1.2"
                transform="scale(0.85) translate(50, 50)"
                strokeDasharray="4 4"
                opacity="0.6"
              />
            </svg>
          </div>

          {/* Metric Bar Card A */}
          <div style={{ width: '100%', marginTop: 14 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 15, fontWeight: 800, color: '#ffffff', marginBottom: 6 }}>
              <span style={{ color: '#94a3b8' }}>{scene.metricLabel || 'VALOR REGISTRADO'}</span>
              <span style={{ color: colorA, fontSize: 18, fontWeight: 900 }}>{scene.metricValA || '100%'}</span>
            </div>
            <div style={{ width: '100%', height: 12, backgroundColor: 'rgba(255,255,255,0.08)', borderRadius: 6, overflow: 'hidden' }}>
              <div
                style={{
                  height: '100%',
                  width: `${barProgress * 85}%`,
                  backgroundColor: colorA,
                  boxShadow: `0 0 16px ${colorA}`,
                }}
              />
            </div>
          </div>
        </div>

        {/* Central VS Badge */}
        <div
          style={{
            position: 'absolute',
            top: '45%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            zIndex: 30,
            width: 64,
            height: 64,
            borderRadius: '50%',
            backgroundColor: '#020914',
            border: `2.5px solid ${accentColor}`,
            boxShadow: `0 0 30px ${accentColor}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transformOrigin: 'center center',
          }}
        >
          <span
            style={{
              color: accentColor,
              fontSize: 22,
              fontWeight: 900,
              transform: `scale(${vsPulse})`,
            }}
          >
            VS
          </span>
        </div>

        {/* Country B Card */}
        <div
          style={{
            flex: 1,
            backgroundColor: 'rgba(2, 9, 22, 0.90)',
            border: `2px solid ${colorB}80`,
            borderRadius: 22,
            padding: '24px 20px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            boxShadow: `0 0 35px ${colorB}25`,
            transform: `scale(${springB})`,
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          {/* Flag Ribbon */}
          <div style={{ display: 'flex', gap: 3, width: '100%', marginBottom: 12 }}>
            {countryB.flagColors?.map((c, i) => (
              <div key={i} style={{ flex: 1, height: 4, backgroundColor: c, borderRadius: 2 }} />
            ))}
          </div>

          <div style={{ fontSize: 22, fontWeight: 900, color: '#ffffff', marginBottom: 6 }}>
            {countryB.name.toUpperCase()}
          </div>
          <div style={{ fontSize: 13, fontWeight: 800, color: colorB, letterSpacing: 1.5, marginBottom: 12 }}>
            [{countryB.iso}] • {countryB.capital.toUpperCase()}
          </div>

          {/* SVG Silhouette B */}
          <div
            style={{
              width: '100%',
              height: 270,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              position: 'relative',
            }}
          >
            {/* Soft Ambient Spotlight behind country */}
            <div
              style={{
                position: 'absolute',
                width: 180,
                height: 180,
                borderRadius: '50%',
                background: `radial-gradient(circle, ${colorB}30 0%, transparent 70%)`,
              }}
            />
            <svg
              viewBox={countryB.viewBox}
              style={{
                maxWidth: '92%',
                maxHeight: '92%',
                filter: `drop-shadow(0 0 25px ${colorB}90)`,
              }}
            >
              <defs>
                <linearGradient id={`gradB-${countryB.name}`} x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stopColor={`${colorB}75`} />
                  <stop offset="100%" stopColor={`${colorB}25`} />
                </linearGradient>
              </defs>
              <path
                d={countryB.path}
                fill={`url(#gradB-${countryB.name})`}
                stroke={colorB}
                strokeWidth="3.5"
              />
              {/* Inner concentric contour */}
              <path
                d={countryB.path}
                fill="none"
                stroke={colorB}
                strokeWidth="1.2"
                transform="scale(0.85) translate(50, 50)"
                strokeDasharray="4 4"
                opacity="0.6"
              />
            </svg>
          </div>

          {/* Metric Bar Card B */}
          <div style={{ width: '100%', marginTop: 14 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 15, fontWeight: 800, color: '#ffffff', marginBottom: 6 }}>
              <span style={{ color: '#94a3b8' }}>{scene.metricLabel || 'VALOR REGISTRADO'}</span>
              <span style={{ color: colorB, fontSize: 18, fontWeight: 900 }}>{scene.metricValB || '100%'}</span>
            </div>
            <div style={{ width: '100%', height: 12, backgroundColor: 'rgba(255,255,255,0.08)', borderRadius: 6, overflow: 'hidden' }}>
              <div
                style={{
                  height: '100%',
                  width: `${barProgress * 70}%`,
                  backgroundColor: colorB,
                  boxShadow: `0 0 16px ${colorB}`,
                }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};