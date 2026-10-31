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

  // Staggered entrances
  const springA = spring({ frame, fps, config: { damping: 13, stiffness: 90 } });
  const springB = spring({ frame: Math.max(0, frame - 10), fps, config: { damping: 13, stiffness: 90 } });

  // Progress bar fill
  const barProgress = interpolate(frame, [15, 55], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

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
      <div style={{ textAlign: 'center', marginBottom: 25 }}>
        <div style={{ fontSize: 20, letterSpacing: 4, color: accentColor, fontWeight: 800, textTransform: 'uppercase' }}>
          {scene.headline || 'CARA A CARA GEOGRÁFICO'}
        </div>
        <div style={{ fontSize: 32, fontWeight: 900, color: '#ffffff', marginTop: 4 }}>
          {countryA.name.toUpperCase()} <span style={{ color: accentColor }}>VS</span> {countryB.name.toUpperCase()}
        </div>
      </div>

      {/* Comparison Grid */}
      <div
        style={{
          display: 'flex',
          gap: 25,
          width: '100%',
          maxWidth: 960,
          justifyContent: 'center',
          alignItems: 'stretch',
        }}
      >
        {/* Country A Card */}
        <div
          style={{
            flex: 1,
            backgroundColor: 'rgba(2, 9, 22, 0.85)',
            border: `2px solid ${primaryColor}70`,
            borderRadius: 20,
            padding: 24,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            boxShadow: `0 0 30px ${primaryColor}20`,
            transform: `scale(${springA})`,
          }}
        >
          <div style={{ fontSize: 22, fontWeight: 900, color: '#ffffff', marginBottom: 12 }}>
            {countryA.name.toUpperCase()}
          </div>

          {/* SVG Silhouette */}
          <div style={{ width: '100%', height: 260, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <svg
              viewBox={countryA.viewBox}
              style={{
                maxWidth: '90%',
                maxHeight: '90%',
                filter: `drop-shadow(0 0 20px ${primaryColor}60)`,
              }}
            >
              <path
                d={countryA.path}
                fill={`${primaryColor}25`}
                stroke={primaryColor}
                strokeWidth="3"
              />
            </svg>
          </div>

          {/* Metric Bar */}
          <div style={{ width: '100%', marginTop: 15 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 16, fontWeight: 800, color: '#ffffff', marginBottom: 6 }}>
              <span>{scene.metricLabel || 'DATO CLAVE'}</span>
              <span style={{ color: primaryColor }}>{scene.metricValA || '100%'}</span>
            </div>
            <div style={{ width: '100%', height: 10, backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 5, overflow: 'hidden' }}>
              <div
                style={{
                  height: '100%',
                  width: `${barProgress * 70}%`,
                  backgroundColor: primaryColor,
                  boxShadow: `0 0 10px ${primaryColor}`,
                }}
              />
            </div>
          </div>
        </div>

        {/* Central VS Pill */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 8,
          }}
        >
          <div
            style={{
              width: 54,
              height: 54,
              borderRadius: '50%',
              backgroundColor: '#0a0f1d',
              border: `2px solid ${accentColor}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: accentColor,
              fontWeight: 900,
              fontSize: 18,
              boxShadow: `0 0 25px ${accentColor}60`,
            }}
          >
            VS
          </div>
        </div>

        {/* Country B Card */}
        <div
          style={{
            flex: 1,
            backgroundColor: 'rgba(2, 9, 22, 0.85)',
            border: `2px solid ${secondaryColor}70`,
            borderRadius: 20,
            padding: 24,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            boxShadow: `0 0 30px ${secondaryColor}20`,
            transform: `scale(${springB})`,
          }}
        >
          <div style={{ fontSize: 22, fontWeight: 900, color: '#ffffff', marginBottom: 12 }}>
            {countryB.name.toUpperCase()}
          </div>

          {/* SVG Silhouette */}
          <div style={{ width: '100%', height: 260, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <svg
              viewBox={countryB.viewBox}
              style={{
                maxWidth: '90%',
                maxHeight: '90%',
                filter: `drop-shadow(0 0 20px ${secondaryColor}60)`,
              }}
            >
              <path
                d={countryB.path}
                fill={`${secondaryColor}25`}
                stroke={secondaryColor}
                strokeWidth="3"
              />
            </svg>
          </div>

          {/* Metric Bar */}
          <div style={{ width: '100%', marginTop: 15 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 16, fontWeight: 800, color: '#ffffff', marginBottom: 6 }}>
              <span>{scene.metricLabel || 'DATO CLAVE'}</span>
              <span style={{ color: secondaryColor }}>{scene.metricValB || '100%'}</span>
            </div>
            <div style={{ width: '100%', height: 10, backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 5, overflow: 'hidden' }}>
              <div
                style={{
                  height: '100%',
                  width: `${barProgress * 95}%`,
                  backgroundColor: secondaryColor,
                  boxShadow: `0 0 10px ${secondaryColor}`,
                }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Comparison Callout Footer */}
      <div
        style={{
          marginTop: 25,
          padding: '12px 30px',
          backgroundColor: 'rgba(245, 158, 11, 0.12)',
          border: `1px solid ${accentColor}60`,
          borderRadius: 30,
          color: '#ffffff',
          fontSize: 18,
          fontWeight: 800,
          letterSpacing: 1,
          textAlign: 'center',
          boxShadow: `0 0 20px ${accentColor}25`,
        }}
      >
        ► {scene.subheadline || 'ANÁLISIS COMPARATIVO ENIGMAIQ'}
      </div>
    </div>
  );
};
