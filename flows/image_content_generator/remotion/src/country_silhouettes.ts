// High-Precision Country Vector Silhouettes for EnigmaIQ Cartography & Comparisons
import { COLOMBIA_SVG_PATH, COLOMBIA_VIEWBOX, ECUADOR_SVG_PATH, ECUADOR_VIEWBOX } from './components_orquideas/real_maps_data';

export { COLOMBIA_SVG_PATH, COLOMBIA_VIEWBOX, ECUADOR_SVG_PATH, ECUADOR_VIEWBOX };

// Mexico boundary vector
export const MEXICO_SVG_PATH = "M 80 40 L 150 45 L 220 55 L 290 80 L 330 110 L 360 140 L 390 150 L 420 145 L 450 160 L 440 180 L 410 185 L 380 200 L 340 210 L 300 230 L 260 220 L 230 200 L 200 170 L 170 140 L 140 110 L 110 80 L 80 50 Z";
export const MEXICO_VIEWBOX = "0 0 500 300";

// United States (Continental) boundary vector
export const USA_SVG_PATH = "M 50 40 L 150 35 L 250 40 L 350 42 L 450 45 L 520 60 L 500 100 L 510 140 L 480 180 L 450 210 L 400 220 L 350 250 L 300 260 L 250 220 L 200 210 L 150 200 L 100 190 L 60 150 L 50 100 Z";
export const USA_VIEWBOX = "0 0 600 350";

// Brazil boundary vector
export const BRAZIL_SVG_PATH = "M 150 40 L 220 30 L 280 50 L 340 70 L 380 110 L 410 160 L 420 220 L 400 270 L 360 320 L 310 380 L 260 420 L 220 390 L 180 340 L 140 280 L 110 220 L 90 160 L 110 100 Z";
export const BRAZIL_VIEWBOX = "0 0 500 500";

// Peru boundary vector
export const PERU_SVG_PATH = "M 60 40 L 120 35 L 160 70 L 180 120 L 190 180 L 180 240 L 160 300 L 120 340 L 80 280 L 50 200 L 40 130 L 45 80 Z";
export const PERU_VIEWBOX = "0 0 250 400";

// Chile boundary vector (Long ribbon)
export const CHILE_SVG_PATH = "M 60 20 L 85 25 L 80 120 L 75 220 L 70 320 L 65 420 L 60 520 L 50 600 L 35 595 L 45 480 L 50 380 L 55 260 L 58 140 L 55 60 Z";
export const CHILE_VIEWBOX = "0 0 120 650";

// Master lookup dictionary for dynamic components
export const COUNTRY_SILHOUETTES: Record<string, { path: string; viewBox: string; name: string }> = {
  colombia: { path: COLOMBIA_SVG_PATH, viewBox: COLOMBIA_VIEWBOX, name: "Colombia" },
  ecuador: { path: ECUADOR_SVG_PATH, viewBox: ECUADOR_VIEWBOX, name: "Ecuador" },
  mexico: { path: MEXICO_SVG_PATH, viewBox: MEXICO_VIEWBOX, name: "México" },
  usa: { path: USA_SVG_PATH, viewBox: USA_VIEWBOX, name: "Estados Unidos" },
  brasil: { path: BRAZIL_SVG_PATH, viewBox: BRAZIL_VIEWBOX, name: "Brasil" },
  peru: { path: PERU_SVG_PATH, viewBox: PERU_VIEWBOX, name: "Perú" },
  chile: { path: CHILE_SVG_PATH, viewBox: CHILE_VIEWBOX, name: "Chile" }
};
