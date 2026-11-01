export type VisualArchetype =
  | 'stock_footage'
  | 'country_map'
  | 'dual_country_clash'
  | 'geological_cross_section'
  | 'technical_blueprint'
  | 'telemetry_gauge'
  | 'community_poll';

export interface DynamicScene {
  sceneNumber: number;
  visualArchetype: VisualArchetype;
  startFrame: number;
  durationFrames: number;
  audioPath: string;
  narration: string;
  headline: string;
  subheadline: string;
  stockVideoPath?: string;
  stockQuery?: string;
  countryA?: string;
  countryB?: string;
  metricLabel?: string;
  metricValA?: string;
  metricValB?: string;
  metricUnit?: string;
  diagramType?: string;
  highlightRegion?: string;
  pollOptionA?: string;
  pollOptionB?: string;
}

export interface DynamicVideoBlueprint {
  title: string;
  category: string;
  pillar?: string;
  colorTheme: {
    primary: string;    // e.g. '#00f5ff' (cyan)
    secondary: string;  // e.g. '#38bdf8' (sky blue)
    accent: string;     // e.g. '#f59e0b' (amber)
    background: string; // e.g. '#040914'
  };
  fps: number;
  totalFrames: number;
  scenes: DynamicScene[];
  facebookDescription?: string;
}
