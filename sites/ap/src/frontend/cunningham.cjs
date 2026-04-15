/* Custom Cunningham Tokens for Richie

   In a child project, you can override those tokens by creating a token file like this one,
   merge your custom tokens with default Richie ones then by using cunningham cli to generate
   sass and ts tokens files (take a look to the `build-theme` command within package.json
   see it in action).

*/

module.exports = {
  themes: {
    default: {
      theme: {
        font: {
          families: { base: 'Rubik', accent: 'Roboto' },
        },
        colors: {
          'primary-100': '#f5e6f5',
          'primary-200': '#e1bfe2',
          'primary-300': '#cd99ce',
          'primary-400': '#9e5c9f',
          'primary-500': '#701471',
          'primary-600': '#5f115f',
          'primary-700': '#4e0e4e',
          'primary-800': '#3d0b3d',
          'primary-900': '#2c082c',
          'secondary-100': '#fce7ec',
          'secondary-200': '#f7bfce',
          'secondary-300': '#f297b0',
          'secondary-400': '#ed6f92',
          'secondary-500': '#d31145',
          'secondary-600': '#b90e3c',
          'secondary-700': '#9f0c33',
          'secondary-800': '#85092a',
          'secondary-900': '#6b0722',
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
          'indianred3': '#df484b',
          'mantis': '#76ce68',
        },
      },
      components: {
        button: {
          'font-family': 'Rubik',
          'font-weight': 'bold',
          'background-color': '#09122c',
        },
      },
      contextuals: {
        content: {
          semantic: {
             brand: { 'on-brand': 'ref(globals.colors.gray-000)', tertiary: 'ref(globals.colors.gray-600)' },
          },
        },
      },
      globals: {
        colors: {
          'brand-050': '#fef5f6',  // Lightest red
          'brand-100': '#fde8eb',
          'brand-150': '#fbdade',
          'brand-200': '#f7b5bd',
          'brand-250': '#f3919c',
          'brand-300': '#ef6d7c',
          'brand-350': '#ea4a5b',
          'brand-400': '#d73e50',
          'brand-450': '#c83748',
          'brand-500': '#be3144',  // Base brand red
          'brand-550': '#ab2c3d',
          'brand-600': '#982736',
          'brand-650': '#85222f',
          'brand-700': '#721d28',
          'brand-750': '#5f1821',
          'brand-800': '#4c131a',
          'brand-850': '#390e13',
          'brand-900': '#26090c',
          'brand-950': '#130405',  // Darkest red
        },
      },
    },
  },
};