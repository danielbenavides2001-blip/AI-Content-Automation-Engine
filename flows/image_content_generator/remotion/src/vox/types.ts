export type VoxSceneKind =
  | 'media_cutout'
  | 'paper_highlight'
  | 'data_bars'
  | 'big_stat'
  | 'vox_map'
  | 'split_process';

export interface VoxBarItem {
  label: string;
  value: number;
  unit?: string;
  highlight?: boolean;
}

export interface VoxBeat {
  id: string;
  kind: VoxSceneKind;
  startFrame: number;
  durationFrames: number;
  headline: string;
  highlightPhrase?: string;
  kicker?: string;
  caption?: string;
  mediaSrc?: string;
  mediaFrames?: number;
  // data_bars
  chartTitle?: string;
  bars?: VoxBarItem[];
  // big_stat
  statValue?: string;
  statUnit?: string;
  statSub?: string;
  // vox_map
  mapCountry?: string;
  mapLabel?: string;
  mapCoords?: string;
  // split_process
  steps?: string[];
}

export interface VoxWord {
  text: string;
  startSec: number;
  endSec: number;
}

export interface VoxBlueprint {
  episodeId: string;
  title: string;
  pillarLabel: string;
  issueNumber: string;
  fps: number;
  totalFrames: number;
  beats: VoxBeat[];
  words: VoxWord[];
}
