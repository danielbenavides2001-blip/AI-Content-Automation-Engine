import React from 'react';
import { Composition } from 'remotion';
import { Subtitles } from './Subtitles';
import { MapRender } from './MapRender';

import { ElPorqueDeTodoAmazonas } from './ElPorqueDeTodoAmazonas';
import { AMAZONAS_TOTAL_FRAMES, AMAZONAS_FPS } from './amazonas_timeline';

import { ElPorqueDeTodoSierraNevada } from './ElPorqueDeTodoSierraNevada';
import { SIERRA_TOTAL_FRAMES, SIERRA_FPS } from './sierra_timeline';

import { ElPorqueDeTodoOrquideas } from './ElPorqueDeTodoOrquideas';
import { ORQUIDEAS_TOTAL_FRAMES, ORQUIDEAS_FPS } from './orquideas_timeline';

import { MundoInsolitoCatatumbo } from './MundoInsolitoCatatumbo';
import { CATATUMBO_TOTAL_FRAMES, CATATUMBO_FPS } from './catatumbo_timeline';

import { ElPorqueDeTodoAjolote } from './ElPorqueDeTodoAjolote';
import { AJOLOTE_TOTAL_FRAMES, AJOLOTE_FPS } from './ajolote_timeline';

import { ElPorqueDeTodoMedusa } from './ElPorqueDeTodoMedusa';
import { MEDUSA_TOTAL_FRAMES, MEDUSA_FPS } from './medusa_timeline';

const FPS = 30;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Subtitles"
        component={Subtitles}
        durationInFrames={30000}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={{
          words: [
            { text: "EnigmaIQ", start: 0, end: 1000 },
            { text: "Inteligencia", start: 1000, end: 2000 },
            { text: "Financiera", start: 2000, end: 3000 }
          ]
        }}
        calculateMetadata={({ props }) => {
          const words = props.words as { text: string; start: number; end: number }[] | undefined;
          if (words && words.length > 0) {
            const lastWord = words[words.length - 1];
            const durationMs = (lastWord.end || 60000) + 2000;
            const durationFrames = Math.ceil((durationMs / 1000) * FPS);
            return { durationInFrames: Math.max(durationFrames, 150) };
          }
          return { durationInFrames: 30000 };
        }}
      />

      <Composition
        id="MapRender"
        component={MapRender}
        durationInFrames={240}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={{
          latitude: 4.570868,
          longitude: -74.297333,
          zoom: 5.2,
          pitch: 45,
          bearing: -10,
          highlightRegion: 'colombia',
          arrowDirection: 'none',
          floatingLabel: 'COLOMBIA'
        }}
      />

      <Composition
        id="ElPorqueDeTodoAmazonas"
        component={ElPorqueDeTodoAmazonas}
        durationInFrames={AMAZONAS_TOTAL_FRAMES}
        fps={AMAZONAS_FPS}
        width={1080}
        height={1920}
      />

      <Composition
        id="ElPorqueDeTodoSierraNevada"
        component={ElPorqueDeTodoSierraNevada}
        durationInFrames={SIERRA_TOTAL_FRAMES}
        fps={SIERRA_FPS}
        width={1080}
        height={1920}
      />

      <Composition
        id="ElPorqueDeTodoOrquideas"
        component={ElPorqueDeTodoOrquideas}
        durationInFrames={ORQUIDEAS_TOTAL_FRAMES}
        fps={ORQUIDEAS_FPS}
        width={1080}
        height={1920}
      />

      <Composition
        id="ElPorqueDeTodoCatatumbo"
        component={MundoInsolitoCatatumbo}
        durationInFrames={CATATUMBO_TOTAL_FRAMES}
        fps={CATATUMBO_FPS}
        width={1080}
        height={1920}
      />

      <Composition
        id="ElPorqueDeTodoAjolote"
        component={ElPorqueDeTodoAjolote}
        durationInFrames={AJOLOTE_TOTAL_FRAMES}
        fps={AJOLOTE_FPS}
        width={1080}
        height={1920}
      />

      <Composition
        id="ElPorqueDeTodoMedusa"
        component={ElPorqueDeTodoMedusa}
        durationInFrames={MEDUSA_TOTAL_FRAMES}
        fps={MEDUSA_FPS}
        width={1080}
        height={1920}
      />
    </>
  );
};
