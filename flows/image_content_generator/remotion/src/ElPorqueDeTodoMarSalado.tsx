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

// Duración oficial con locución Fenrir (75.0 segundos = 2250 frames @ 30 FPS)
export const MAR_SALADO_TOTAL_FRAMES = 2250;
export const MAR_SALADO_FPS = 30;

// Subtítulos sincronizados palabra por palabra con la voz de Fenrir
const SUBTITLES = [
  { start: 0.0, end: 1.12, words: ["¿POR", "QUÉ", "EL", "MAR"] },
  { start: 1.12, end: 1.8, words: ["ES", "SALADO"] },
  { start: 1.8, end: 2.62, words: ["SI", "LOS", "RÍOS"] },
  { start: 2.62, end: 3.75, words: ["QUE", "LLEGAN", "A", "ÉL"] },
  { start: 3.75, end: 5.1, words: ["SON", "DE", "AGUA", "DULCE?"] },
  { start: 5.1, end: 6.01, words: ["TODO", "EMPIEZA"] },
  { start: 6.01, end: 7.06, words: ["CON", "LA", "LLUVIA."] },
  { start: 7.06, end: 8.27, words: ["AL", "CAER,", "EL", "AGUA"] },
  { start: 8.27, end: 9.33, words: ["ATRAPA", "DIÓXIDO"] },
  { start: 9.33, end: 10.08, words: ["DE", "CARBONO"] },
  { start: 10.08, end: 11.21, words: ["DE", "LA", "ATMÓSFERA"] },
  { start: 11.21, end: 12.04, words: ["Y", "SE", "VUELVE"] },
  { start: 12.04, end: 13.4, words: ["LIGERAMENTE", "ÁCIDA."] },
  { start: 13.4, end: 14.69, words: ["ESA", "LLUVIA", "ÁCIDA"] },
  { start: 14.69, end: 16.22, words: ["DESGASTA", "LENTAMENTE"] },
  { start: 16.22, end: 18.15, words: ["LAS", "ROCAS", "CONTINENTALES,"] },
  { start: 18.15, end: 19.68, words: ["ARRANCÁNDOLES", "IONES"] },
  { start: 19.68, end: 21.37, words: ["Y", "MINERALES", "SOLUBLES,"] },
  { start: 21.37, end: 22.9, words: ["ESPECIALMENTE", "SODIO"] },
  { start: 22.9, end: 23.7, words: ["Y", "CLORURO."] },
  { start: 23.7, end: 25.04, words: ["LOS", "RÍOS", "TRANSPORTAN"] },
  { start: 25.04, end: 26.05, words: ["ESTOS", "MINERALES"] },
  { start: 26.05, end: 27.19, words: ["DE", "FORMA", "CONTINUA"] },
  { start: 27.19, end: 28.33, words: ["HACIA", "LOS", "OCÉANOS"] },
  { start: 28.33, end: 29.6, words: ["DE", "TODO", "EL", "PLANETA."] },
  { start: 29.6, end: 30.74, words: ["Y", "AQUÍ", "ESTÁ"] },
  { start: 30.74, end: 32.4, words: ["EL", "GRAN", "SECRETO:"] },
  { start: 32.4, end: 33.85, words: ["EL", "SOL", "EVAPORA"] },
  { start: 33.85, end: 35.2, words: ["EL", "AGUA", "PURA,"] },
  { start: 35.2, end: 36.34, words: ["PERO", "LA", "SAL"] },
  { start: 36.34, end: 38.1, words: ["JAMÁS", "SE", "EVAPORA."] },
  { start: 38.1, end: 39.97, words: ["SE", "QUEDA", "ACUMULADA"] },
  { start: 39.97, end: 41.53, words: ["DURANTE", "CIENTOS"] },
  { start: 41.53, end: 43.6, words: ["DE", "MILLONES", "DE", "AÑOS."] },
  { start: 43.6, end: 44.75, words: ["HOY", "CADA", "LITRO"] },
  { start: 44.75, end: 45.9, words: ["DE", "AGUA", "DE", "MAR"] },
  { start: 45.9, end: 47.54, words: ["CONTIENE", "EN", "PROMEDIO"] },
  { start: 47.54, end: 48.69, words: ["UNOS", "35", "GRAMOS"] },
  { start: 48.69, end: 50.0, words: ["DE", "SAL", "DISUELTA."] },
  { start: 50.0, end: 51.03, words: ["SI", "SACÁRAMOS"] },
  { start: 51.03, end: 51.97, words: ["TODA", "LA", "SAL"] },
  { start: 51.97, end: 52.83, words: ["DEL", "OCÉANO"] },
  { start: 52.83, end: 54.37, words: ["Y", "LA", "ESPARCIÉRAMOS"] },
  { start: 54.37, end: 55.74, words: ["SOBRE", "LA", "TIERRA,"] },
  { start: 55.74, end: 57.19, words: ["FORMARÍA", "UNA", "CAPA"] },
  { start: 57.19, end: 58.39, words: ["COLOSAL", "DE", "MÁS"] },
  { start: 58.39, end: 59.5, words: ["DE", "150", "METROS"] },
  { start: 59.5, end: 60.62, words: ["DE", "ALTO", "SOBRE"] },
  { start: 60.62, end: 62.5, words: ["TODOS", "LOS", "CONTINENTES."] },
  { start: 62.5, end: 63.58, words: ["EL", "OCÉANO", "NO", "ES"] },
  { start: 63.58, end: 65.15, words: ["SALADO", "POR", "CASUALIDAD:"] },
  { start: 65.15, end: 66.66, words: ["ES", "EL", "ARCHIVO", "QUÍMICO"] },
  { start: 66.66, end: 68.02, words: ["DE", "MILLONES", "DE", "AÑOS"] },
  { start: 68.02, end: 69.6, words: ["DE", "HISTORIA", "GEOLÓGICA."] },
  { start: 69.6, end: 71.01, words: ["ESTO", "ES", "ENIGMAIQ."] },
  { start: 71.01, end: 72.67, words: ["¿CONOCÍAS", "ESTE", "DATO?"] },
  { start: 72.67, end: 74.0, words: ["CUÉNTANOS", "EN", "LOS"] },
  { start: 74.0, end: 75.0, words: ["COMENTARIOS."] },
];

