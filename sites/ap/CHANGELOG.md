# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- 🐛(ap) cache sitemap.xml response to avoid crawler timeouts
  The sitemap.xml endpoint was rebuilt from the database on every request,
  which was slow enough to make search engine crawlers time out. Wrap the
  view with Django's cache_page (configurable via SITEMAP_CACHE_TIMEOUT,
  defaults to 24h) so it is served instantly after the first request.
- 🐛(ap) serve https:// URLs in sitemap.xml and robots.txt behind the proxy
  The app sits behind a reverse proxy that terminates TLS and forwards plain
  HTTP, so request.is_secure() always evaluated to False. Configure
  SECURE_PROXY_SSL_HEADER so the sitemap's <loc> entries and the robots.txt
  "Sitemap:" line correctly advertise https:// instead of http://.
- 🐛(ap) disallow crawling of parameterized URLs in robots.txt
  Query-string URLs (pagination on detail pages, client-side search filters,
  tracking params...) are not unique indexable content; all real content
  already lives at clean, path-based URLs covered by the sitemap. Add
  `Disallow: *?*` to reduce crawl budget waste and duplicate content
  discovery.
- 🐛(ap) add self-referencing canonical tag to every indexable page
  Pages had no canonical tag, risking duplicate-content signals across
  paginated, filtered and query-string URL variants. Add a self-referencing
  `<link rel="canonical">` (built from the same https-aware SITE.web_url used
  by the sitemap/robots.txt fixes) pointing to the clean, absolute URL of the
  current page, with query strings excluded so pagination/search-filter
  variants consolidate onto the canonical page.

## [1.5.0] - 2026-05-15

### Changed

- 💥(ap) upgrade ap site with Richie v3.4.0
  Upgrade the ap site with the coockiecutter
  latest upstream version. All the packages
  including richie version.
- 💥(ap) revert to use official NGINX image
  Revert to use again the official NGINX docker image.
  Also upgrade to latest stable release.
- 🔨(deps) add missing pbr dev dependency for bandit
- 🐛(deps) upgrade raincoat to 1.2.4 for Python 3.11 compatibility
- 💄(course) change heading font size on course page
- ⬆️(deps) update python dependencies

### Fixed

- 🐛(frontend) backport improve error handling for enrollment
- 📌(deps) pin front dependencies
- 🐛(ap) fix course page rendering
- 💄(ap) fix social network logo
  Replace the image that is shown by default when sharing
  the homepage of AP site to a social network.

### Added

- ✨(profile) add optional gamma dashboard menu items
  Add Performance and Leaderboard menu items to user profile dropdown.
  Both are disabled by default and can be enabled via environment variables
  AUTHENTICATION_PROFILE_URL_PERFORMANCE_ENABLED and
  AUTHENTICATION_PROFILE_URL_LEADERBOARD_ENABLED respectively.

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
