# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Install richie for C-Academy

### Added

- 🔧(rolling_deploy) Enable the deliver of the static asset files like css,
  images, fonts, etc. Nginx will also deliver this files, but during rolling
  deploy, the nginx could have one version of the files and the app still
  running a different version.