export const ElPorqueDeTodoMarSalado: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const currentTimeSec = frame / fps;
  const fontFamily = "'Montserrat', 'Montserrat Black', sans-serif";

  // Subtítulo activo y progreso de palabra
  const activeSub =
    SUBTITLES.find((s) => currentTimeSec >= s.start && currentTimeSec < s.end) ||
    SUBTITLES[SUBTITLES.length - 1];
  const subDuration = Math.max(0.1, activeSub.end - activeSub.start);
  const subProgress = Math.min(1, Math.max(0, (currentTimeSec - activeSub.start) / subDuration));
  const activeWordIdx = Math.min(
    activeSub.words.length - 1,
    Math.floor(subProgress * activeSub.words.length)
  );

  // Parámetros de animación para el diagrama de evaporación (Beat 4)
  const sunPulse = Math.sin(frame * 0.1) * 0.15 + 0.85;
  const sunRotate = (frame * 0.4) % 360;
  const vaporDrift = (frame * 2.8) % 240;

  return (
    <div
      style={{
        position: 'relative',
        width: 1080,
        height: 1920,
        backgroundColor: '#020914',
        overflow: 'hidden',
        fontFamily: "'Montserrat', 'Bahnschrift', Arial, sans-serif",
      }}
    >
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');
        @font-face {
          font-family: 'Montserrat';
          src: url('${staticFile('fonts/Montserrat-Bold.ttf')}') format('truetype');
          font-weight: 700 900;
          font-style: normal;
        }
      `}</style>
      {/* ======================================================== */}
      {/* 1. SECUENCIA VISUAL POR BEATS CON STOCK VIDEO SILENCIADO */}
      {/* ======================================================== */}

      {/* BEAT 1: HOOK DE LA PREGUNTA (0s - 5.1s / 0 - 153 frames) */}
      <Sequence from={0} durationInFrames={153}>
        <OffthreadVideo
          src={staticFile('mar_salado_assets/scene1_ocean.mp4')}
          muted={true}
          volume={0}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        {/* Viñeta cinematográfica */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              'linear-gradient(to bottom, rgba(2,9,20,0.65) 0%, rgba(2,9,20,0.2) 40%, rgba(2,9,20,0.75) 100%)',
          }}
        />

        {/* RECUADRO DE LA PREGUNTA (Exacto al video de referencia y visible en frame 0 para la miniatura) */}
        <div
          style={{
            position: 'absolute',
            top: 420,
            left: 75,
            right: 75,
            padding: '38px 24px',
            backgroundColor: 'rgba(14, 25, 48, 0.95)',
            border: '4px solid #f59e0b',
            borderRadius: 24,
            boxShadow: '0 0 35px rgba(245, 158, 11, 0.4)',
            textAlign: 'center',
            zIndex: 50,
          }}
        >
          <div
            style={{
              fontSize: 52,
              fontWeight: 900,
              color: '#ffffff',
              letterSpacing: 2,
              marginBottom: 10,
              textTransform: 'uppercase',
            }}
          >
            ¿POR QUÉ EL MAR
          </div>
          <div
            style={{
              fontSize: 62,
              fontWeight: 900,
              color: '#f59e0b',
              letterSpacing: 3,
              textTransform: 'uppercase',
            }}
          >
            ES SALADO?
          </div>
        </div>
      </Sequence>

      {/* BEAT 2: LLUVIA ÁCIDA & ATMÓSFERA (5.1s - 13.4s / 153 - 402 frames) */}
      <Sequence from={153} durationInFrames={249}>
        <OffthreadVideo
          src={staticFile('mar_salado_assets/scene2_rain.mp4')}
          muted={true}
          volume={0}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              'linear-gradient(to bottom, rgba(2,9,20,0.6) 0%, transparent 45%, rgba(2,9,20,0.8) 100%)',
          }}
        />

        <div
          style={{
            position: 'absolute',
            top: 250,
            left: 65,
            right: 65,
            padding: '16px 24px',
            borderRadius: 20,
            backgroundColor: 'rgba(11, 23, 42, 0.92)',
            border: '2px solid #38bdf8',
            boxShadow: '0 0 25px rgba(56, 189, 248, 0.35)',
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: 28, fontWeight: 900, color: '#ffffff', letterSpacing: 1.5 }}>
            LLUVIA ÁCIDA NATURAL
          </div>
          <div style={{ fontSize: 20, fontWeight: 700, color: '#38bdf8', marginTop: 4 }}>
            EL AGUA DISUELVE CO₂ DE LA ATMÓSFERA
          </div>
        </div>
      </Sequence>

      {/* BEAT 3: EROSIÓN CONTINENTAL & RÍOS (13.4s - 29.6s / 402 - 888 frames) */}
      <Sequence from={402} durationInFrames={486}>
        <OffthreadVideo
          src={staticFile('mar_salado_assets/scene3_river.mp4')}
          muted={true}
          volume={0}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              'linear-gradient(to bottom, rgba(2,9,20,0.6) 0%, transparent 50%, rgba(2,9,20,0.8) 100%)',
          }}
        />

        <div
          style={{
            position: 'absolute',
            top: 250,
            left: 65,
            right: 65,
            padding: '16px 24px',
            borderRadius: 20,
            backgroundColor: 'rgba(11, 23, 42, 0.92)',
            border: '2px solid #f59e0b',
            boxShadow: '0 0 25px rgba(245, 158, 11, 0.35)',
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: 28, fontWeight: 900, color: '#ffffff', letterSpacing: 1.5 }}>
            DESGASTE DE ROCAS
          </div>
          <div style={{ fontSize: 20, fontWeight: 700, color: '#f59e0b', marginTop: 4 }}>
            EXTRACCIÓN DE SODIO (Na⁺) Y CLORURO (Cl⁻)
          </div>
        </div>

        {/* Badges de Minerales */}
        <div
          style={{
            position: 'absolute',
            top: 400,
            left: 100,
            right: 100,
            display: 'flex',
            justifyContent: 'center',
            gap: 24,
          }}
        >
          <div
            style={{
              padding: '12px 28px',
              borderRadius: 16,
              backgroundColor: 'rgba(11, 23, 42, 0.9)',
              border: '2px solid #38bdf8',
              color: '#ffffff',
              fontSize: 22,
              fontWeight: 800,
            }}
          >
            Na⁺ <span style={{ color: '#38bdf8', fontSize: 16 }}>Sodio</span>
          </div>
          <div
            style={{
              padding: '12px 28px',
              borderRadius: 16,
              backgroundColor: 'rgba(11, 23, 42, 0.9)',
              border: '2px solid #10b981',
              color: '#ffffff',
              fontSize: 22,
              fontWeight: 800,
            }}
          >
            Cl⁻ <span style={{ color: '#10b981', fontSize: 16 }}>Cloruro</span>
          </div>
        </div>
      </Sequence>

      {/* BEAT 4: DIAGRAMA CIENTÍFICO 2D - EVAPORACIÓN SOLAR (29.6s - 43.6s / 888 - 1308 frames) */}
      <Sequence from={888} durationInFrames={420}>
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: 'radial-gradient(circle at 50% 30%, #07192f 0%, #020914 85%)',
          }}
        />

        {/* Encabezado del Secreto */}
        <div
          style={{
            position: 'absolute',
            top: 180,
            left: 65,
            right: 65,
            padding: '18px 24px',
            borderRadius: 20,
            backgroundColor: 'rgba(11, 23, 42, 0.92)',
            border: '2px solid #f59e0b',
            boxShadow: '0 0 30px rgba(245, 158, 11, 0.35)',
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: 30, fontWeight: 900, color: '#ffffff', letterSpacing: 2 }}>
            EL SECRETO: LA EVAPORACIÓN
          </div>
          <div style={{ fontSize: 18, fontWeight: 700, color: '#f59e0b', marginTop: 4 }}>
            EL AGUA PURA SE VA • LA SAL SE QUEDA
          </div>
        </div>

        {/* Sol Pulsante con Radiación */}
        <div
          style={{
            position: 'absolute',
            top: 360,
            left: '50%',
            transform: 'translateX(-50%)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <div
            style={{
              width: 140,
              height: 140,
              borderRadius: '50%',
              background: 'radial-gradient(circle, #fde047 20%, #f59e0b 70%, #d97706 100%)',
              boxShadow: `0 0 ${40 * sunPulse}px rgba(245, 158, 11, 0.8)`,
              transform: `scale(${sunPulse})`,
            }}
          />
          <div
            style={{
              fontSize: 20,
              fontWeight: 800,
              color: '#fde047',
              letterSpacing: 2,
              marginTop: 14,
            }}
          >
            RADIACIÓN TÉRMICA SOLAR
          </div>
        </div>

        {/* Flechas de Vapor Ascendente */}
        <div
          style={{
            position: 'absolute',
            top: 560,
            left: 100,
            right: 100,
            display: 'flex',
            justifyContent: 'space-around',
          }}
        >
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                transform: `translateY(-${(vaporDrift + i * 40) % 120}px)`,
                opacity: 0.85,
              }}
            >
              <span style={{ fontSize: 32, color: '#38bdf8' }}>↑</span>
              <span
                style={{
                  fontSize: 14,
                  fontWeight: 800,
                  color: '#38bdf8',
                  letterSpacing: 1,
                }}
              >
                H₂O PURA
              </span>
            </div>
          ))}
        </div>

        {/* Superficie Oceánica & Lecho Marino con Precipitación de Sal */}
        <div
          style={{
            position: 'absolute',
            bottom: 380,
            left: 55,
            right: 55,
            height: 200,
            borderRadius: 24,
            background: 'linear-gradient(to bottom, rgba(14, 165, 233, 0.3) 0%, rgba(2, 44, 84, 0.7) 100%)',
            border: '2px solid rgba(56, 189, 248, 0.4)',
            padding: 20,
            boxSizing: 'border-box',
          }}
        >
          <div style={{ fontSize: 18, fontWeight: 800, color: '#38bdf8', textAlign: 'center' }}>
            CUENCA MARINA (ACUMULACIÓN PERPETUA)
          </div>
          {/* Cristales de sal sedimentados */}
          <div
            style={{
              display: 'flex',
              justifyContent: 'center',
              gap: 16,
              marginTop: 24,
              flexWrap: 'wrap',
            }}
          >
            {['NaCl', 'SO₄', 'Mg', 'Ca', 'K'].map((ion, idx) => (
              <div
                key={idx}
                style={{
                  padding: '8px 16px',
                  borderRadius: 12,
                  backgroundColor: '#f59e0b',
                  color: '#020914',
                  fontSize: 16,
                  fontWeight: 900,
                  boxShadow: '0 0 12px rgba(245, 158, 11, 0.6)',
                }}
              >
                {ion}
              </div>
            ))}
          </div>
          <div
            style={{
              fontSize: 16,
              fontWeight: 700,
              color: '#f59e0b',
              textAlign: 'center',
              marginTop: 20,
            }}
          >
            LA SAL NO SE EVAPORA • SE CONCENTRA POR MILLONES DE AÑOS
          </div>
        </div>
      </Sequence>

      {/* BEAT 5: MÉTRICAS COLOSALES (43.6s - 62.5s / 1308 - 1875 frames) */}
      <Sequence from={1308} durationInFrames={567}>
        <OffthreadVideo
          src={staticFile('mar_salado_assets/scene5_ocean_deep.mp4')}
          muted={true}
          volume={0}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              'linear-gradient(to bottom, rgba(2,9,20,0.6) 0%, transparent 40%, rgba(2,9,20,0.85) 100%)',
          }}
        />

        {/* Tarjeta de Métrica 1: 35g de sal por litro */}
        <div
          style={{
            position: 'absolute',
            top: 260,
            left: 65,
            right: 65,
            padding: '28px 24px',
            backgroundColor: 'rgba(11, 23, 42, 0.92)',
            border: '3px solid #f59e0b',
            borderRadius: 22,
            boxShadow: '0 0 35px rgba(245, 158, 11, 0.35)',
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: 68, fontWeight: 900, color: '#f59e0b', letterSpacing: 2 }}>
            35 g
          </div>
          <div
            style={{
              fontSize: 22,
              fontWeight: 800,
              color: '#ffffff',
              letterSpacing: 1.5,
              marginTop: 6,
            }}
          >
            DE SAL POR CADA LITRO DE MAR
          </div>
        </div>

        {/* Tarjeta de Métrica 2: +150 metros de capa sobre continentes */}
        <div
          style={{
            position: 'absolute',
            top: 520,
            left: 65,
            right: 65,
            padding: '28px 24px',
            backgroundColor: 'rgba(11, 23, 42, 0.92)',
            border: '3px solid #38bdf8',
            borderRadius: 22,
            boxShadow: '0 0 35px rgba(56, 189, 248, 0.35)',
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: 68, fontWeight: 900, color: '#38bdf8', letterSpacing: 2 }}>
            +150 m
          </div>
          <div
            style={{
              fontSize: 22,
              fontWeight: 800,
              color: '#ffffff',
              letterSpacing: 1.5,
              marginTop: 6,
            }}
          >
            DE CAPA SOBRE TODOS LOS CONTINENTES
          </div>
        </div>
      </Sequence>

      {/* BEAT 6: OUTRO & COMUNIDAD ENIGMAIQ (62.5s - 75.0s / 1875 - 2250 frames) */}
      <Sequence from={1875} durationInFrames={375}>
        <OffthreadVideo
          src={staticFile('mar_salado_assets/scene6_beach.mp4')}
          muted={true}
          volume={0}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              'linear-gradient(to bottom, rgba(2,9,20,0.6) 0%, transparent 40%, rgba(2,9,20,0.85) 100%)',
          }}
        />

        <div
          style={{
            position: 'absolute',
            top: 360,
            left: 65,
            right: 65,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
          }}
        >
          {/* Logo Circular IQ */}
          <div
            style={{
              width: 130,
              height: 130,
              borderRadius: '50%',
              backgroundColor: '#f59e0b',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 0 45px rgba(245, 158, 11, 0.55)',
              marginBottom: 24,
            }}
          >
            <span style={{ fontSize: 58, fontWeight: 900, color: '#020914' }}>IQ</span>
          </div>
          <div
            style={{
              fontSize: 46,
              fontWeight: 900,
              color: '#ffffff',
              letterSpacing: 4,
              textTransform: 'uppercase',
            }}
          >
            ENIGMAIQ
          </div>
          <div
            style={{
              fontSize: 22,
              fontWeight: 800,
              color: '#f59e0b',
              letterSpacing: 2,
              marginTop: 10,
            }}
          >
            LA VERDAD DETRÁS DE TODO
          </div>
          <div
            style={{
              fontSize: 18,
              fontWeight: 700,
              color: '#e2e8f0',
              marginTop: 18,
              padding: '10px 24px',
              backgroundColor: 'rgba(11, 23, 42, 0.85)',
              borderRadius: 20,
              border: '1px solid rgba(245, 158, 11, 0.3)',
            }}
          >
            ¿CONOCÍAS ESTE DATO? COMENTA ABAJO 👇
          </div>
        </div>
      </Sequence>

      {/* ======================================================== */}
      {/* 2. PILL SUPERIOR ENIGMAIQ (Idéntico a la referencia)     */}
      {/* ======================================================== */}
      {frame < 2050 && (
        <div
          style={{
            position: 'absolute',
            top: 70,
            left: 55,
            zIndex: 80,
            padding: '8px 24px',
            borderRadius: 24,
            backgroundColor: '#f59e0b',
            boxShadow: '0 0 20px rgba(245, 158, 11, 0.45)',
          }}
        >
          <span
            style={{
              fontSize: 18,
              fontWeight: 900,
              color: '#020914',
              letterSpacing: 2,
              textTransform: 'uppercase',
            }}
          >
            ENIGMAIQ
          </span>
        </div>
      )}

      {/* ======================================================== */}
      {/* 3. SUBTÍTULOS EXACTOS AL VIDEO DE REFERENCIA (Y=1220px)  */}
      {/* ======================================================== */}
      {frame < 2050 && (
        <div
          style={{
            position: 'absolute',
            top: 1220,
            left: 50,
            right: 50,
            zIndex: 85,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              fontFamily,
              fontSize: activeSub.words.length > 3 ? 82 : 94,
              fontWeight: 900,
              lineHeight: 1.15,
              letterSpacing: '-2px',
              textTransform: 'uppercase',
              display: 'flex',
              flexWrap: 'wrap',
              justifyContent: 'center',
              alignItems: 'center',
              maxWidth: 980,
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
                    margin: '0 12px',
                    WebkitTextStroke: '10px #000000',
                    paintOrder: 'stroke fill',
                    textShadow: '0 4px 18px rgba(0,0,0,0.85)',
                    transform: isHighlight ? 'scale(1.10)' : 'scale(1)',
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
      {/* 4. MASTER AUDIO: LOCUCIÓN FENRIR + DRONE AMBIENTAL       */}
      {/* ======================================================== */}
      <Audio src={staticFile('mar_salado_assets/fenrir_mar_salado.mp3')} volume={1.0} />
      <Audio src={staticFile('mar_salado_assets/ambient_bed.mp3')} volume={0.14} />
    </div>
  );
};
