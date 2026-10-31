import React from 'react';
import {
  Audio,
  Sequence,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import { ProceduralGridCanvas } from './components_orquideas/ProceduralGridCanvas';
import { WatermarkLogo } from './components_mundo_insolito/WatermarkLogo';
import { Scene1SierraHook } from './components_sierra/Scene1SierraHook';
import { Scene2MarathonGradient } from './components_sierra/Scene2MarathonGradient';
import { Scene3IsolatedBlock } from './components_sierra/Scene3IsolatedBlock';
import { Scene4TectonicJourney } from './components_sierra/Scene4TectonicJourney';
import { Scene5SierraPoll } from './components_sierra/Scene5SierraPoll';
import { SIERRA_TIMELINE } from './sierra_timeline';

export const ElPorqueDeTodoSierraNevada: React.FC = () => {
  return (
    <div
      style={{
        flex: 1,
        backgroundColor: '#0a0d14',
        position: 'relative',
        width: 1080,
        height: 1920,
        overflow: 'hidden',
      }}
    >
      {/* 1. Procedural Background Canvas */}
      <ProceduralGridCanvas accentColor="#00f5ff" />

      {/* 2. Top-Right Brand Watermark */}
      <WatermarkLogo />

      {/* 3. Scenes Sequence */}
      {SIERRA_TIMELINE.map((beat) => {
        let SceneComponent: React.FC;
        switch (beat.scene) {
          case 'Scene1SierraHook':
            SceneComponent = Scene1SierraHook;
            break;
          case 'Scene2MarathonGradient':
            SceneComponent = Scene2MarathonGradient;
            break;
          case 'Scene3IsolatedBlock':
            SceneComponent = Scene3IsolatedBlock;
            break;
          case 'Scene4TectonicJourney':
            SceneComponent = Scene4TectonicJourney;
            break;
          case 'Scene5SierraPoll':
            SceneComponent = Scene5SierraPoll;
            break;
          default:
            SceneComponent = Scene1SierraHook;
        }

        return (
          <Sequence
            key={beat.id}
            from={beat.startFrame}
            durationInFrames={beat.durationFrames}
          >
            <SceneComponent />
            {/* Synchronized voiceover beat audio */}
            <Audio src={staticFile(beat.audioPath)} volume={1.0} />
          </Sequence>
        );
      })}

      {/* 4. Typewriter Subtitles with Phantom Text at Bottom */}
      <SubtitlesOverlay />
    </div>
  );
};

const SubtitlesOverlay: React.FC = () => {
  const frame = useCurrentFrame();

  const activeBeat = SIERRA_TIMELINE.find(
    (b) => frame >= b.startFrame && frame < b.startFrame + b.durationFrames
  );

  if (!activeBeat) return null;

  const localFrame = frame - activeBeat.startFrame;
  const audioDurationFrames = Math.round(activeBeat.audioDuration * 30);
  const text = activeBeat.text;

  const progress = Math.min(1, Math.max(0, localFrame / (audioDurationFrames * 0.95)));
  const visibleCharsCount = Math.floor(progress * text.length);

  const visibleText = text.slice(0, visibleCharsCount);
  const hiddenText = text.slice(visibleCharsCount);

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 65,
        left: 60,
        right: 60,
        zIndex: 100,
        display: 'flex',
        justifyContent: 'center',
      }}
    >
      <div
        style={{
          backgroundColor: 'rgba(11, 14, 20, 0.92)',
          border: '1.5px solid rgba(0, 245, 255, 0.45)',
          borderRadius: 16,
          padding: '18px 32px',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.6), 0 0 15px rgba(0, 245, 255, 0.2)',
          backdropFilter: 'blur(12px)',
          maxWidth: 960,
          textAlign: 'center',
          fontFamily: 'Bahnschrift, Arial, sans-serif',
          fontSize: 34,
          lineHeight: 1.3,
          fontWeight: 700,
        }}
      >
        <span style={{ color: '#ffffff' }}>{visibleText}</span>
        <span style={{ opacity: 0 }}>{hiddenText}</span>
      </div>
    </div>
  );
};
