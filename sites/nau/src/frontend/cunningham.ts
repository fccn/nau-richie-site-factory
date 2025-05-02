import { defaultTokens, DefaultTokens, Configuration } from "@openfun/cunningham-react";

const config: Configuration = {
  themes: {
    default: {
      theme: {
        font: {
          families: { base: 'IBM Plex Sans', accent: 'IBM Plex Sans' },
        },
        colors: {
          'primary-100': '#B39AFD',
          'primary-200': '#f19597',
          'primary-300': '#e86a6f',
          'primary-400': '#693ae9',
          'primary-500': '#693ae9',
          'primary-600': '#e81f2f',
          'primary-700': '#1f1a61',
          'primary-800': '#4b19e6',
          'primary-900': '#bb0014',
          'secondary-100': '#eff8ff',
          'secondary-200': '#eaf3fd',
          'secondary-300': '#e2ebf5',
          'secondary-400': '#c0c9d3',
          'secondary-500': '#a3abb4',
          'secondary-600': '#79818a',
          'secondary-700': '#656c75',
          'secondary-800': '#454d55',
          'secondary-900': '#242b32',
          'black': '#000000',
          'black-two': '#232323',
          'dark': '#29303b',
          'brownish-grey': '#686868',
          'battleship-grey': '#686f7a',
          'purplish-grey': '#726c74',
          'light-grey': '#d2d2d2',
          'silver': '#d5dbe0',
          'pale-grey': '#eceff1',
          'white-three': '#fdfdfd',
          'white': '#ffffff',
          'turquoise-blue': '#0498be',
          'mediumturquoise': '#becde1',
          'robin-egg-blue': '#4fd0e7',
          'ocean-blue': '#0069b3',
          'darkish-blue': '#002d7f',
          'navy-blue': '#001f50',
          'lipstick': '#e51a2d',
          'indianred3': '#4b19e6',
          'mantis': '#76ce68',
        },
      },
      components: {
        button: {
          "border-radius": "0.25rem",
          "border-radius--active": "0.25rem",
          "background-color--active": "ref(theme.colors.indianred3)",
          "font-family": "ref(theme.font.families.base)",
        },
      },
    },
  },
};

export default config;