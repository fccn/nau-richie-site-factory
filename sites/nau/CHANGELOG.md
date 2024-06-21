# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- 🐛(rdfa) fix RDFa Course errors on Google Search Console

### Changed

- ⬆️(nau) upgrade richie to v2.32.0
- ⚰️(setttings) remove unused setting

## [1.28.0] - 2024-06-21

### Fixed

- 🐛(storage) fix missing staticfiles.json after collectstatic

### Changed

- ⚡️(assets) static assets only on nginx image.
  Remove option of deliver static assets from application
  docker image, to be more compatible with Richie upstream.
  Consequence is lower the app docker image size.
  The awscli was moved to nginx.

## [1.27.0] - 2024-06-19

### Changed

- 💚(circleci) upgrade circleci build
- 👷(docker) upgrade nodejs and python
- ⬆️(nau) upgrade richie to v2.28.0
- 💄(footer) refactor footer logos placeholder
- 💄(header) update nau fccn logo

### Fixed

- 🚨(pylint) fix pylint errors on the backend

### Added

- ✨(redirect) add new redirects to course and org

## [1.26.0] - 2024-05-29

### Added

- ⚡️(s3) add the CDNManifestStaticFilesStorage from Richie cookiecutter
  so we can use static assets from S3 Bucket like a CDN.

### Fixed

- 🌐(i18n) override translations to remove "Richie news" from blogpost badges

## [1.25.0] - 2024-05-13

### Changed

- 👷(s3) replace s3cmd with awscli, that is more speedy

## [1.24.0] - 2024-05-10

### Added

- ✨(redirect) add course redirect and joainie urls
- 👷(s3) install s3cmd to send static assets to compatible S3 compatible bucket

### Fixed

- 🔨(dev) update development environment variables from openfun.
  Copy the development environment variables from openfun.
  Configure to use a dummy LMS, to show LMS integration component.

## [1.23.0] - 2024-04-24

### Fixed

- 🔧(sentry) ignore dockerflow request.summary logger
- 🔊(log) remove request.summary logger
- 🗑️(jenkins) remove unnecessary jenkinsfile

### Added

- 🩺(kubernetes) liveness checks

## [1.22.0] - 2024-04-10

### Added

- 🩹(social) add default open graph image for social share of homepage page
- 🔧(sentry) additional Sentry settings
- 📌(plugins) add django_snippet for HTML inputs

### Changed

- 🔥(thirdparty) remove initializer code for third party services

### Fixed

- 📌(backend) pin django-cms to version less than 4
- 💚(circleci) fix docker-compose duplicate user key

## [1.21.0] - 2023-12-06

### Added

- ⚡️(html) improve performance by hint browsers to pre-connect to CDN or S3

### Changed

- 👷(dependabot) remove dependabot
- 💄(ui) refactor hero section
- 💄(ui) comment out instagram link on the footer
- 💄(ui) replace twitter with instagram on the footer
- 💄(course_glimpse) show course glimpse footer
- ⚡️(video) improve player button visibility
- 🍱(fonts) remove google fonts and replace them for local assets for performance
- ⬆️(nau) upgrade richie to v2.24.1
- ✨(seo) remove django-check-seo
- ⬆️(nginx) upgrade nginx to latest stable release 1.24.0
- ⚡️(chatbot) lazy load chatbot js
- ⚡️(video) lazy load embed video player
- 💚(circleci) upgrade circleci build
- ⬆️(frontend) upgrade frontend dev dependencies

### Fixed

- ♿️(footer) improve accessibility in NAU footer logo with a link to homepage.

## [1.20.1] - 2023-06-05

### Fixed

- 🐛(language) fix language name on course page

## [1.20.0] - 2023-04-21

### Fixed

- 🐛(search) fix redirect for the search course page.
  After the upgrade of django-cms v3.11.2 we can enable
  `CMS_REDIRECT_PRESERVE_QUERY_PARAMS` setting that fix the redirect of
  the parent courses page isn't the same of the course search.

### Changed

- ⬆️(nau) upgrade richie to v2.22.0
- ⬆️(dependencies) upgrade frontend dependencies
- ⬆️(dependencies) upgrade python dependencies

## [1.19.1] - 2023-03-23

### Fixed

- ⏪️(web_analytics) removed web analytics google tag manager custom code

## [1.19.0] - 2023-03-23

### Added

- ✅(jest) add jest tests to site factory
- ✨(api) update openedx-adapter adapter
- ✨(seo) add django-check-seo

### Changed

- ⬆️(nau) upgrade richie to v2.21.0
- ⬆️(nau) upgrade python dev dependencies
- 📈(web_analytics) upgraded web analytics django settings
- ⏪️(web_analytics) removed web analytics custom code
- ⏪️(openedx) removed richie frontend override of the openedx lms api
  integration.

### Fixed

- ⬆️(search) allow to configure multiple elastic search instances

## [1.18.0] - 2023-01-23

### Added

- 📈(web_analytics) add Google Tag Manager deploy per environment configuration
- ✨(cookies) make cookie bar optional, to activate it use COOKIE_BAR setting.
- 📈(web_analytics) add custom dimensions to NAU custom Google Tag Manager.

### Fixed

- 🐛(gitmoji) fix git lint with emoji

### Changed

- 💄(footer) Increase the size of the white part of footer where
some logos are put.

