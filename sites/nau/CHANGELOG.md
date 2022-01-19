# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- ♻️(styles) refactor style to reflect merge maps

### Changed

- ⬆️(richie) upgrade richie to 2.11.0
- 💄(search-input) header search bar theme improvements
- 💄(category-glimpse) category glimpse rendering and background fix
- 💄(reboot) default link color and menu selected fix

## [1.2.0] - 2021-12-07

### Changed

- ⬆️(upgrade) upgrade frontend js libraries

### Added

- ♻️(styles) add extras to styles

### Fixed

- 💚(ci) fix circleci builds
- 💄(blogpost glimpse) correct the cover colo

## [1.1.0] - 2021-11-05

### Changed

- ⬆️(richie) upgrade richie to 2.9.1

### Fixed

-💄(styles) fix header styles and hero background

## [1.0.2] - 2021-11-03

### Fixed

- 🌐(language) revert change default language to pt

## [1.0.1] - 2021-11-03

### Fixed

- 🐛(upgrade) fix richie upgrade

## [1.0.0] - 2021-11-02

### Added

- 🍱(icon) add nau icons
- 💄(hero) new styles for nau hero
- 💚(jenkins) jenkins build jobs to build node
- 🌐(footer) localize footer
- 🚨(linter) run linters

### Fixed
- 💄(header) fix header menu render issues
- 💄(header) fix blue underline on main menu
- ➖(jquery) remove jquery JS
- 💄(courses) remove contact us button

### Changed
- ⬆️(richie) upgrade richie to 2.9.0
- 🌐(language) change default language to pt
- 🎨(footer) change newsletter link to be relative
- 🩹(footer) change footer social network links

## [0.3.1] - 2021-10-11

### Fixed

- ⬆️(upgrade) fix upgrade richie frontend

## [0.3.0] - 2021-10-11

### Fixed

- ⬆️(upgrade) upgrade richie frontend

### Changed

- 💄(pages) change page header colors

## [0.2.0] - 2021-10-11

### Changed

- 💄(footer) add max-height to entity logos
- 💄(fonts) replace fonts for NAU alternatives
- 💄(colors) add NAU colors to the palette
- 💄(footer) simplify footer styles
- 🔍️(seo) robots.txt delived by richie
- 💄(footer) add footer overrides
- ✨(support) add jira service desk support widget
- 📈(cookie) add cookie message
- 📈(web_analytics) add settings for web analytics
- 🔨(dev cache) remove cache during development
- 🩹(setup) fix metadata name
- 💄(frontend) add template to override style
- ⬆️(richie) Upgrade richie GN-622
- 🌐(translations) fix translation
- 🔧(settings) add course run sync config
- 💚(jenkins) stop build containers
- 💚(nginx) use nginx official docker image
- ⬆️(nginx) upgrade nginx to 1.20.1
- 🛂(edx) delegate authentication to open edX LMS
- 🛂(edx) delegate authentication to open edX LMS
- 🐛(search) add pt lang to search
- 🛂(edx) delegate authentication to open edX LMS
- 🩹(menu) change order of the LMS menu
- 🌐(menu) translate lms menu options to pt-pt
- 🐛(docker) install wait-for-it tool

## [0.1.0] - 2021-07-19

### Added

- Install richie for NAU site
- Configure media storage to use Ceph S3 Bucket
- Add a Gunicort worker abort handler that prints the current stack trace when
  the worker timeout's 
  or blocks on waiting for an external dependency.
- Changed primary action colors from red to NAU blues

## [0.0.1-alpha1] - 2021-07-12

### Changed

- Install richie for NAU

