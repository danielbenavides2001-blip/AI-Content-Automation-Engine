import React from 'react';
import {
  Audio,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

// Timed script sentences and subtitle windows (aligned to mar_salado_voice.mp3: 67 seconds)
export const MAR_SALADO_TOTAL_FRAMES = 2010;
export const MAR_SALADO_FPS = 30;

const SUBTITLES = [
  { start: 0, end: 5.8, words: '¿Por qué el mar es salado si los ríos que llegan a él son de agua dulce?'.split(' ') },
  { start: 5.8, end: 14.5, words: 'Todo empieza con la lluvia. Al caer, el agua atrapa dióxido de carbono y se vuelve ácida.'.split(' ') },
  { start: 14.5, end: 27.8, words: 'Esa lluvia desgasta las rocas continentales y les arranca minerales como el sodio y el cloruro. Los ríos los llevan al mar.'.split(' ') },
  { start: 27.8, end: 42.5, words: 'Y aquí está el secreto: el sol evapora el agua pura, pero la sal no se evapora, se queda acumulada durante millones de años.'.split(' ') },
  { start: 42.5, end: 55.5, words: 'Hoy cada litro de mar tiene unos 35 gramos de sal. Si la sacáramos toda, formaría una capa de más de 150 metros de alto.'.split(' ') },
  { start: 55.5, end: 67.0, words: 'El océano no es salado por casualidad: guarda millones de años de historia. Esto es EnigmaIQ.'.split(' ') },
];

export const ElPorqueDeTodoMarSalado: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const currentTimeSec = frame / fps;

  // Active subtitle group
  const activeSub = SUBTITLES.find((s) => currentTimeSec >= s.start && currentTimeSec < s.end) || SUBTITLES[0];
  const subProgress = Math.min(1, Math.max(0, (currentTimeSec - activeSub.start) / Math.max(0.1, activeSub.end - activeSub.start)));
  const activeWordIdx = Math.min(activeSub.words.length - 1, Math.floor(subProgress * activeSub.words.length));

  // Sun & Evaporation animation parameters (Scene 4)
  const sunPulse = Math.sin(frame * 0.1) * 0.15 + 0.85;
  const sunRotate = (frame * 0.5) % 360;
  const dropletDrift = (frame * 2.5) % 200;

  return (
    <div
      style={{
        position: 'relative',
        width: 1080,
        height: 1920,
        backgroundColor: '#020914',
        overflow: 'hidden',
        fontFamily: "'Bahnschrift', 'Montserrat', Arial, sans-serif",
      }}
    >
      {/* ======================================================== */}
      {/* 1. SEQUENTIAL VISUAL LAYERS BY NARRATIVE BEAT            */}
      {/* ======================================================== */}

      {/* BEAT 1: Ocean Shore Hook (0s - 5.8s / 0 - 174 frames) */}
      <Sequence from={0} durationInFrames={175}>
        <OffthreadVideo
          src={staticFile('mar_salado_assets/scene1_ocean.mp4')}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        {/* Dark Vignette Overlay */}
        <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to bottom, rgba(2,9,20,0.6) 0%, transparent 40%, rgba(2,9,20,0.7) 100%)' }} />

        {/* Central Hook Card */}
        <div
          style={{
            position: 'absolute',
            top: 260,
            left: 55,
            right: 55,
            padding: '36px 30px',
            backgroundColor: 'rgba(11, 23, 42, 0.92)',
            border: '3.5px solid #f59e0b',
            borderRadius: 24,
            boxShadow: '0 0 35px rgba(245, 158, 11, 0.35)',
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: 38, fontWeight: 900, color: '#ffffff', letterSpacing: 1.5, marginBottom: 8, textTransform: 'uppercase' }}>
            ¿POR QUÉ EL MAR
          </div>
          <div style={{ fontSize: 48, fontWeight: 900, color: '#f59e0b', letterSpacing: 2, textTransform: 'uppercase' }}>
            ES SALADO?
          </div>
        </div>
      </Sequence>

      {/* BEAT 2: Rain & Atmosphere (5.8s - 14.5s / 175 - 435 frames) */}
      <Sequence from={175} durationInFrames={260}>
        <OffthreadVideo
          src={staticFile('mar_salado_assets/scene2_rain.mp4')}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to bottom, rgba(2,9,20,0.5) 0%, transparent 50%, rgba(2,9,20,0.75) 100%)' }} />

        {/* Informative Header Banner */}
        <div
          style={{
            position: 'absolute',
            top: 250,
            left: '50%',
            transform: 'translateX(-50%)',
            padding: '10px 28px',
            borderRadius: 30,
            backgroundColor: 'rgba(11, 23, 42, 0.88)',
            border: '2px solid #38bdf8',
            color: '#ffffff',
            fontSize: 20,
            fontWeight: 900,
            letterSpacing: 2,
            boxShadow: '0 0 25px rgba(56, 189, 248, 0.3)',
            whiteSpace: 'nowrap',
          }}
        >
          EL ORIGEN // <span style={{ color: '#38bdf8' }}>LLUVIA ÁCIDA & CO₂</span>
        </div>
      </Sequence>

      {/* BEAT 3: Continental Erosion & Rivers (14.5s - 27.8s / 435 - 835 frames) */}
      <Sequence from={435} durationInFrames={400}>
        <OffthreadVideo
          src={staticFile('mar_salado_assets/scene3_river.mp4')}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to bottom, rgba(2,9,20,0.5) 0%, transparent 50%, rgba(2,9,20,0.75) 100%)' }} />

        {/* Informative Header Banner */}
        <div
          style={{
            position: 'absolute',
            top: 250,
            left: '50%',
            transform: 'translateX(-50%)',
            padding: '10px 28px',
            borderRadius: 30,
            backgroundColor: 'rgba(11, 23, 42, 0.88)',
            border: '2px solid #f59e0b',
            color: '#ffffff',
            fontSize: 20,
            fontWeight: 900,
            letterSpacing: 2,
            boxShadow: '0 0 25px rgba(245, 158, 11, 0.3)',
            whiteSpace: 'nowrap',
          }}
        >
          TRANSPORTE FLUVIAL // <span style={{ color: '#f59e0b' }}>SODIO & CLORURO</span>
        </div>
      </Sequence>

      {/* BEAT 4: 2D Evaporation Diagram (27.8s - 42.5s / 835 - 1275 frames) */}
      <Sequence from={835} durationInFrames={440}>
        <div
          style={{
            position: 'absolute',
            inset: 0,
            backgroundColor: '#051329',
            overflow: 'hidden',
          }}
        >
          {/* Top Title */}
          <div
            style={{
              position: 'absolute',
              top: 230,
              width: '100%',
              textAlign: 'center',
              fontSize: 38,
              fontWeight: 900,
              color: '#f59e0b',
              letterSpacing: 3,
            }}
          >
            EL SECRETO
          </div>

          <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{ position: 'absolute', inset: 0 }}>
            <defs>
              <linearGradient id="oceanEvapGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#0284c7" />
                <stop offset="100%" stopColor="#082f49" />
              </linearGradient>
            </defs>

            {/* Radiant Sun in Upper Right */}
            <g transform="translate(820, 480)">
              {/* Sun Rays */}
              <g transform={`rotate(${sunRotate})`}>
                {Array.from({ length: 12 }).map((_, i) => (
                  <line
                    key={i}
                    x1="0"
                    y1="95"
                    x2="0"
                    y2="135"
                    stroke="#facc15"
                    strokeWidth="7"
                    strokeLinecap="round"
                    transform={`rotate(${i * 30})`}
                  />
                ))}
              </g>
              {/* Sun Body */}
              <circle cx="0" cy="0" r="75" fill="#facc15" />
            </g>

            {/* Rising Evaporation Droplets */}
            {Array.from({ length: 28 }).map((_, i) => {
              const x = 160 + (i * 33) % 760;
              const baseY = 1100 - ((i * 47 + dropletDrift * 3) % 450);
              return (
                <path
                  key={i}
                  d={`M ${x} ${baseY} Q ${x - 5} ${baseY + 12} ${x} ${baseY + 18} Q ${x + 5} ${baseY + 12} ${x} ${baseY} Z`}
                  fill="#38bdf8"
                  opacity="0.8"
                />
              );
            })}

            {/* Evaporation Arrow Callout */}
            <g transform="translate(180, 680)">
              <text x="0" y="0" fill="#38bdf8" fontSize="28" fontWeight="900">
                AGUA ↑
              </text>
              <text x="0" y="32" fill="#ffffff" fontSize="20" fontWeight="700">
                se evapora pura
              </text>
            </g>

            {/* Ocean Sea Layer */}
            <path
              d="M 0 1120 Q 270 1080 540 1120 T 1080 1100 L 1080 1920 L 0 1920 Z"
              fill="url(#oceanEvapGrad)"
            />

            {/* Precipitating Salt Crystals (White Squares) accumulating at seabed */}
            {Array.from({ length: 60 }).map((_, i) => {
              const sx = 60 + (i * 37) % 960;
              const sy = 1200 + (i * 23) % 400;
              return (
                <rect
                  key={i}
                  x={sx}
                  y={sy}
                  width="12"
                  height="12"
                  rx="2"
                  fill="#ffffff"
                  opacity="0.9"
                />
              );
            })}
          </svg>
        </div>
      </Sequence>

      {/* BEAT 5: Deep Ocean & 35g Metric Card (42.5s - 55.5s / 1275 - 1665 frames) */}
      <Sequence from={1275} durationInFrames={390}>
        <OffthreadVideo
          src={staticFile('mar_salado_assets/scene5_ocean_deep.mp4')}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        <div style={{ position: 'absolute', inset: 0, background: 'rgba(2, 9, 20, 0.45)' }} />

        {/* Metric Card A: 35g de sal por litro */}
        {frame < 1470 ? (
          <div
            style={{
              position: 'absolute',
              top: 320,
              left: 60,
              right: 60,
              padding: '45px 30px',
              backgroundColor: 'rgba(11, 23, 42, 0.92)',
              border: '3.5px solid #f59e0b',
              borderRadius: 24,
              boxShadow: '0 0 35px rgba(245, 158, 11, 0.35)',
              textAlign: 'center',
            }}
          >
            <div style={{ fontSize: 88, fontWeight: 900, color: '#f59e0b', letterSpacing: 2, marginBottom: 8 }}>
              35 g
            </div>
            <div style={{ fontSize: 26, fontWeight: 800, color: '#ffffff', letterSpacing: 1 }}>
              de sal por cada litro
            </div>
          </div>
        ) : (
          /* Metric Card B: 150m de capa continental */
          <div
            style={{
              position: 'absolute',
              top: 320,
              left: 60,
              right: 60,
              padding: '45px 30px',
              backgroundColor: 'rgba(11, 23, 42, 0.92)',
              border: '3.5px solid #f59e0b',
              borderRadius: 24,
              boxShadow: '0 0 35px rgba(245, 158, 11, 0.35)',
              textAlign: 'center',
            }}
          >
            <div style={{ fontSize: 82, fontWeight: 900, color: '#f59e0b', letterSpacing: 2, marginBottom: 8 }}>
              +150 m
            </div>
            <div style={{ fontSize: 24, fontWeight: 800, color: '#ffffff', letterSpacing: 1 }}>
              de capa sobre los continentes
            </div>
          </div>
        )}
      </Sequence>

      {/* BEAT 6: Coastline Beach Outro & EnigmaIQ Card (55.5s - 67.0s / 1665 - 2010 frames) */}
      <Sequence from={1665} durationInFrames={345}>
        <OffthreadVideo
          src={staticFile('mar_salado_assets/scene6_beach.mp4')}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to bottom, rgba(2,9,20,0.4) 0%, rgba(2,9,20,0.8) 100%)' }} />

        {/* Final 3 seconds EnigmaIQ Brand Screen */}
        {frame >= 1890 && (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              backgroundColor: '#020914',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 90,
            }}
          >
            <div
              style={{
                width: 130,
                height: 130,
                borderRadius: '50%',
                backgroundColor: '#f59e0b',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 0 45px rgba(245, 158, 11, 0.5)',
                marginBottom: 24,
              }}
            >
              <span style={{ fontSize: 58, fontWeight: 900, color: '#020914' }}>IQ</span>
            </div>
            <div style={{ fontSize: 44, fontWeight: 900, color: '#ffffff', letterSpacing: 4 }}>
              ENIGMAIQ
            </div>
            <div style={{ fontSize: 18, fontWeight: 700, color: '#f59e0b', letterSpacing: 2, marginTop: 8 }}>
              LA VERDAD DETRÁS DE TODO
            </div>
          </div>
        )}
      </Sequence>

      {/* ======================================================== */}
      {/* 2. TOP HEADER PILL: ENIGMAIQ                             */}
      {/* ======================================================== */}
      {frame < 1890 && (
        <div
          style={{
            position: 'absolute',
            top: 70,
            left: 55,
            zIndex: 80,
            padding: '8px 24px',
            borderRadius: 24,
            backgroundColor: '#f59e0b',
            boxShadow: '0 0 20px rgba(245, 158, 11, 0.4)',
          }}
        >
          <span style={{ fontSize: 18, fontWeight: 900, color: '#020914', letterSpacing: 2, textTransform: 'uppercase' }}>
            ENIGMAIQ
          </span>
        </div>
      )}

      {/* ======================================================== */}
      {/* 3. KINETIC SUBTITLES IN LOWER SAFE ZONE (300px Safe Zone) */}
      {/* ======================================================== */}
      {frame < 1890 && (
        <div
          style={{
            position: 'absolute',
            bottom: 310,
            left: 45,
            right: 45,
            zIndex: 85,
            textAlign: 'center',
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              fontSize: 34,
              fontWeight: 900,
              lineHeight: 1.3,
              letterSpacing: 0.5,
              textTransform: 'uppercase',
            }}
          >
            {activeSub.words.map((word, idx) => {
              const isHighlight = idx === activeWordIdx;
              return (
                <span
                  key={idx}
                  style={{
                    color: isHighlight ? '#f59e0b' : '#ffffff',
                    display: 'inline-block',
                    marginRight: 9,
                    WebkitTextStroke: '2px #000000',
                    textShadow: '0 4px 12px rgba(0,0,0,0.9)',
                    transform: isHighlight ? 'scale(1.15)' : 'scale(1)',
                    transition: 'transform 0.05s ease',
                  }}
                >
                  {word}
                </span>
              );
            })}
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* 4. MASTER AUDIO & BACKGROUND SOUNDSCAPE                  */}
      {/* ======================================================== */}
      <Audio src={staticFile('mar_salado_assets/mar_salado_voice.mp3')} volume={1.0} />
      <Audio src={staticFile('mar_salado_assets/ambient_bed.mp3')} volume={0.18} />
    </div>
  );
};