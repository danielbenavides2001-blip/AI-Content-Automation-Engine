import React from 'react';
import { Audio, Sequence, staticFile, useCurrentFrame } from 'remotion';
import { DynamicVideoBlueprint, DynamicScene } from './types';
import { ProceduralAtmosphere } from './ProceduralAtmosphere';
import { DynamicHeader } from './DynamicHeader';
import { SceneCountryMap } from './SceneCountryMap';
import { SceneDualCountryClash } from './SceneDualCountryClash';
import { SceneGeologicalCrossSection } from './SceneGeologicalCrossSection';
import { SceneTechnicalBlueprint } from './SceneTechnicalBlueprint';
import { SceneTelemetryGauge } from './SceneTelemetryGauge';
import { SceneCommunityPoll } from './SceneCommunityPoll';
import { KineticSubtitles } from './KineticSubtitles';

// High-quality default blueprint (> 60 seconds / 2000 frames)
export const DEFAULT_BLUEPRINT: DynamicVideoBlueprint = {
  title: "Colombia vs Ecuador: La Corona de las Orquídeas",
  category: "COMPARATIVA DE PAÍSES",
  colorTheme: {
    primary: "#00f5ff",
    secondary: "#38bdf8",
    accent: "#f59e0b",
    background: "#030814",
  },
  fps: 30,
  totalFrames: 2050, // 68.3 seconds (> 60s)
  scenes: [
    {
      sceneNumber: 1,
      visualArchetype: "dual_country_clash",
      startFrame: 0,
      durationFrames: 390,
      audioPath: "audio_orquideas/beat1.mp3",
      narration: "En los Andes tropicales existe una guerra silenciosa por la corona botánica del planeta entre Colombia y Ecuador.",
      headline: "CARA A CARA BOTÁNICO",
      subheadline: "COLOMBIA VS ECUADOR: ¿QUIÉN TIENE LA CORONA?",
      countryA: "colombia",
      countryB: "ecuador",
      metricLabel: "DIVERSIDAD TOTAL",
      metricValA: "4.270+",
      metricValB: "4.000+",
    },
    {
      sceneNumber: 2,
      visualArchetype: "country_map",
      startFrame: 390,
      durationFrames: 420,
      audioPath: "audio_orquideas/beat2.mp3",
      narration: "Colombia alberga más de cuatro mil doscientas especies registradas gracias a sus tres cordilleras aisladas por cañones profundos.",
      headline: "EL GIGANTE EN NÚMERO TOTAL",
      subheadline: "COLOMBIA: 4.270 ESPECIES REGISTRADAS",
      countryA: "colombia",
      metricLabel: "ESPECIES TOTALES",
      metricValA: "4.270+",
    },
    {
      sceneNumber: 3,
      visualArchetype: "country_map",
      startFrame: 810,
      durationFrames: 410,
      audioPath: "audio_orquideas/beat3.mp3",
      narration: "Pero Ecuador responde con una densidad insuperable: tiene cuatro veces más orquídeas por cada kilómetro cuadrado de territorio.",
      headline: "DENSIDAD RÉCORD",
      subheadline: "ECUADOR: 4X MÁS DENSIDAD POR KM²",
      countryA: "ecuador",
      metricLabel: "DENSIDAD / KM²",
      metricValA: "4x SUPERIOR",
    },
    {
      sceneNumber: 4,
      visualArchetype: "geological_cross_section",
      startFrame: 1220,
      durationFrames: 420,
      audioPath: "audio_orquideas/beat4.mp3",
      narration: "El secreto está en las laderas andinas donde el aire cálido del Amazonas choca contra la roca fría generando microclimas únicos.",
      headline: "EL MECANISMO ANDINO",
      subheadline: "MICROCLIMAS DE NIEBLA PERPETUA",
      metricLabel: "GRADIENTE TÉRMICO",
      metricValA: "0°C A 28°C",
    },
    {
      sceneNumber: 5,
      visualArchetype: "community_poll",
      startFrame: 1640,
      durationFrames: 410,
      audioPath: "audio_orquideas/beat5.mp3",
      narration: "¿A quién le das tú la corona mundial: a Colombia por cantidad total o a Ecuador por su densidad? Comenta tu opinión.",
      headline: "¿QUIÉN TIENE LA CORONA MUNDIAL?",
      subheadline: "DEBATE COMUNITARIO ENIGMAIQ",
      pollOptionA: "COLOMBIA (Mayor cantidad total)",
      pollOptionB: "ECUADOR (4 veces más densidad)",
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
          {scene.visualArchetype === 'country_map' && (
            <SceneCountryMap
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {scene.visualArchetype === 'dual_country_clash' && (
            <SceneDualCountryClash
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {scene.visualArchetype === 'geological_cross_section' && (
            <SceneGeologicalCrossSection
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {scene.visualArchetype === 'technical_blueprint' && (
            <SceneTechnicalBlueprint
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {scene.visualArchetype === 'telemetry_gauge' && (
            <SceneTelemetryGauge
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {scene.visualArchetype === 'community_poll' && (
            <SceneCommunityPoll
              scene={scene}
              primaryColor={blueprint.colorTheme?.primary}
              secondaryColor={blueprint.colorTheme?.secondary}
              accentColor={blueprint.colorTheme?.accent}
            />
          )}

          {/* Audio Synchronization per scene */}
          {scene.audioPath && (
            <Audio src={staticFile(scene.audioPath)} volume={1.0} />
          )}
        </Sequence>
      ))}

      {/* 4. Bottom Kinetic Subtitles Overlay (315px Safe Zone) */}
      <KineticSubtitles
        activeScene={activeScene}
        primaryColor={blueprint.colorTheme?.primary}
        secondaryColor={blueprint.colorTheme?.secondary}
      />
    </div>
  );
};
