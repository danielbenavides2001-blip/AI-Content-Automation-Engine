import React from 'react';
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { VoxBeat } from './types';
import geodataRaw from '../real_country_geodata.json';

interface GeoEntry {
  name: string;
  capital: string;
  coords: string;
  path: string;
  viewBox: string;
}
const GEODATA = geodataRaw as Record<string, GeoEntry>;

const MediaFrame: React.FC<{ src?: string; framesCount?: number; height: number; width?: number }> = ({
  src,
  framesCount = 0,
  height,
  width = 920,
}) => {
  const frame = useCurrentFrame();
  if (!src) return null;

  let resolved = src;
  if (framesCount > 0) {
    const idx = (frame % framesCount) + 1;
    const padded = String(idx).padStart(4, '0');
    resolved = staticFile(`${src}/f_${padded}.jpg`);
  } else if (!src.startsWith('http')) {
    resolved = staticFile(src);
  }
  const driftScale = 1.0 + (frame % 240) * 0.00028;

  return (
    <div
      style={{
        width,
        height,
        overflow: 'hidden',
        position: 'relative',
        backgroundColor: '#1E1E1E',
        border: '4px solid #141414',
      }}
    >
      <div style={{ width: '100%', height: '100%', transform: `scale(${driftScale})` }}>
        <Img
          src={resolved}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </div>
      {/* Subtle printed halftone film overlay */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'linear-gradient(180deg, rgba(244,239,230,0.03) 0%, rgba(18,18,18,0.14) 100%)',
          pointerEvents: 'none',
        }}
      />
    </div>
  );
};

const MaskingTape: React.FC<{ left?: number; right?: number; top?: number; rotate?: number }> = ({
  left,
  right,
  top = -18,
  rotate = -6,
}) => (
  <div
    style={{
      position: 'absolute',
      top,
      left,
      right,
      width: 120,
      height: 36,
      backgroundColor: 'rgba(255, 232, 163, 0.86)',
      border: '1.5px solid rgba(160, 130, 70, 0.45)',
      transform: `rotate(${rotate}deg)`,
      boxShadow: '2px 3px 0px rgba(20,20,20,0.16)',
      zIndex: 15,
    }}
  />
);

const HandCircleRed: React.FC<{ width: number; height: number; progress: number }> = ({
  width,
  height,
  progress,
}) => {
  const frame = useCurrentFrame();
  // 10fps boiling jitter effect (every 3 frames at 30fps)
  const boilStep = Math.floor(frame / 3);
  const dx = ((boilStep * 7) % 3) - 1;
  const dy = ((boilStep * 13) % 3) - 1;
  const perim = 2 * (width + height);

  return (
    <svg
      width={width + 26}
      height={height + 26}
      viewBox={`-13 -13 ${width + 26} ${height + 26}`}
      style={{
        position: 'absolute',
        left: '50%',
        top: '50%',
        transform: `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`,
        pointerEvents: 'none',
        overflow: 'visible',
      }}
    >
      <path
        d={`M ${width * 0.12} ${height * 0.08} C ${width * 0.55} -6, ${width + 6} ${height * 0.06}, ${width} ${height * 0.52} C ${width + 4} ${height * 0.96}, ${width * 0.45} ${height + 8}, ${width * 0.08} ${height * 0.92} C -6 ${height * 0.65}, -4 ${height * 0.12}, ${width * 0.18} ${height * 0.06}`}
        fill="none"
        stroke="#E63946"
        strokeWidth={6.5}
        strokeLinecap="round"
        strokeDasharray={perim}
        strokeDashoffset={perim * (1 - Math.min(1, Math.max(0, progress)))}
      />
    </svg>
  );
};