## [1.17.0] - 2022-11-11

### Added

- ✨(header) add maintenance message on header if setting
  `MAINTENANCE_HEADER_MSG` is true

### Changed

- ⬆️(nau) upgrade richie to v2.17.0
- 👷(docker) add app `nauedu/nau` docker image with static assets.
  The nauedu/nau docker image will start to have static assets,
  to improve rolling deploy of the static assets.
  We will stop use the `nauedu/nau-nginx` docker image and use the
  newer dynamic built nginx image.
  This newer nginx image will have the static assets from both 
  current/older and new releases, so the user don't view a missing css
  during the rolling deploy.

## [1.16.0] - 2022-10-25

### Changed

- ⬆️(nginx) upgrade nginx to latest stable release 1.22.1
- ⬆️(nau) upgrade richie to v2.16.0

## [1.15.0] - 2022-10-25

### Added

- 🔧(language) add django language settings that allows to configure language
  cookies differently, so we can share it with the open edx.

### Changed

- 💄(template) help url on header menu
- 💄(template) remove category tag icon

### Fixed

- 🌐(i18n) fix share course mailto references Richie instead of NAU
- 🐛(cache) limit the cache ttl for course pages based on course run dates
- 🐛(scss) enroll button is not clickable on small width screens
- 🐛(scss) persons category tags have the wrong hover color
- 🐛(scss) fix issues with background on icon tag

## [1.14.1] - 2022-09-01

### Fixed

- ➕(dependencies) add pip requests package for open edx lms backend.

## [1.14.0] - 2022-09-01

### Changed

- 💄(scss) clear person detail subheader whitespace
- 🐛(scss) fix border-radius in cutting the corners of entity logos
- 🐛(scss) fix issues with category tag rendering
- 🔨(frontend) add package.json ts build output dir
- ⬆️(nau) upgrade richie to v2.15.1
- ♻️(scss) refactor scss code

### Added

- ✨(googletagmanager) add Google Tag Manager to nau site without using
  Richie upstream Web Analytics.
- 🔧(rolling_deploy) Enable the deliver of the static asset files like css,
  images, fonts, etc. Nginx will also deliver this files, but during rolling
  deploy, the nginx could have one version of the files and the app still
  running a different version.

## [1.13.0] - 2022-06-28

### Changed

- 💄(logo) add by fccn on nau logo
- ⬆️(nau) upgrade richie to v2.15.0
- upgrade node to v16

## [1.12.0] - 2022-05-24

### Added

- ✨(chatbot) add course parameter to chatbot widget

## [1.11.0] - 2022-05-18

### Added

- ✨(chatbot) add chatbot widget if the setting `CHATBOT_WIDGET_JS_URL`
  is defined.

## [1.10.0] - 2022-04-20

### Changed

- 🐛(cookies) fix cookie policy link

## [1.9.0] - 2022-04-20

### Changed

- ⬆️(richie) upgrade richie to v2.14.1

## [1.8.0] - 2022-04-05

### Changed

- ⬆️(richie) upgrade richie to v2.14.0
- ⚰️(course_detail) remove overridden blocks on course detail template.
  The specific code have been moved, improved and superseded by uptream.
- 🔧(jira) configure Jira Service Desk widget on local development

### Fixed

- ⬆️(richie) fix frontend upgrade

## [1.7.0] - 2022-03-29

### Changed

- ⬆️(dependencies) upgrade dependencies

## [1.6.0] - 2022-03-29

### Fixed

- 💄(course_detail) fix title size and color of plan and organization
- 💚(circleci) fix circleci check configuration step
- 🌐(i18n) fix missing translations

### Changed

- 🐛(cache) lower page content cache from 1 day to 30 minutes

## [1.5.0] - 2022-03-14

### Fixed

- 💄(course_detail) remove excessive text in "What you'll learn"
- 🐛(css) fix blog category tags text color
- 💄(css) fix check mark color when course skills contains a list of items

### Changed

- 💄(course_detail) higher enroll button.
  Move enroll button for open to enroll course runs to be higher on the
  screen. For a single open course run the enroll button is visible on
  the right using a desktop viewport. If using mobile at 
  least it will be visible for simple swipe instead of scrolling
  to the button of the screen.
- ⬆️(richie) upgrade richie to v2.13.0
- ⬆️(search) upgrade elastic search to 7.17.0

## [1.4.0] - 2022-02-14

### Changed

- 💄(header) preserve the order of the components language change combo box, 
  login and register buttons, so they have the same presentation as the LMS.

## [1.3.0] - 2022-02-11

### Added

- ✨(404) add arquivo404 js to 404 page on Richie
- ✨(tracking) add facebook pixel tracking code

### Fixed

- 🐛(search) fix header and home search component
- 🌐(i18n) translate missing string

### Changed

- 💄(course_glimpse) rework course glimpse cards
- 🌐(i18n) change translations of 'Persons' and 'First session' for PT and EN.
- ⬆️(dependencies) upgrade frontend dependencies
- ⬆️(python) upgrade python to 3.10
- ⬆️(dependencies) upgrade python dependencies
- ⬆️(richie) upgrade richie to 2.12.0
- ✅(jira) add jira service desk test
- ♻️(styles) clean unused values in theme.scss
- 💄(footer) fix link hover color
- ♻️(styles) refactor style to reflect merge maps
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

