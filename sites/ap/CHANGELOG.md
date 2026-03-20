# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- 💥(ap) upgrade ap site with latest version
  Upgrade the ap site with the coockiecutter
  latest upstream version. All the packages
  including richie version.
- 💥(ap) revert to use official NGINX image
  Revert to use again the official NGINX docker image.
  Also upgrade to latest stable release.
- 🔨(deps) add missing pbr dev dependency for bandit

## [1.4.0] - 2026-01-08

### Added

-💄(ap) changed how the course availability is displayed

### Fixed

- 💚(circleci) check-changes job fix and redis image update 
    - Fix CI pipeline by correcting branch reference to origin/master
    - Updated the redis images from bitnami to fundocker

## [1.3.0] - 2025-07-02

### Changed

- 🔥(video) remove lazy load video player
- ⬆️(ap) upgrade dependencies
- 🔧(ap) update settings w/ site cookiecutter
- ⚰️(maintenance) remove maintenance functionality
- ⬆️(ap) upgrade richie to v3.1.2

### Fixed

- 🐛(ap) added homepage logo link to the header

## [1.2.1] - 2025-04-16

### Fixed

- 💚(ap) adjust CI build

## [1.2.0] - 2025-04-16

### Changed

- ⬆️(ap) upgrade richie to v3.0.0

## [1.1.1] - 2025-04-01

### Fixed

- 🐛(ap) adjusted login redirect
  Override backend authentication to adjust the 
  login redirect 

## [1.1.0] - 2025-03-21

### Added

- 🔧(ap) add media S3 default ACL to `public-read`
- 🔧(ap) allow to configure Django Storages from environment `DJANGO_STORAGES`
- ✨(ap) added features to meet the first release requirements
  Changed logo image
  Removed english language and leave only portuguese
  Set the missing variable `RICHIE_FILTERS_PRESENTATION`
  to have the filters working

### Changed
- Updated the favicon and apple touch icon variants
- ⬆️(ap) upgrade richie to v3.0.0

## [1.0.0] - 2025-03-06

### Added 

- 🎉(ap) started the site ap_nau

### Changed

- 🚧(ap) added search filters to ap_nau
- 💄(ap) updated branding and colors for ap_nau
- 🚧(ap) added demo-site command to support multilingual generation
- 🔥(templates) removed custom parameter page_url in the template
- 👷(ap) added ci build for ap site
- 🚚(ap) renamed the site name from ap_nau to ap
- ✨(ap) define search filters
