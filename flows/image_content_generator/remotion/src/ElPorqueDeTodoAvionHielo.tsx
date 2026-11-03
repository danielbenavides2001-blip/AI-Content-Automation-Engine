import React from 'react';
import {
  Audio,
  Img,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {
  AVION_HIELO_TOTAL_FRAMES,
  AVION_HIELO_FPS,
  AVION_SUBTITLES,
} from './avion_hielo_timeline';

export { AVION_HIELO_TOTAL_FRAMES, AVION_HIELO_FPS };

export const ElPorqueDeTodoAvionHielo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const currentTimeSec = frame / fps;
  const fontFamily = "'Montserrat', 'Montserrat Black', sans-serif";

  // Subtítulo activo y palabra destacada
  const activeSub =
    AVION_SUBTITLES.find((s) => currentTimeSec >= s.start && currentTimeSec < s.end) ||
    AVION_SUBTITLES[AVION_SUBTITLES.length - 1];
  const subDuration = Math.max(0.08, activeSub.end - activeSub.start);
  const subProgress = Math.min(1, Math.max(0, (currentTimeSec - activeSub.start) / subDuration));
  const activeWordIdx = Math.min(
    activeSub.words.length - 1,
    Math.floor(subProgress * activeSub.words.length)
  );

  // Parámetros de efectos dinámicos
  // Relámpago ambiental en tormenta
  const lightningFlash =
    Math.sin(frame * 0.18) > 0.85
      ? Math.sin(frame * 1.5) * 0.4 + 0.5
      : 0;

  // Sacudida de cabina en picada mortal (Beats 1 y 4)
  const isViolentDive = (frame >= 0 && frame < 408) || (frame >= 893 && frame < 1375);
  const shakeX = isViolentDive ? Math.sin(frame * 1.2) * 8 : 0;
  const shakeY = isViolentDive ? Math.cos(frame * 1.6) * 10 : 0;

  // Altímetro digital en tiempo real: de 10.740 m a 2.500 m en Beat 1, y de 8.500 m a 0 m en Beat 4
  let currentAlt = 10740;
  if (frame < 408) {
    // 0s a 13.6s
    currentAlt = Math.round(interpolate(frame, [0, 408], [10740, 3900], { extrapolateRight: 'clamp' }));
  } else if (frame < 593) {
    // Crucero en altitud
    currentAlt = 11200;
  } else if (frame < 893) {
    // Analogía
    currentAlt = 9800;
  } else if (frame < 1375) {
    // Picada mortal de 8 km en 1 minuto
    currentAlt = Math.round(interpolate(frame, [893, 1375], [8800, 180], { extrapolateRight: 'clamp' }));
  } else {
    currentAlt = 0;
  }

  // Alarma Mayday parpadeante
  const maydayBlink = Math.sin(frame * 0.4) > 0;

  return (
    <div
      style={{
        position: 'relative',
        width: 1080,
        height: 1920,
        backgroundColor: '#020611',
        overflow: 'hidden',
        fontFamily: "'Montserrat', 'Bahnschrift', Arial, sans-serif",
      }}
    >
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap');
        @font-face {
          font-family: 'Montserrat';
          src: url('${staticFile('fonts/Montserrat-Bold.ttf')}') format('truetype');
          font-weight: 700 900;
          font-style: normal;
        }
      `}</style>

      {/* Contenedor principal con temblor de cabina */}
      <div
        style={{
          position: 'absolute',
          inset: -20,
          transform: `translate(${shakeX}px, ${shakeY}px)`,
        }}
      >
        {/* ======================================================== */}
        {/* ESCENA 1: EL GRAN HOOK - PICADA DE 8 KM (0s - 13.62s / frames 0 - 408) */}
        {/* ======================================================== */}
        {frame < 408 && (
          <div style={{ position: 'absolute', inset: 0 }}>
            {/* Fondo de tormenta con nubes oscuras */}
            <Img
              src={staticFile('avion_hielo_assets/storm_bg.jpg')}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                filter: 'brightness(0.7) contrast(1.2)',
                transform: `scale(${1.05 + (frame / 408) * 0.08})`,
              }}
            />
            {/* Resplandor de relámpago */}
            {lightningFlash > 0 && (
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  backgroundColor: `rgba(210, 235, 255, ${lightningFlash * 0.45})`,
                  pointerEvents: 'none',
                }}
              />
            )}
            {/* 3D Blender Jet en Picada vertical */}
            <div
              style={{
                position: 'absolute',
                inset: 0,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
              }}
            >
              <OffthreadVideo
                src={staticFile('avion_hielo_assets/plane_dive_loop.mp4')}
                muted={true}
                volume={0}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'contain',
                }}
              />
            </div>
            {/* Viñeta dramática de bordes oscuros */}
            <div
              style={{
                position: 'absolute',
                inset: 0,
                background:
                  'radial-gradient(ellipse at center, transparent 35%, rgba(1, 4, 12, 0.88) 100%)',
              }}
            />
          </div>
        )}

        {/* ======================================================== */}
        {/* ESCENA 2: VUELO TEXAS A BAHAMAS Y HIELO (13.62s - 19.78s / frames 408 - 593) */}
        {/* ======================================================== */}
        {frame >= 408 && frame < 593 && (
          <div style={{ position: 'absolute', inset: 0 }}>
            <Img
              src={staticFile('avion_hielo_assets/storm_bg.jpg')}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                filter: 'brightness(0.65) hue-rotate(190deg)',
              }}
            />
            {/* 3D Blender Jet volando en crucero con escarcha de hielo */}
            <div
              style={{
                position: 'absolute',
                inset: 0,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
              }}
            >
              <OffthreadVideo
                src={staticFile('avion_hielo_assets/plane_cruise_loop.mp4')}
                muted={true}
                volume={0}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'contain',
                }}
              />
            </div>
            {/* Capa de viñeta helada */}
            <div
              style={{
                position: 'absolute',
                inset: 0,
                background:
                  'linear-gradient(to bottom, rgba(5,15,30,0.65) 0%, transparent 40%, rgba(5,15,30,0.85) 100%)',
              }}
            />
          </div>
        )}

        {/* ======================================================== */}
        {/* ESCENA 3: ANALOGÍA AERODINÁMICA (19.78s - 29.78s / frames 593 - 893) */}
        {/* ======================================================== */}
        {frame >= 593 && frame < 893 && (
          <div style={{ position: 'absolute', inset: 0 }}>
            {frame < 735 ? (
              // Parte A: Mano por la ventana del carro
              <div style={{ position: 'absolute', inset: 0 }}>
                <Img
                  src={staticFile('avion_hielo_assets/hand_car.jpg')}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    filter: 'contrast(1.15) brightness(0.95)',
                    transform: `scale(${1.0 + ((frame - 593) / 142) * 0.05})`,
                  }}
                />
                <div
                  style={{
                    position: 'absolute',
                    inset: 0,
                    background:
                      'linear-gradient(to bottom, rgba(2,6,17,0.7) 0%, transparent 40%, rgba(2,6,17,0.85) 100%)',
                  }}
                />
              </div>
            ) : (
              // Parte B: 3D Blender Airfoil Stall con líneas de flujo
              <div style={{ position: 'absolute', inset: 0, backgroundColor: '#030814' }}>
                <Img
                  src={staticFile('avion_hielo_assets/storm_bg.jpg')}
                  style={{
                    position: 'absolute',
                    inset: 0,
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    filter: 'blur(8px) brightness(0.35)',
                  }}
                />
                <div
                  style={{
                    position: 'absolute',
                    inset: 0,
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                  }}
                >
                  <OffthreadVideo
                    src={staticFile('avion_hielo_assets/airfoil_stall.mp4')}
                    muted={true}
                    volume={0}
                    style={{
                      width: '100%',
                      height: '100%',
                      objectFit: 'contain',
                    }}
                  />
                </div>
              </div>
            )}
          </div>
        )}

        {/* ======================================================== */}
        {/* ESCENA 4: PICADA MORTAL Y ALARMA MAYDAY (29.78s - 45.84s / frames 893 - 1375) */}
        {/* ======================================================== */}
        {frame >= 893 && frame < 1375 && (
          <div style={{ position: 'absolute', inset: 0 }}>
            <Img
              src={staticFile('avion_hielo_assets/storm_bg.jpg')}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                filter: 'brightness(0.6) contrast(1.3) hue-rotate(330deg)',
              }}
            />
            {/* Resplandor de alarma roja en cabina */}
            {maydayBlink && (
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  backgroundColor: 'rgba(239, 68, 68, 0.28)',
                  pointerEvents: 'none',
                }}
              />
            )}
            {/* 3D Blender Jet en caída libre */}
            <div
              style={{
                position: 'absolute',
                inset: 0,
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                transform: `rotate(${Math.sin(frame * 0.2) * 5}deg)`,
              }}
            >
              <OffthreadVideo
                src={staticFile('avion_hielo_assets/plane_dive_loop.mp4')}
                muted={true}
                volume={0}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'contain',
                }}
              />
            </div>
            <div
              style={{
                position: 'absolute',
                inset: 0,
                background:
                  'radial-gradient(ellipse at center, transparent 30%, rgba(15, 2, 2, 0.9) 100%)',
              }}
            />
          </div>
        )}

        {/* ======================================================== */}
        {/* ESCENA 5: IMPACTO EN FLORIDA & CAJA NEGRA 3D (45.84s - 65.53s / frames 1375 - 1966) */}
        {/* ======================================================== */}
        {frame >= 1375 && (
          <div style={{ position: 'absolute', inset: 0 }}>
            {frame < 1680 ? (
              // Parte A: Vista aérea del impacto en Florida
              <div style={{ position: 'absolute', inset: 0 }}>
                <Img
                  src={staticFile('avion_hielo_assets/florida_crater.jpg')}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    filter: 'contrast(1.15) brightness(0.9)',
                    transform: `scale(${1.0 + ((frame - 1375) / 305) * 0.08})`,
                  }}
                />
                {/* Destello de luces policiales en la escena */}
                <div
                  style={{
                    position: 'absolute',
                    inset: 0,
                    background:
                      frame % 12 < 6
                        ? 'radial-gradient(circle at 30% 75%, rgba(59, 130, 246, 0.35) 0%, transparent 60%)'
                        : 'radial-gradient(circle at 70% 75%, rgba(239, 68, 68, 0.35) 0%, transparent 60%)',
                    pointerEvents: 'none',
                  }}
                />
                <div
                  style={{
                    position: 'absolute',
                    inset: 0,
                    background:
                      'linear-gradient(to bottom, rgba(2,6,17,0.7) 0%, transparent 45%, rgba(2,6,17,0.88) 100%)',
                  }}
                />
              </div>
            ) : (
              // Parte B: 3D Blender Flight Data Recorder (Caja Negra)
              <div style={{ position: 'absolute', inset: 0, backgroundColor: '#020611' }}>
                <Img
                  src={staticFile('avion_hielo_assets/storm_bg.jpg')}
                  style={{
                    position: 'absolute',
                    inset: 0,
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    filter: 'blur(10px) brightness(0.25)',
                  }}
                />
                <div
                  style={{
                    position: 'absolute',
                    inset: 0,
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                  }}
                >
                  <OffthreadVideo
                    src={staticFile('avion_hielo_assets/black_box_3d.mp4')}
                    muted={true}
                    volume={0}
                    style={{
                      width: '100%',
                      height: '100%',
                      objectFit: 'contain',
                    }}
                  />
                </div>
                <div
                  style={{
                    position: 'absolute',
                    inset: 0,
                    background:
                      'radial-gradient(circle at center, transparent 40%, rgba(2,6,17,0.92) 100%)',
                  }}
                />
              </div>
            )}
          </div>
        )}
      </div>

      {/* ======================================================== */}
      {/* 2. HUD OVERLAYS TÉCNICOS & INDICADORES DE VUELO           */}
      {/* ======================================================== */}

      {/* BADGE MARCA ENIGMAIQ (Top-Left) */}
      <div
        style={{
          position: 'absolute',
          top: 65,
          left: 55,
          zIndex: 80,
          padding: '8px 22px',
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

      {/* ALTÍMETRO DIGITAL HUD (Top-Right) */}
      {currentAlt > 0 && (
        <div
          style={{
            position: 'absolute',
            top: 65,
            right: 55,
            zIndex: 80,
            padding: '10px 20px',
            borderRadius: 16,
            backgroundColor: 'rgba(7, 15, 30, 0.88)',
            border: isViolentDive ? '2px solid #ef4444' : '2px solid #38bdf8',
            boxShadow: isViolentDive
              ? '0 0 25px rgba(239, 68, 68, 0.45)'
              : '0 0 20px rgba(56, 189, 248, 0.3)',
            textAlign: 'right',
          }}
        >
          <div
            style={{
              fontSize: 14,
              fontWeight: 900,
              color: isViolentDive ? '#fca5a5' : '#7dd3fc',
              letterSpacing: 1.5,
              textTransform: 'uppercase',
            }}
          >
            ALTITUD DE VUELO
          </div>
          <div
            style={{
              fontSize: 32,
              fontWeight: 900,
              color: isViolentDive ? '#ef4444' : '#ffffff',
              fontVariantNumeric: 'tabular-nums',
            }}
          >
            {currentAlt.toLocaleString('es-CO')} M
          </div>
          {isViolentDive && (
            <div
              style={{
                fontSize: 13,
                fontWeight: 900,
                color: '#f87171',
                marginTop: 2,
                letterSpacing: 1,
              }}
            >
              DESCENSO: -8.000 M/MIN
            </div>
          )}
        </div>
      )}

      {/* BANNER RECUADRO DE LA PREGUNTA (Visible en frame 0 para miniatura, 0s - 4.5s) */}
      {frame < 135 && (
        <div
          style={{
            position: 'absolute',
            top: 420,
            left: 65,
            right: 65,
            padding: '36px 22px',
            backgroundColor: 'rgba(11, 20, 38, 0.96)',
            border: '4px solid #f59e0b',
            borderRadius: 24,
            boxShadow: '0 0 40px rgba(245, 158, 11, 0.45)',
            textAlign: 'center',
            zIndex: 90,
            opacity: interpolate(frame, [115, 135], [1, 0], { extrapolateRight: 'clamp' }),
          }}
        >
          <div
            style={{
              fontSize: 48,
              fontWeight: 900,
              color: '#ffffff',
              letterSpacing: 2,
              marginBottom: 10,
              textTransform: 'uppercase',
            }}
          >
            ¿CÓMO PUEDE UN AVIÓN
          </div>
          <div
            style={{
              fontSize: 58,
              fontWeight: 900,
              color: '#f59e0b',
              letterSpacing: 3,
              textTransform: 'uppercase',
            }}
          >
            CAER 8 KM EN 1 MINUTO?
          </div>
        </div>
      )}

      {/* HUD BADGES CONTEXTUALES SEGÚN BEAT */}
      {/* Beat 2: Temperatura bajo cero y Alerta de Hielo */}
      {frame >= 408 && frame < 593 && (
        <div
          style={{
            position: 'absolute',
            top: 250,
            left: 70,
            right: 70,
            padding: '16px 24px',
            borderRadius: 20,
            backgroundColor: 'rgba(8, 20, 42, 0.92)',
            border: '2px solid #06b6d4',
            boxShadow: '0 0 30px rgba(6, 182, 212, 0.4)',
            textAlign: 'center',
            zIndex: 75,
          }}
        >
          <div style={{ fontSize: 32, fontWeight: 900, color: '#e0f2fe', letterSpacing: 2 }}>
            TEMPERATURA EXTERIOR: -47 °C
          </div>
          <div
            style={{
              fontSize: 20,
              fontWeight: 900,
              color: '#38bdf8',
              marginTop: 4,
              letterSpacing: 1.5,
              textTransform: 'uppercase',
            }}
          >
            ❄️ CONGELAMIENTO SEVERO DE ALAS
          </div>
        </div>
      )}

      {/* Beat 3B: Diagrama Aerodinámico de Sustentación */}
      {frame >= 735 && frame < 893 && (
        <div
          style={{
            position: 'absolute',
            top: 250,
            left: 70,
            right: 70,
            padding: '16px 24px',
            borderRadius: 20,
            backgroundColor: 'rgba(10, 18, 36, 0.92)',
            border: '2px solid #ef4444',
            boxShadow: '0 0 25px rgba(239, 68, 68, 0.4)',
            textAlign: 'center',
            zIndex: 75,
          }}
        >
          <div style={{ fontSize: 26, fontWeight: 900, color: '#ffffff', letterSpacing: 1.5 }}>
            PÉRDIDA DE SUSTENTACIÓN (STALL)
          </div>
          <div style={{ fontSize: 18, fontWeight: 700, color: '#f87171', marginTop: 4 }}>
            EL HIELO ROMPE EL FLUJO DE AIRE SOBRE EL ALA
          </div>
        </div>
      )}

      {/* Beat 4: ALERTA CRÍTICA MAYDAY */}
      {frame >= 893 && frame < 1375 && (
        <div
          style={{
            position: 'absolute',
            top: 230,
            left: 65,
            right: 65,
            padding: '20px 24px',
            borderRadius: 20,
            backgroundColor: maydayBlink ? 'rgba(220, 38, 38, 0.95)' : 'rgba(127, 29, 29, 0.92)',
            border: '3px solid #fca5a5',
            boxShadow: '0 0 35px rgba(239, 68, 68, 0.6)',
            textAlign: 'center',
            zIndex: 75,
          }}
        >
          <div
            style={{
              fontSize: 34,
              fontWeight: 900,
              color: '#ffffff',
              letterSpacing: 2,
              textTransform: 'uppercase',
            }}
          >
            ⚠ ALERTA: ¡MAYDAY! ¡MAYDAY!
          </div>
          <div
            style={{
              fontSize: 20,
              fontWeight: 900,
              color: '#fee2e2',
              marginTop: 4,
              letterSpacing: 1.5,
            }}
          >
            PÉRDIDA CATASTRÓFICA DE CONTROL
          </div>
        </div>
      )}

      {/* Beat 5B: Etiqueta de Caja Negra 3D */}
      {frame >= 1680 && (
        <div
          style={{
            position: 'absolute',
            top: 250,
            left: 70,
            right: 70,
            padding: '16px 24px',
            borderRadius: 20,
            backgroundColor: 'rgba(15, 23, 42, 0.92)',
            border: '2px solid #f97316',
            boxShadow: '0 0 25px rgba(249, 115, 22, 0.45)',
            textAlign: 'center',
            zIndex: 75,
          }}
        >
          <div style={{ fontSize: 26, fontWeight: 900, color: '#ffffff', letterSpacing: 2 }}>
            FLIGHT DATA RECORDER
          </div>
          <div style={{ fontSize: 18, fontWeight: 900, color: '#fb923c', marginTop: 4 }}>
            CAJA NEGRA: LA ÚNICA TESTIGO
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* 3. SUBTÍTULOS EXACTOS CON MONTSERRAT 900 & GOLD HIGHLIGHT */}
      {/* ======================================================== */}
      {frame < 1960 && (
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
      {/* 4. MASTER AUDIO: LOCUCIÓN OFICIAL FENRIR + FONDO         */}
      {/* ======================================================== */}
      <Audio src={staticFile('avion_hielo_assets/fenrir_narration.mp3')} volume={1.0} />
      <Audio src={staticFile('mar_salado_assets/ambient_bed.mp3')} volume={0.12} />
    </div>
  );
};