export const VoxSceneView: React.FC<{ beat: VoxBeat; isFirstScene: boolean }> = ({
  beat,
  isFirstScene,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  // Inside <Sequence from={beat.startFrame}>, Remotion resets frame to 0
  const localFrame = frame;
  const progress = Math.min(1, localFrame / Math.max(1, beat.durationFrames));

  const slap = isFirstScene && localFrame < 3
    ? 1
    : spring({ frame: localFrame, fps, config: { damping: 14, stiffness: 210, mass: 0.65 } });
  const cardScale = 0.94 + 0.06 * slap;
  const cardY = isFirstScene && localFrame < 3 ? 0 : (1 - slap) * 28;
  const boilIdx = Math.floor(frame / 3) % 2;

  // Render highlighted phrase inside headline
  const renderHighlightedHeadline = (text: string, phrase?: string, highlightRatio = 1) => {
    if (!phrase) return <span>{text}</span>;
    const idx = text.toLowerCase().indexOf(phrase.toLowerCase());
    if (idx === -1) return <span>{text}</span>;
    const before = text.slice(0, idx);
    const match = text.slice(idx, idx + phrase.length);
    const after = text.slice(idx + phrase.length);

    return (
      <>
        {before}
        <span style={{ position: 'relative', display: 'inline-block', padding: '0 8px' }}>
          <span
            style={{
              position: 'absolute',
              left: 0,
              top: 4,
              bottom: 2,
              width: `${Math.min(100, Math.max(0, highlightRatio * 100))}%`,
              backgroundColor: '#FFE14D',
              zIndex: 0,
            }}
          />
          <span style={{ position: 'relative', zIndex: 1 }}>{match}</span>
        </span>
        {after}
      </>
    );
  };

  if (beat.kind === 'media_cutout') {
    const tilt = beat.id.charCodeAt(beat.id.length - 1) % 2 === 0 ? -1.1 : 1.1;
    return (
      <div
        style={{
          position: 'absolute',
          top: 158,
          left: 58,
          right: 58,
          display: 'flex',
          flexDirection: 'column',
          gap: 28,
          transform: `translateY(${cardY}px) scale(${cardScale})`,
        }}
      >
        {/* Editorial headline strip */}
        <div
          style={{
            backgroundColor: '#FFFDF8',
            border: '4px solid #141414',
            boxShadow: '9px 9px 0px #141414',
            padding: '22px 26px',
          }}
        >
          <div
            style={{
              display: 'inline-block',
              backgroundColor: '#E63946',
              color: '#FFFFFF',
              fontFamily: "'Courier New', monospace",
              fontWeight: 700,
              fontSize: 20,
              padding: '4px 12px',
              marginBottom: 12,
              letterSpacing: 1.1,
            }}
          >
            {(beat.kicker || 'ARCHIVO VISUAL').toUpperCase()}
          </div>
          <div
            style={{
              fontFamily: "'VoxSans', 'Montserrat', Arial, sans-serif",
              fontWeight: 900,
              fontSize: 44,
              lineHeight: 1.14,
              color: '#141414',
            }}
          >
            {renderHighlightedHeadline(
              beat.headline,
              beat.highlightPhrase,
              interpolate(localFrame, [4, 24], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
            )}
          </div>
        </div>

        {/* Taped moving paper cutout frame */}
        <div
          style={{
            position: 'relative',
            backgroundColor: '#FFFDF8',
            padding: 18,
            border: '4px solid #141414',
            boxShadow: '14px 14px 0px #141414',
            transform: `rotate(${tilt}deg)`,
          }}
        >
          <MaskingTape left={60} top={-20} rotate={-7} />
          <MaskingTape right={60} top={-20} rotate={8} />
          <MediaFrame src={beat.mediaSrc} framesCount={beat.mediaFrames} width={920} height={910} />
          {beat.caption && (
            <div
              style={{
                marginTop: 14,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                fontFamily: "'Courier New', monospace",
                fontWeight: 700,
                fontSize: 21,
                color: '#2B2B2B',
              }}
            >
              <span>▶ {beat.caption}</span>
              <span style={{ color: '#E63946' }}>[EN VIVO]</span>
            </div>
          )}
        </div>
      </div>
    );
  }

  if (beat.kind === 'paper_highlight') {
    const sweep = interpolate(localFrame, [2, 26], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    return (
      <div
        style={{
          position: 'absolute',
          top: 162,
          left: 58,
          right: 58,
          display: 'flex',
          flexDirection: 'column',
          gap: 28,
          transform: `translateY(${cardY}px) scale(${cardScale})`,
        }}
      >
        {/* Newspaper article cutout card */}
        <div
          style={{
            position: 'relative',
            backgroundColor: '#FFFDF7',
            border: '4px solid #141414',
            boxShadow: '12px 12px 0px #141414',
            padding: '28px 32px 32px',
          }}
        >
          <MaskingTape left={390} top={-20} rotate={boilIdx === 0 ? -2 : 1.5} />
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              borderBottom: '2px solid rgba(20,20,20,0.2)',
              paddingBottom: 10,
              marginBottom: 18,
              fontFamily: "'Courier New', monospace",
              fontSize: 19,
              fontWeight: 700,
              color: '#555',
            }}
          >
            <span>REPORTE // {(beat.kicker || 'EVIDENCIA').toUpperCase()}</span>
            <span style={{ color: '#E63946' }}>SUBRAYADO CLAVE</span>
          </div>
          {/* Faux blurred news lines above */}
          <div style={{ display: 'flex', gap: 12, marginBottom: 16, opacity: 0.22 }}>
            <div style={{ height: 10, width: '42%', backgroundColor: '#141414' }} />
            <div style={{ height: 10, width: '52%', backgroundColor: '#141414' }} />
          </div>

          <div
            style={{
              fontFamily: "Georgia, 'Times New Roman', serif",
              fontWeight: 700,
              fontSize: 50,
              lineHeight: 1.24,
              color: '#141414',
            }}
          >
            {renderHighlightedHeadline(beat.headline, beat.highlightPhrase || beat.headline.split(' ').slice(0, 4).join(' '), sweep)}
          </div>

          {/* Faux news lines below */}
          <div style={{ display: 'flex', gap: 14, marginTop: 22, opacity: 0.2 }}>
            <div style={{ height: 10, width: '34%', backgroundColor: '#141414' }} />
            <div style={{ height: 10, width: '28%', backgroundColor: '#141414' }} />
            <div style={{ height: 10, width: '30%', backgroundColor: '#141414' }} />
          </div>
        </div>

        {/* Dynamic accompanying B-roll below */}
        <div
          style={{
            position: 'relative',
            backgroundColor: '#FFFDF8',
            padding: 14,
            border: '4px solid #141414',
            boxShadow: '10px 10px 0px #E63946',
            transform: 'rotate(0.8deg)',
          }}
        >
          <MediaFrame src={beat.mediaSrc} framesCount={beat.mediaFrames} width={928} height={640} />
        </div>
      </div>
    );
  }

  if (beat.kind === 'data_bars') {
    const bars = beat.bars && beat.bars.length ? beat.bars : [
      { label: 'Estándar', value: 25, unit: '%', highlight: false },
      { label: 'Extremo', value: 92, unit: '%', highlight: true },
    ];
    const maxVal = Math.max(...bars.map((b) => b.value), 1);

    return (
      <div
        style={{
          position: 'absolute',
          top: 158,
          left: 58,
          right: 58,
          display: 'flex',
          flexDirection: 'column',
          gap: 24,
          transform: `translateY(${cardY}px) scale(${cardScale})`,
        }}
      >
        <div
          style={{
            backgroundColor: '#FFFDF8',
            border: '4px solid #141414',
            boxShadow: '12px 12px 0px #141414',
            padding: '28px 32px',
          }}
        >
          <div
            style={{
              fontFamily: "'Courier New', monospace",
              fontSize: 20,
              fontWeight: 700,
              color: '#E63946',
              marginBottom: 8,
            }}
          >
            GRÁFICA COMPARATIVA // {(beat.kicker || 'DATOS').toUpperCase()}
          </div>
          <div
            style={{
              fontFamily: "'VoxSans', 'Montserrat', Arial, sans-serif",
              fontWeight: 900,
              fontSize: 40,
              lineHeight: 1.15,
              color: '#141414',
              marginBottom: 28,
            }}
          >
            {beat.chartTitle || beat.headline}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 22 }}>
            {bars.map((bar, bi) => {
              const barGrow = interpolate(localFrame, [4 + bi * 5, 22 + bi * 5], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              const pct = Math.max(8, (bar.value / maxVal) * 100 * barGrow);
              const valNow = Math.round(bar.value * barGrow);
              return (
                <div key={bar.label} style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                    <span
                      style={{
                        fontFamily: "'VoxSans', 'Montserrat', Arial, sans-serif",
                        fontWeight: 900,
                        fontSize: 26,
                        color: '#141414',
                      }}
                    >
                      {bar.label}
                    </span>
                    <span
                      style={{
                        fontFamily: "'Courier New', monospace",
                        fontWeight: 900,
                        fontSize: 28,
                        color: bar.highlight ? '#E63946' : '#141414',
                      }}
                    >
                      {valNow}{bar.unit || ''}
                    </span>
                  </div>
                  <div
                    style={{
                      width: '100%',
                      height: 44,
                      backgroundColor: '#EBE3D3',
                      border: '3px solid #141414',
                      position: 'relative',
                    }}
                  >
                    <div
                      style={{
                        width: `${pct}%`,
                        height: '100%',
                        backgroundColor: bar.highlight ? '#E63946' : '#1D4ED8',
                        borderRight: '3px solid #141414',
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Supporting real video clip */}
        <div
          style={{
            position: 'relative',
            backgroundColor: '#FFFDF8',
            padding: 14,
            border: '4px solid #141414',
            boxShadow: '10px 10px 0px #141414',
          }}
        >
          <MediaFrame src={beat.mediaSrc} framesCount={beat.mediaFrames} width={928} height={540} />
        </div>
      </div>
    );
  }

  if (beat.kind === 'big_stat') {
    const circleProg = interpolate(localFrame, [4, 24], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    return (
      <div
        style={{
          position: 'absolute',
          top: 158,
          left: 58,
          right: 58,
          display: 'flex',
          flexDirection: 'column',
          gap: 26,
          transform: `translateY(${cardY}px) scale(${cardScale})`,
        }}
      >
        <div
          style={{
            backgroundColor: '#FFFDF8',
            border: '4px solid #141414',
            boxShadow: '12px 12px 0px #141414',
            padding: '28px 32px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
          }}
        >
          <div
            style={{
              backgroundColor: '#FFE14D',
              border: '2.5px solid #141414',
              padding: '5px 16px',
              fontFamily: "'Courier New', monospace",
              fontWeight: 700,
              fontSize: 20,
              marginBottom: 18,
            }}
          >
            {(beat.kicker || 'CIFRA CLAVE').toUpperCase()}
          </div>

          <div style={{ position: 'relative', display: 'inline-block', padding: '14px 36px', marginBottom: 14 }}>
            <HandCircleRed width={440} height={150} progress={circleProg} />
            <div
              style={{
                fontFamily: "'VoxSans', 'Montserrat', Arial, sans-serif",
                fontWeight: 900,
                fontSize: 108,
                lineHeight: 1,
                color: '#141414',
              }}
            >
              {beat.statValue || '100%'}
              {beat.statUnit ? (
                <span style={{ fontSize: 44, marginLeft: 8, color: '#E63946' }}>{beat.statUnit}</span>
              ) : null}
            </div>
          </div>

          <div
            style={{
              fontFamily: "'VoxSans', 'Montserrat', Arial, sans-serif",
              fontWeight: 900,
              fontSize: 36,
              lineHeight: 1.18,
              color: '#141414',
            }}
          >
            {beat.statSub || beat.headline}
          </div>
        </div>

        <div
          style={{
            position: 'relative',
            backgroundColor: '#FFFDF8',
            padding: 14,
            border: '4px solid #141414',
            boxShadow: '10px 10px 0px #141414',
            transform: 'rotate(-0.8deg)',
          }}
        >
          <MaskingTape left={60} top={-18} rotate={-5} />
          <MediaFrame src={beat.mediaSrc} framesCount={beat.mediaFrames} width={928} height={680} />
        </div>
      </div>
    );
  }

  if (beat.kind === 'vox_map') {
    const key = (beat.mapCountry || 'colombia').toLowerCase();
    const geo = GEODATA[key] || GEODATA.colombia;
    const zoom = interpolate(progress, [0, 1], [1.0, 1.14]);
    const strokeProg = interpolate(localFrame, [2, 28], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });

    return (
      <div
        style={{
          position: 'absolute',
          top: 158,
          left: 58,
          right: 58,
          display: 'flex',
          flexDirection: 'column',
          gap: 24,
          transform: `translateY(${cardY}px) scale(${cardScale})`,
        }}
      >
        <div
          style={{
            backgroundColor: '#EDE4D3',
            border: '4px solid #141414',
            boxShadow: '12px 12px 0px #141414',
            padding: 24,
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <span
              style={{
                backgroundColor: '#E63946',
                color: '#FFFFFF',
                padding: '5px 14px',
                fontFamily: "'Courier New', monospace",
                fontWeight: 700,
                fontSize: 20,
              }}
            >
              UBICACIÓN // {(beat.mapLabel || geo.name).toUpperCase()}
            </span>
            <span style={{ fontFamily: "'Courier New', monospace", fontSize: 19, fontWeight: 700, color: '#141414' }}>
              {beat.mapCoords || geo.coords}
            </span>
          </div>

          <div
            style={{
              height: 620,
              backgroundColor: '#E6DCC8',
              border: '3px solid #141414',
              position: 'relative',
              overflow: 'hidden',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
            }}
          >
            {/* Cartographic latitude/longitude lines */}
            <svg width="100%" height="100%" style={{ position: 'absolute', inset: 0, opacity: 0.35 }}>
              {[120, 240, 360, 480].map((y) => (
                <line key={y} x1="0" y1={y} x2="920" y2={y} stroke="#141414" strokeDasharray="6 8" />
              ))}
              {[180, 360, 540, 720].map((x) => (
                <line key={x} x1={x} y1="0" x2={x} y2="620" stroke="#141414" strokeDasharray="6 8" />
              ))}
            </svg>

            <svg
              viewBox={geo.viewBox || '0 0 700 700'}
              width={560}
              height={560}
              style={{ transform: `scale(${zoom})`, position: 'relative', zIndex: 2 }}
            >
              <path
                d={geo.path}
                fill="#FFE14D"
                fillOpacity={0.88}
                stroke="#E63946"
                strokeWidth={9}
                strokeLinejoin="round"
                strokeDasharray={3200}
                strokeDashoffset={3200 * (1 - strokeProg)}
              />
              {/* Animated locator pin */}
              <circle cx={350} cy={350} r={14 + boilIdx * 4} fill="#E63946" stroke="#141414" strokeWidth={5} />
            </svg>
          </div>

          <div
            style={{
              marginTop: 14,
              fontFamily: "'VoxSans', 'Montserrat', Arial, sans-serif",
              fontWeight: 900,
              fontSize: 34,
              color: '#141414',
            }}
          >
            {beat.headline}
          </div>
        </div>

        <div
          style={{
            backgroundColor: '#FFFDF8',
            padding: 12,
            border: '4px solid #141414',
            boxShadow: '9px 9px 0px #141414',
          }}
        >
          <MediaFrame src={beat.mediaSrc} framesCount={beat.mediaFrames} width={932} height={470} />
        </div>
      </div>
    );
  }

  // split_process: step-by-step index cards + video
  const steps = beat.steps && beat.steps.length ? beat.steps : [beat.headline];
  return (
    <div
      style={{
        position: 'absolute',
        top: 158,
        left: 58,
        right: 58,
        display: 'flex',
        flexDirection: 'column',
        gap: 22,
        transform: `translateY(${cardY}px) scale(${cardScale})`,
      }}
    >
      <div
        style={{
          backgroundColor: '#FFFDF8',
          border: '4px solid #141414',
          boxShadow: '10px 10px 0px #141414',
          padding: '22px 26px',
        }}
      >
        <div
          style={{
            fontFamily: "'Courier New', monospace",
            fontSize: 20,
            fontWeight: 700,
            color: '#E63946',
            marginBottom: 8,
          }}
        >
          SECUENCIA // {(beat.kicker || 'MECÁNICA').toUpperCase()}
        </div>
        <div
          style={{
            fontFamily: "'VoxSans', 'Montserrat', Arial, sans-serif",
            fontWeight: 900,
            fontSize: 38,
            color: '#141414',
            marginBottom: 18,
          }}
        >
          {beat.headline}
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          {steps.slice(0, 3).map((st, si) => {
            const visible = si === 0 || localFrame >= si * 10;
            return (
              <div
                key={si}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 16,
                  backgroundColor: visible ? '#FFE14D' : '#EBE3D3',
                  border: '3px solid #141414',
                  padding: '12px 18px',
                  opacity: visible ? 1 : 0.45,
                }}
              >
                <div
                  style={{
                    backgroundColor: '#141414',
                    color: '#FFFFFF',
                    fontFamily: "'Courier New', monospace",
                    fontWeight: 900,
                    fontSize: 24,
                    width: 40,
                    height: 40,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                  }}
                >
                  {si + 1}
                </div>
                <span
                  style={{
                    fontFamily: "'VoxSans', 'Montserrat', Arial, sans-serif",
                    fontWeight: 900,
                    fontSize: 26,
                    color: '#141414',
                  }}
                >
                  {st}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      <div
        style={{
          backgroundColor: '#FFFDF8',
          padding: 14,
          border: '4px solid #141414',
          boxShadow: '10px 10px 0px #141414',
        }}
      >
        <MediaFrame src={beat.mediaSrc} framesCount={beat.mediaFrames} width={928} height={580} />
      </div>
    </div>
  );
};
