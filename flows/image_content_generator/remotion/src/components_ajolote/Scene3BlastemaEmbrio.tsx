import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { HeaderAjolote } from './HeaderAjolote';

export const Scene3BlastemaEmbrio: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 90 },
  });

  // Nerve electrical pulse traveling through axon
  const pulseOffset = (frame * 6) % 240;

  // Blastema growth expansion
  const blastemaGrowth = interpolate(frame, [20, 160], [0.3, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Cell division mitosis pulsing
  const cellPulse = Math.sin(frame * 0.15) * 3;

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: 10,
      }}
    >
      <HeaderAjolote
        category="DESDIFERENCIACIÓN Y"
        categoryHighlight="BLASTEMA"
        bigMetric="BLASTEMA VIVO"
        metricSubtitle="los nervios activan el retroceso celular a estado embrionario"
        badgeText="MILAGRO BIOLÓGICO"
        badgeColor="#38bdf8"
      />

      {/* Main Framed Stage */}
      <div
        style={{
          position: 'absolute',
          top: 365,
          left: 60,
          right: 60,
          height: 1000,
          border: '1.5px solid rgba(255, 255, 255, 0.15)',
          backgroundColor: 'rgba(11, 14, 20, 0.92)',
          backdropFilter: 'blur(10px)',
          borderRadius: 16,
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '24px 30px',
          zIndex: 15,
        }}
      >
        <div
          style={{
            alignSelf: 'flex-start',
            color: '#38bdf8',
            fontFamily: 'Consolas, monospace',
            fontSize: 16,
            letterSpacing: 2,
            display: 'flex',
            gap: 15,
          }}
        >
          <span>SEÑALIZACIÓN NEUROTRÓFICA</span>
          <span style={{ color: '#64748b' }}>|</span>
          <span style={{ color: '#fbbf24' }}>INMERSIÓN EN EL MUÑÓN</span>
        </div>

        {/* Anatomical Cross Section & Blastema Stage */}
        <div style={{ width: '100%', height: 780, position: 'relative' }}>
          <svg width="100%" height="100%" viewBox="0 0 900 780">
            <defs>
              <linearGradient id="nerveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#f59e0b" />
                <stop offset="100%" stopColor="#fef08a" />
              </linearGradient>

              <radialGradient id="blastemaGrad" cx="70%" cy="50%" r="60%">
                <stop offset="0%" stopColor="#67e8f9" stopOpacity="0.9" />
                <stop offset="50%" stopColor="#0284c7" stopOpacity="0.7" />
                <stop offset="100%" stopColor="#082f49" stopOpacity="0.4" />
              </radialGradient>
            </defs>

            {/* Arm Stump Graphic Container */}
            <g transform={`scale(${entrance})`} style={{ transformOrigin: '450px 360px' }}>
              {/* Healthy Arm Stump Base (Left Side) */}
              <g transform="translate(100, 200)">
                {/* Arm Tissue Outline */}
                <path
                  d="M 50 40 L 400 40 L 400 320 L 50 320 Z"
                  fill="rgba(244, 114, 182, 0.15)"
                  stroke="#db2777"
                  strokeWidth="2.5"
                />

                {/* Skin Layer */}
                <rect x="50" y="32" width="350" height="12" fill="#fda4af" />
                <rect x="50" y="316" width="350" height="12" fill="#fda4af" />

                {/* Bone / Skeletal Core */}
                <rect x="50" y="145" width="350" height="70" rx="10" fill="#f1f5f9" stroke="#94a3b8" strokeWidth="2" />
                <text x="140" y="188" fill="#475569" fontFamily="Consolas, monospace" fontSize="18" fontWeight="bold">
                  HÚMERO / HUESO
                </text>

                {/* Muscle Fibers (Reddish) */}
                <rect x="50" y="44" width="350" height="100" fill="rgba(239, 68, 68, 0.25)" stroke="#ef4444" strokeWidth="1" strokeDasharray="6 3" />
                <rect x="50" y="216" width="350" height="100" fill="rgba(239, 68, 68, 0.25)" stroke="#ef4444" strokeWidth="1" strokeDasharray="6 3" />
                <text x="80" y="100" fill="#f87171" fontFamily="Consolas, monospace" fontSize="14">MÚSCULO ESQUELÉTICO</text>

                {/* Yellow Nerve Trunk Running Through Stump */}
                <path
                  d="M 50 120 C 180 120 280 160 400 180"
                  stroke="url(#nerveGrad)"
                  strokeWidth="8"
                  fill="none"
                  strokeLinecap="round"
                />
                {/* Electrical nerve spark pulse */}
                <circle
                  cx={50 + pulseOffset * 1.4}
                  cy={120 + Math.sin(pulseOffset * 0.05) * 25 + (pulseOffset * 0.2)}
                  r="7"
                  fill="#ffffff"
                  filter="drop-shadow(0 0 6px #facc15)"
                />

                {/* Amputation Cut Line Marker */}
                <line x1="400" y1="20" x2="400" y2="340" stroke="#f43f5e" strokeWidth="3" strokeDasharray="6 4" />
                <text x="360" y="15" fill="#f43f5e" fontFamily="Consolas, monospace" fontSize="13">CORTE</text>

                {/* ================================================= */}
                {/* THE BLASTEMA BUD EXPANDING FROM STUMP (RIGHT SIDE)*/}
                {/* ================================================= */}
                <g transform={`translate(400, 180) scale(${blastemaGrowth})`}>
                  {/* Glowing Blastema Dome */}
                  <path
                    d="M 0 -140 C 160 -120 280 -60 300 0 C 280 60 160 120 0 140 Z"
                    fill="url(#blastemaGrad)"
                    stroke="#38bdf8"
                    strokeWidth="3"
                  />

                  {/* Pulsing Progenitor Cells inside Blastema */}
                  {[
                    { x: 50, y: -60, r: 12 },
                    { x: 90, y: -20, r: 14 },
                    { x: 70, y: 40, r: 11 },
                    { x: 140, y: -45, r: 13 },
                    { x: 160, y: 15, r: 15 },
                    { x: 120, y: 65, r: 10 },
                    { x: 210, y: -10, r: 12 },
                    { x: 240, y: 10, r: 9 },
                  ].map((cell, idx) => (
                    <g key={idx} transform={`translate(${cell.x}, ${cell.y})`}>
                      <circle
                        cx="0"
                        cy="0"
                        r={cell.r + cellPulse}
                        fill="#06b6d4"
                        stroke="#e0f2fe"
                        strokeWidth="2"
                        opacity="0.9"
                      />
                      <circle cx="2" cy="-2" r="3" fill="#ffffff" />
                    </g>
                  ))}

                  {/* Apical Epithelial Cap (AEC) - Outer Protective Skin */}
                  <path
                    d="M 270 -50 C 315 -20 315 20 270 50"
                    stroke="#e0e7ff"
                    strokeWidth="5"
                    fill="none"
                    strokeLinecap="round"
                  />
                  <text x="210" y="-85" fill="#e0e7ff" fontFamily="Consolas, monospace" fontSize="13" fontWeight="bold">
                    CAPUCHÓN APICAL (AEC)
                  </text>
                </g>
              </g>

              {/* Callout Card 1: Nerve Signal Requirement */}
              <g transform="translate(60, 580)">
                <rect width="360" height="110" rx="10" fill="rgba(15, 23, 42, 0.95)" stroke="#fbbf24" strokeWidth="1.5" />
                <text x="18" y="32" fill="#fbbf24" fontFamily="Consolas, monospace" fontSize="14" fontWeight="bold">
                  FACTORES DE CRECIMIENTO:
                </text>
                <text x="18" y="62" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="20" fontWeight="bold">
                  SEÑALES DEL NERVIO (nAG)
                </text>
                <text x="18" y="90" fill="#94a3b8" fontFamily="Consolas, monospace" fontSize="13">
                  Sin axón conectado, el blastema colapsa
                </text>
              </g>

              {/* Callout Card 2: Mitosis Explosion */}
              <g transform="translate(480, 580)">
                <rect width="360" height="110" rx="10" fill="rgba(15, 23, 42, 0.95)" stroke="#38bdf8" strokeWidth="1.5" />
                <text x="18" y="32" fill="#38bdf8" fontFamily="Consolas, monospace" fontSize="14" fontWeight="bold">
                  POTENCIA REGENERATIVA:
                </text>
                <text x="18" y="62" fill="#ffffff" fontFamily="Bahnschrift, sans-serif" fontSize="20" fontWeight="bold">
                  DESDIFERENCIACIÓN TOTAL
                </text>
                <text x="18" y="90" fill="#94a3b8" fontFamily="Consolas, monospace" fontSize="13">
                  Las células retroceden a estado embrionario
                </text>
              </g>
            </g>
          </svg>
        </div>

        {/* Bottom Status Chip */}
        <div
          style={{
            backgroundColor: 'rgba(20, 26, 36, 0.95)',
            border: '1.5px solid #38bdf8',
            borderRadius: 10,
            padding: '12px 30px',
            fontFamily: 'Consolas, monospace',
            fontSize: 20,
            fontWeight: 800,
            color: '#38bdf8',
            letterSpacing: 2,
          }}
        >
          LAS CÉLULAS ADULTAS RETROCEDEN EN EL TIEMPO PARA FORMAR EL BLASTEMA
        </div>
      </div>
    </div>
  );
};
