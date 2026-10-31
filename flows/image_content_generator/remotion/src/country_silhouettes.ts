// Exact High-Precision Vector Silhouettes for EnigmaIQ Cartography & Country Comparisons
import { COLOMBIA_SVG_PATH, COLOMBIA_VIEWBOX, ECUADOR_SVG_PATH, ECUADOR_VIEWBOX } from './components_orquideas/real_maps_data';

export { COLOMBIA_SVG_PATH, COLOMBIA_VIEWBOX, ECUADOR_SVG_PATH, ECUADOR_VIEWBOX };

export const MEXICO_SVG_PATH = "M 80 40 L 150 45 L 220 55 L 290 80 L 330 110 L 360 140 L 390 150 L 420 145 L 450 160 L 440 180 L 410 185 L 380 200 L 340 210 L 300 230 L 260 220 L 230 200 L 200 170 L 170 140 L 140 110 L 110 80 L 80 50 Z";
export const MEXICO_VIEWBOX = "0 0 500 300";

export const USA_SVG_PATH = "M 50 40 L 150 35 L 250 40 L 350 42 L 450 45 L 520 60 L 500 100 L 510 140 L 480 180 L 450 210 L 400 220 L 350 250 L 300 260 L 250 220 L 200 210 L 150 200 L 100 190 L 60 150 L 50 100 Z";
export const USA_VIEWBOX = "0 0 600 350";

export const BRAZIL_SVG_PATH = "M 150 40 L 220 30 L 280 50 L 340 70 L 380 110 L 410 160 L 420 220 L 400 270 L 360 320 L 310 380 L 260 420 L 220 390 L 180 340 L 140 280 L 110 220 L 90 160 L 110 100 Z";
export const BRAZIL_VIEWBOX = "0 0 500 500";

export const PERU_SVG_PATH = "M 60 40 L 120 35 L 160 70 L 180 120 L 190 180 L 180 240 L 160 300 L 120 340 L 80 280 L 50 200 L 40 130 L 45 80 Z";
export const PERU_VIEWBOX = "0 0 250 400";

export const CHILE_SVG_PATH = "M 60 20 L 85 25 L 80 120 L 75 220 L 70 320 L 65 420 L 60 520 L 50 600 L 35 595 L 45 480 L 50 380 L 55 260 L 58 140 L 55 60 Z";
export const CHILE_VIEWBOX = "0 0 120 650";

export const ARGENTINA_SVG_PATH = "M 140 30 L 220 35 L 260 70 L 250 140 L 210 200 L 200 260 L 180 340 L 160 440 L 140 540 L 120 620 L 90 610 L 110 500 L 130 380 L 140 260 L 130 150 L 110 80 Z";
export const ARGENTINA_VIEWBOX = "0 0 320 680";

export const VENEZUELA_SVG_PATH = "M 60 80 L 120 50 L 200 45 L 280 50 L 360 70 L 380 110 L 350 160 L 310 200 L 250 230 L 180 220 L 120 200 L 80 160 L 50 120 Z";
export const VENEZUELA_VIEWBOX = "0 0 420 280";

export interface SilhouetteData {
  path: string;
  viewBox: string;
  name: string;
  capital: string;
  coordinates: string;
}

const BASE_SILHOUETTES: Record<string, SilhouetteData> = {
  colombia: {
    path: COLOMBIA_SVG_PATH,
    viewBox: COLOMBIA_VIEWBOX,
    name: "Colombia",
    capital: "Bogotá",
    coordinates: "4.5709° N, 74.2973° W"
  },
  ecuador: {
    path: ECUADOR_SVG_PATH,
    viewBox: ECUADOR_VIEWBOX,
    name: "Ecuador",
    capital: "Quito",
    coordinates: "1.8312° S, 78.1834° W"
  },
  mexico: {
    path: MEXICO_SVG_PATH,
    viewBox: MEXICO_VIEWBOX,
    name: "México",
    capital: "Ciudad de México",
    coordinates: "23.6345° N, 102.5528° W"
  },
  usa: {
    path: USA_SVG_PATH,
    viewBox: USA_VIEWBOX,
    name: "Estados Unidos",
    capital: "Washington D.C.",
    coordinates: "37.0902° N, 95.7129° W"
  },
  brasil: {
    path: BRAZIL_SVG_PATH,
    viewBox: BRAZIL_VIEWBOX,
    name: "Brasil",
    capital: "Brasilia",
    coordinates: "14.2350° S, 51.9253° W"
  },
  peru: {
    path: PERU_SVG_PATH,
    viewBox: PERU_VIEWBOX,
    name: "Perú",
    capital: "Lima",
    coordinates: "9.1900° S, 75.0152° W"
  },
  chile: {
    path: CHILE_SVG_PATH,
    viewBox: CHILE_VIEWBOX,
    name: "Chile",
    capital: "Santiago",
    coordinates: "35.6751° S, 71.5430° W"
  },
  argentina: {
    path: ARGENTINA_SVG_PATH,
    viewBox: ARGENTINA_VIEWBOX,
    name: "Argentina",
    capital: "Buenos Aires",
    coordinates: "38.4161° S, 63.6167° W"
  },
  venezuela: {
    path: VENEZUELA_SVG_PATH,
    viewBox: VENEZUELA_VIEWBOX,
    name: "Venezuela",
    capital: "Caracas",
    coordinates: "6.4238° N, 66.5897° W"
  }
};

// Master lookup dictionary with case-insensitive and common alias normalization
export const COUNTRY_SILHOUETTES: Record<string, SilhouetteData> = {
  ...BASE_SILHOUETTES,
  "méxico": BASE_SILHOUETTES.mexico,
  "estados unidos": BASE_SILHOUETTES.usa,
  "estados_unidos": BASE_SILHOUETTES.usa,
  "eeuu": BASE_SILHOUETTES.usa,
  "ee.uu.": BASE_SILHOUETTES.usa,
  "united states": BASE_SILHOUETTES.usa,
  "brazil": BASE_SILHOUETTES.brasil,
  "perú": BASE_SILHOUETTES.peru,
};
