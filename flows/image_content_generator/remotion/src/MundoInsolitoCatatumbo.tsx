import React from 'react';
import {
  Audio,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import { ProceduralLightningCanvas } from './components_mundo_insolito/ProceduralLightningCanvas';
import { WatermarkLogo } from './components_mundo_insolito/WatermarkLogo';
import { Scene1CatatumboHook } from './components_mundo_insolito/Scene1CatatumboHook';
import { Scene2HorseshoeTrap } from './components_mundo_insolito/Scene2HorseshoeTrap';
import { Scene3ThermalClashCrossSection } from './components_mundo_insolito/Scene3ThermalClashCrossSection';
import { Scene4GuinnessRecordFlashRate } from './components_mundo_insolito/Scene4GuinnessRecordFlashRate';
import { Scene5CatatumboPoll } from './components_mundo_insolito/Scene5CatatumboPoll';
import { CATATUMBO_TIMELINE } from './catatumbo_timeline';

export const MundoInsolitoCatatumbo: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        flex: 1,
        backgroundColor: '#0d0f12',
        position: 'relative',
        width: 1080,
        height: 1920,
        overflow: 'hidden',
      }}
    >
      {/* 1. Procedural Background Canvas */}
      <ProceduralLightningCanvas intensity={1.1} strikeProbability={0.12} />

      {/* 2. Top-Right Brand Watermark */}
      <WatermarkLogo />

      {/* 3. Scenes Sequence */}
      {CATATUMBO_TIMELINE.map((beat) => {
        let SceneComponent: React.FC;
        switch (beat.scene) {
          case 'Scene1CatatumboHook':
            SceneComponent = Scene1CatatumboHook;
            break;
          case 'Scene2HorseshoeTrap':
            SceneComponent = Scene2HorseshoeTrap;
            break;
          case 'Scene3ThermalClashCrossSection':
            SceneComponent = Scene3ThermalClashCrossSection;
            break;
          case 'Scene4GuinnessRecordFlashRate':
            SceneComponent = Scene4GuinnessRecordFlashRate;
            break;
          case 'Scene5CatatumboPoll':
            SceneComponent = Scene5CatatumboPoll;
            break;
          default:
            SceneComponent = Scene1CatatumboHook;
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

  // Find active beat
  const activeBeat = CATATUMBO_TIMELINE.find(
    (b) => frame >= b.startFrame && frame < b.startFrame + b.durationFrames
  );

  if (!activeBeat) return null;

  const localFrame = frame - activeBeat.startFrame;
  const audioDurationFrames = Math.round(activeBeat.audioDuration * 30);
  const text = activeBeat.text;

  // Typewriter progress
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
          backgroundColor: 'rgba(13, 16, 22, 0.88)',
          border: '1.5px solid rgba(0, 245, 255, 0.45)',
          borderRadius: 16,
          padding: '18px 32px',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.6), 0 0 15px rgba(0, 245, 255, 0.15)',
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
