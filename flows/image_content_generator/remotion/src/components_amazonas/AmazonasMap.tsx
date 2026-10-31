import React from 'react';
import { interpolate } from 'remotion';
import {
  AMAZON_CITIES,
  AMAZON_RIVERS,
  SA_COUNTRIES,
  SA_VIEWBOX,
} from './amazonas_geo_data';

interface AmazonasMapProps {
  frame: number;
  zoomProgress?: number; // 0 to 1
  scanProgress?: number; // 0 to 1
}

export const AmazonasMap: React.FC<AmazonasMapProps> = ({
  frame,
  zoomProgress = 0,
  scanProgress = 0,
}) => {
  // Camera smooth zoom into the Amazon basin
  // Center of South America is around (500, 700).
  // Amazon river basin is around (520, 370).
  const zoom = interpolate(zoomProgress, [0, 1], [1.0, 2.05], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const panX = interpolate(zoomProgress, [0, 1], [0, -70]);
  const panY = interpolate(zoomProgress, [0, 1], [0, 190]);

  // Current scanned distance in km (0 to 6400)
  const scannedKm = Math.min(6400, Math.round(scanProgress * 6400));

  // Scanning beam head coordinates along the river (from Andes x:240,y:420 to Atlantic x:850,y:250)
  const beamX = interpolate(scanProgress, [0, 1], [230, 850]);
  const beamY = interpolate(
    scanProgress,
    [0, 0.35, 0.7, 1],
    [430, 395, 360, 260]
  );

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: 1080,
        height: 1920,
        backgroundColor: '#020914',
        overflow: 'hidden',
      }}
    >
      {/* 1. Oceanic Background with Deep Topographic Vignette */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: 1080,
          height: 1920,
          background:
            'radial-gradient(circle at 50% 40%, #06192e 0%, #030c18 60%, #01060d 100%)',
        }}
      />

      {/* 2. Scaled Map Wrapper with Camera Pan & Zoom */}
      <div
        style={{
          position: 'absolute',
          top: 260,
          left: 40,
          width: 1000,
          height: 1400,
          transform: `translate(${panX}px, ${panY}px) scale(${zoom})`,
          transformOrigin: '520px 380px',
        }}
      >
        <svg
          viewBox={SA_VIEWBOX}
          width="1000"
          height="1400"
          style={{ overflow: 'visible' }}
        >
          <defs>
            {/* Amazon Rainforest Biome Gradient */}
            <radialGradient id="rainforestGlow" cx="52%" cy="27%" r="35%">
              <stop offset="0%" stopColor="#15803d" stopOpacity="0.45" />
              <stop offset="70%" stopColor="#047857" stopOpacity="0.25" />
              <stop offset="100%" stopColor="#064e3b" stopOpacity="0" />
            </radialGradient>

            {/* Glowing River Filter */}
            <filter id="riverGlow" x="-30%" y="-30%" width="160%" height="160%">
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>

            {/* Scan Pulse Glow */}
            <filter id="scanGlow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="8" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          {/* South America Landmass (Country Polygons) */}
          <g>
            {SA_COUNTRIES.map((c, idx) => {
              const isAmazonCountry = [
                'Brazil',
                'Peru',
                'Colombia',
                'Ecuador',
                'Bolivia',
                'Venezuela',
              ].includes(c.name);

              return (
                <path
                  key={idx}
                  d={c.d}
                  fill={isAmazonCountry ? '#0a221a' : '#07151f'}
                  stroke="rgba(56, 189, 248, 0.2)"
                  strokeWidth="1.2"
                />
              );
            })}
          </g>

          {/* Amazon Rainforest Basin Bio-Glow */}
          <ellipse
            cx="540"
            cy="370"
            rx="320"
            ry="200"
            fill="url(#rainforestGlow)"
          />

          {/* Tributaries Network */}
          <g opacity="0.6">
            {AMAZON_RIVERS.filter((r) => !r.isMain).map((r, idx) => (
              <path
                key={idx}
                d={r.d}
                fill="none"
                stroke="#06b6d4"
                strokeWidth="2.5"
                strokeLinecap="round"
                opacity="0.7"
              />
            ))}
          </g>

          {/* MAIN STEM OF THE AMAZON RIVER (GLOWING ARTERY) */}
          <g filter="url(#riverGlow)">
            {AMAZON_RIVERS.filter((r) => r.isMain).map((r, idx) => (
              <path
                key={idx}
                d={r.d}
                fill="none"
                stroke="#38bdf8"
                strokeWidth="4.5"
                strokeLinecap="round"
              />
            ))}
          </g>

          {/* Key Amazon Cities */}
          {AMAZON_CITIES.map((city, idx) => {
            const offsetY = city.name.includes("Leticia")
              ? 18
              : city.name.includes("Iquitos")
              ? -12
              : city.name.includes("Manaos")
              ? -10
              : 4;
            return (
              <g key={idx} transform={`translate(${city.x}, ${city.y})`}>
                <circle cx="0" cy="0" r="3.5" fill="#f8fafc" />
                <circle
                  cx="0"
                  cy="0"
                  r="7"
                  fill="none"
                  stroke="#38bdf8"
                  strokeWidth="1"
                  opacity="0.8"
                />
                <text
                  x="10"
                  y={offsetY}
                  fill="#e2e8f0"
                  fontSize="12"
                  fontFamily="Consolas, monospace"
                  fontWeight="700"
                  letterSpacing="1"
                  filter="drop-shadow(0 2px 4px rgba(0,0,0,0.9))"
                >
                  {city.name}
                </text>
              </g>
            );
          })}

          {/* ======================================================== */}
          {/* ANIMATED SCANNER / RADAR BEAM SEARCHING FOR BRIDGES      */}
          {/* ======================================================== */}
          {scanProgress > 0 && (
            <g>
              {/* Radar Sweeping Rings at the front of the scan */}
              {[15, 30, 48].map((radius, rIdx) => (
                <circle
                  key={rIdx}
                  cx={beamX}
                  cy={beamY}
                  r={radius + ((frame * 1.5 + rIdx * 12) % 24)}
                  fill="none"
                  stroke="#ef4444"
                  strokeWidth="1.8"
                  opacity={0.7 - rIdx * 0.2}
                />
              ))}

              {/* Laser Core Head */}
              <circle
                cx={beamX}
                cy={beamY}
                r="7"
                fill="#ffffff"
                filter="url(#scanGlow)"
              />

              {/* Scanned Path Trail (Highlighted in Bright Cyan/Red) */}
              <line
                x1="230"
                y1="430"
                x2={beamX}
                y2={beamY}
                stroke="#ef4444"
                strokeWidth="3"
                strokeDasharray="6 6"
                opacity="0.8"
              />
            </g>
          )}
        </svg>
      </div>

      {/* ======================================================== */}
      {/* 3. DYNAMIC BRIDGE SCANNER HUD (CENTER-UPPER OVERLAY)     */}
      {/* ======================================================== */}
      <div
        style={{
          position: 'absolute',
          top: 250,
          left: 100,
          right: 100,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          pointerEvents: 'none',
          zIndex: 50,
        }}
      >
        <div
          style={{
            backgroundColor: 'rgba(5, 15, 30, 0.88)',
            border: '1.5px solid rgba(239, 68, 68, 0.6)',
            borderRadius: 14,
            padding: '12px 24px',
            boxShadow:
              '0 8px 30px rgba(0, 0, 0, 0.9), 0 0 20px rgba(239, 68, 68, 0.25)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 6,
          }}
        >
          <div
            style={{
              fontFamily: 'Consolas, monospace',
              fontSize: 18,
              fontWeight: 800,
              color: '#94a3b8',
              letterSpacing: 2,
              textTransform: 'uppercase',
            }}
          >
            [ ESCÁNER SATELITAL CONTINENTAL ]
          </div>

          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 16,
              margin: '4px 0',
            }}
          >
            <div
              style={{
                fontFamily: 'Consolas, monospace',
                fontSize: 26,
                fontWeight: 900,
                color: '#38bdf8',
                letterSpacing: 1.5,
              }}
            >
              DISTANCIA: {scannedKm.toLocaleString()} KM
            </div>

            <div
              style={{
                width: 2,
                height: 24,
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
              }}
            />

            <div
              style={{
                fontFamily: 'Consolas, monospace',
                fontSize: 26,
                fontWeight: 900,
                color: '#ef4444',
                letterSpacing: 1.5,
                display: 'flex',
                alignItems: 'center',
                gap: 6,
              }}
            >
              <span>🚫</span> PUENTES: 0
            </div>
          </div>

          <div
            style={{
              fontFamily: 'Bahnschrift, Arial, sans-serif',
              fontSize: 16,
              fontWeight: 700,
              color: '#fca5a5',
              letterSpacing: 1,
            }}
          >
            NINGÚN CRUCE ARTIFICIAL EN TODA LA CUENCA PRINCIPAL
          </div>
        </div>
      </div>
    </div>
  );
};
