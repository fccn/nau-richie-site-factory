# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- 📌(ap) pin django-formtools version
  richie leaves django-formtools as an unpinned transitive dependency, so
  a fresh image build can silently resolve a newer version with a breaking
  regression (django-formtools 2.6.1 changed get_form_list() caching
  behaviour, breaking the CMS wizard used to create blog posts and other
  pages with TypeError: BaseForm.__init__() got an unexpected keyword
  argument 'wizard_user'). Pin to the version already fixed upstream by
  richie (django-formtools<2.6, see openfun/richie#9a84bc4) to prevent
  future drift on rebuild.
- 🐛(ap) stop disallowing crawling of parameterized URLs in robots.txt
  The `Disallow: *?*` rule added for fccn/nau-technical#991 conflicted with
  the self-referencing canonical tag strategy added for
  fccn/nau-technical#993: Google explicitly recommends against using
  robots.txt for canonicalization, since a page can still get indexed (e.g.
  via an external link, such as a social media post linking a paginated
  URL) without ever being crawled to read its canonical tag - which
  prevents consolidating that page's link signals onto the clean URL,
  instead of achieving that consolidation as intended. The canonical tag
  alone already fully handles duplicate-content consolidation for these
  URLs, so revert the robots.txt rule and rely on canonical only.

## [1.5.2] - 2026-08-21

### Fixed

- 📌(ap) pin Django and djangocms-link versions
  richie leaves Django and djangocms-link as unpinned transitive
  dependencies, so a fresh image build can silently resolve a newer
  djangocms-link with a breaking DB migration (5.2.0 renamed the
  Link.target column to link_target). Pin both to the versions
  currently deployed and already migrated (Django 4.2.30,
  djangocms-link 5.1.1) to prevent future drift on rebuild.

## [1.5.1] - 2026-08-20

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
