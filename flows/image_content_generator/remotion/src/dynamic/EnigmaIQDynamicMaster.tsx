import React from 'react';
import { Audio, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from 'remotion';
import { DynamicVideoBlueprint, DynamicScene } from './types';
import { ProceduralAtmosphere } from './ProceduralAtmosphere';
import { DynamicHeader } from './DynamicHeader';
import { SceneStockFootage } from './SceneStockFootage';
import { SceneCountryMap } from './SceneCountryMap';
import { SceneDualCountryClash } from './SceneDualCountryClash';
import { SceneGeologicalCrossSection } from './SceneGeologicalCrossSection';
import { SceneTechnicalBlueprint } from './SceneTechnicalBlueprint';
import { SceneTelemetryGauge } from './SceneTelemetryGauge';
import { SceneCommunityPoll } from './SceneCommunityPoll';
import { KineticSubtitles } from './KineticSubtitles';

// High-quality default blueprint (> 60 seconds / 2050 frames)
export const DEFAULT_BLUEPRINT: DynamicVideoBlueprint = {
  title: "¿Por qué el mar es salado si los ríos son dulces?",
  category: "FENÓMENOS OCEÁNICOS",
  colorTheme: {
    primary: "#00f5ff",
    secondary: "#38bdf8",
    accent: "#f59e0b",
    background: "#030814",
  },
  fps: 30,
  totalFrames: 2010, // 67.0 seconds (> 60s)
  scenes: [
    {
      sceneNumber: 1,
      visualArchetype: "stock_footage",
      startFrame: 0,
      durationFrames: 240,
      audioPath: "mar_salado_assets/mar_salado_voice.mp3",
      stockVideoPath: "mar_salado_assets/scene1_ocean.mp4",
      narration: "¿Por qué el mar es salado si los ríos que llegan a él son de agua dulce?",
      headline: "¿POR QUÉ EL MAR",
      subheadline: "ES SALADO?",
    },
    {
      sceneNumber: 2,
      visualArchetype: "stock_footage",
      startFrame: 240,
      durationFrames: 420,
      audioPath: "mar_salado_assets/mar_salado_voice.mp3",
      stockVideoPath: "mar_salado_assets/scene2_rain.mp4",
      narration: "Todo empieza con la lluvia. Al caer, el agua atrapa dióxido de carbono y se vuelve ácida.",
      headline: "LA LLUVIA ÁCIDA NATURAL",
      subheadline: "MINERALES ARRANCADOS DE LAS ROCAS",
    },
    {
      sceneNumber: 3,
      visualArchetype: "stock_footage",
      startFrame: 660,
      durationFrames: 450,
      audioPath: "mar_salado_assets/mar_salado_voice.mp3",
      stockVideoPath: "mar_salado_assets/scene3_river.mp4",
      narration: "Esa lluvia desgasta las rocas continentales y les arranca minerales como el sodio y el cloruro.",
      headline: "TRANSPORTE CONTINENTAL",
      subheadline: "SODIO Y CLORURO VIAJAN AL MAR",
    },
    {
      sceneNumber: 4,
      visualArchetype: "stock_footage",
      startFrame: 1110,
      durationFrames: 450,
      audioPath: "mar_salado_assets/mar_salado_voice.mp3",
      stockVideoPath: "mar_salado_assets/scene5_ocean_deep.mp4",
      narration: "Y aquí está el secreto: el sol evapora el agua pura, pero la sal no se evapora, se queda acumulada.",
      headline: "CONCENTRACIÓN MILENARIA",
      subheadline: "35 GRAMOS POR CADA LITRO",
      metricLabel: "DENSIDAD DE SAL",
      metricValA: "35 g / L",
    },
    {
      sceneNumber: 5,
      visualArchetype: "community_poll",
      startFrame: 1560,
      durationFrames: 450,
      audioPath: "mar_salado_assets/mar_salado_voice.mp3",
      stockVideoPath: "mar_salado_assets/scene6_beach.mp4",
      narration: "El océano no es salado por casualidad: guarda millones de años de historia. ¿Conocías este dato?",
      headline: "¿SABÍAS ESTE DATO?",
      subheadline: "DEBATE COMUNITARIO ENIGMAIQ",
      pollOptionA: "SÍ, YA LO SABÍA",
      pollOptionB: "NO, ME ACABO DE ENTERAR",
    },
  ],
};

export const EnigmaIQDynamicMaster: React.FC<Partial<DynamicVideoBlueprint>> = (props) => {
  const frame = useCurrentFrame();
  const blueprint: DynamicVideoBlueprint = {
    ...DEFAULT_BLUEPRINT,
    ...props,
    scenes: props.scenes || DEFAULT_BLUEPRINT.scenes,
  };

  // Find currently active scene
  const activeScene: DynamicScene =
    blueprint.scenes.find(
      (s) => frame >= s.startFrame && frame < s.startFrame + s.durationFrames
    ) || blueprint.scenes[blueprint.scenes.length - 1];

  return (
    <div
      style={{
        position: 'relative',
        width: 1080,
        height: 1920,
        backgroundColor: blueprint.colorTheme?.background || '#030814',
        overflow: 'hidden',
      }}
    >
      {/* 1. Procedural Background Atmosphere */}
      <ProceduralAtmosphere
        primaryColor={blueprint.colorTheme?.primary}
        secondaryColor={blueprint.colorTheme?.secondary}
        backgroundColor={blueprint.colorTheme?.background}
      />

      {/* 2. Top EnigmaIQ Branding Header */}
      <DynamicHeader
        category={blueprint.category}
        primaryColor={blueprint.colorTheme?.primary}
        secondaryColor={blueprint.colorTheme?.secondary}
      />

      {/* 3. Sequential Scene Renderers */}
      {blueprint.scenes.map((scene, idx) => (
        <Sequence
          key={`scene-${idx}`}
          from={scene.startFrame}
          durationInFrames={scene.durationFrames}
        >
          {/* Real Stock Footage Background (when available on ANY archetype) */}
          {scene.stockVideoPath && scene.visualArchetype !== 'stock_footage' && (
            <div style={{ position: 'absolute', inset: 0, overflow: 'hidden' }}>
              <OffthreadVideo
                src={staticFile(scene.stockVideoPath)}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                }}
              />
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  background:
                    'linear-gradient(to bottom, rgba(2,9,20,0.7) 0%, rgba(2,9,20,0.3) 40%, rgba(2,9,20,0.8) 100%)',
                }}
              />
            </div>
          )}

          {/* Archetype 0: Pure Stock Footage */}
          {scene.visualArchetype === 'stock_footage' && (
            <SceneStockFootage
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {/* Archetype 1: Single Country Map */}
          {scene.visualArchetype === 'country_map' && (
            <SceneCountryMap
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {/* Archetype 2: Dual Country Clash */}
          {scene.visualArchetype === 'dual_country_clash' && (
            <SceneDualCountryClash
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {/* Archetype 3: Geological Cross Section */}
          {scene.visualArchetype === 'geological_cross_section' && (
            <SceneGeologicalCrossSection
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {/* Archetype 4: Technical Blueprint */}
          {scene.visualArchetype === 'technical_blueprint' && (
            <SceneTechnicalBlueprint
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {/* Archetype 5: Telemetry Gauge */}
          {scene.visualArchetype === 'telemetry_gauge' && (
            <SceneTelemetryGauge
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {/* Archetype 6: Community Poll / Debate */}
          {scene.visualArchetype === 'community_poll' && (
            <SceneCommunityPoll
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {/* Scene Audio Synchronization */}
          {scene.audioPath && (
            <Audio src={staticFile(scene.audioPath)} volume={1.0} />
          )}
        </Sequence>
      ))}

      {/* 4. Ambient Soundscape Drone Bed */}
      <Audio src={staticFile('mar_salado_assets/ambient_bed.mp3')} volume={0.15} />

      {/* 5. Bottom Kinetic Subtitles Overlay (315px Safe Zone) */}
      <KineticSubtitles
        activeScene={activeScene}
        primaryColor={blueprint.colorTheme?.primary}
        secondaryColor={blueprint.colorTheme?.secondary}
      />
    </div>
  );
};
