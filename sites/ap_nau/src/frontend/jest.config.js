const path = require('path');

module.exports = {
  preset: 'ts-jest',
  moduleDirectories: [path.resolve(__dirname, 'js'), 'node_modules'],
  modulePaths: [
    '<rootDir>',
    '<rootDir>/node_modules/richie-education/js/',
  ],
  moduleFileExtensions: ['css', 'js', 'ts', 'tsx'],
  moduleNameMapper: {
    '\\.(css)$': '<rootDir>/front/__mocks__/styleMock.js',
    '^lodash-es$': 'lodash',
  },
  setupFilesAfterEnv: ['<rootDir>/jest/setup.ts'],
  testMatch: [`${__dirname}/js/**/*.spec.+(ts|tsx|js)`],
  coverageDirectory: '.coverage',
  testEnvironment: 'jsdom',
  testEnvironmentOptions: {
    url: 'https://localhost',
  },
  resolver: '<rootDir>/node_modules/richie-education/jest/resolver.js',
  transformIgnorePatterns: [
    '<rootDir>/node_modules/(?!(lodash-es|@hookform/resolvers|query-string|decode-uri-component|split-on-first|filter-obj|richie-education)/)',
  ],
  globals: {
    RICHIE_VERSION: 'test',
  },
};