"""
Django settings for the richie NAU project.
"""
import json
import os

from django.utils.translation import gettext_lazy as _

# pylint: disable=ungrouped-imports
import sentry_sdk
from configurations import Configuration, values
from richie.apps.courses.settings.mixins import RichieCoursesConfigurationMixin
from sentry_sdk.integrations.django import DjangoIntegration

from base.utils import merge_dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join("/", "data")


def get_release():
    """Get the current release of the application.

    By release, we mean the release from the version.json file à la Mozilla [1]
    (if any). If this file has not been found, it defaults to "NA".

    [1]
    https://github.com/mozilla-services/Dockerflow/blob/master/docs/version_object.md
    """
    # Try to get the current release from the version.json file generated by the
    # CI during the Docker image build
    try:
        with open(os.path.join(BASE_DIR, "version.json")) as version:
            return json.load(version)["version"]
    except FileNotFoundError:
        return "NA"  # Default: not available


class StyleguideMixin:
    """
    Theme styleguide reference

    Only used to build styleguide page without the need to hardcode properties
    and values into styleguide template.
    """

    STYLEGUIDE = {
        # Available font family names
        "fonts": ["hind", "montserrat"],
        # Named color palette
        "palette": [
            "black",
            "black-two",
            "dark",
            "brownish-grey",
            "battleship-grey",
            "purplish-grey",
            "light-grey",
            "silver",
            "pale-grey",
            "white-three",
            "white",
            "navy-blue",
            "darkish-blue",
            "ocean-blue",
            "turquoise-blue",
            "robin-egg-blue",
            "mediumturquoise",
            "lipstick",
            "indianred3",
        ],
        # Available gradient background
        "gradient_colors": [
            "neutral-gradient",
            "light-gradient",
            "middle-gradient",
            "dark-gradient",
            "white-mask-gradient",
        ],
        # Available color schemes
        "schemes": [
            "primary",
            "secondary",
            "tertiary",
            "clear",
            "light",
            "lightest",
            "indianred3",
            "neutral-gradient",
            "light-gradient",
            "middle-gradient",
            "dark-gradient",
            "white-mask-gradient",
            "clouds",
            "transparent-clear",
            "transparent-darkest",
        ],
    }


class DRFMixin:
    """
    Django Rest Framework configuration mixin.
    NB: DRF picks its settings from the REST_FRAMEWORK namespace on the settings, hence
    the nesting of all our values inside that prop
    """

    REST_FRAMEWORK = {
        "ALLOWED_VERSIONS": ("1.0",),
        "DEFAULT_VERSION": "1.0",
        "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework.authentication.SessionAuthentication",
        ),
    }


class Base(StyleguideMixin, DRFMixin, RichieCoursesConfigurationMixin, Configuration):
    """
    This is the base configuration every configuration (aka environnement) should inherit from. It
    is recommended to configure third-party applications by creating a configuration mixins in
    ./configurations and compose the Base configuration with those mixins.

    It depends on an environment variable that SHOULD be defined:

    * DJANGO_SECRET_KEY

    You may also want to override default configuration by setting the following environment
    variables:

    * DJANGO_SENTRY_DSN
    * RICHIE_ES_HOST
    * DB_NAME
    * DB_USER
    * DB_PASSWORD
    * DB_HOST
    * DB_PORT
    """

    DEBUG = False

    SITE_ID = 1

    # Security
    ALLOWED_HOSTS = values.ListValue([])
    SECRET_KEY = "ThisIsAnExampleKeyForDevPurposeOnly"  # nosec
    # System check reference:
    # https://docs.djangoproject.com/en/3.1/ref/checks/#security
    SILENCED_SYSTEM_CHECKS = values.ListValue(
        [
            # Allow the X_FRAME_OPTIONS to be set to "SAMEORIGIN"
            "security.W019"
        ]
    )
    # The X_FRAME_OPTIONS value should be set to "SAMEORIGIN" to display
    # DjangoCMS frontend admin frames. Dockerflow raises a system check security
    # warning with this setting, one should add "security.W019" to the
    # SILENCED_SYSTEM_CHECKS setting (see above).
    X_FRAME_OPTIONS = "SAMEORIGIN"

    # Django change the default value to `same-origin` on version 3.1, but we need that JS AJAX
    # calls send at least the richie hostname to Open edX LMS.
    # The Open edx LMS uses the HTTP meta `HTTP_REFERER` to validade that the request was sent by
    # the richie site.
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

    # Application definition
    ROOT_URLCONF = "nau.urls"
    WSGI_APPLICATION = "nau.wsgi.application"

    # Database
    DATABASES = {
        "default": {
            "ENGINE": values.Value(
                "django.db.backends.mysql",
                environ_name="DB_ENGINE",
                environ_prefix=None,
            ),
            "NAME": values.Value("richie", environ_name="DB_NAME", environ_prefix=None),
            "USER": values.Value(
                "richie_user", environ_name="DB_USER", environ_prefix=None
            ),
            "PASSWORD": values.Value(
                "pass", environ_name="DB_PASSWORD", environ_prefix=None
            ),
            "HOST": values.Value(
                "localhost", environ_name="DB_HOST", environ_prefix=None
            ),
            "PORT": values.Value(3306, environ_name="DB_PORT", environ_prefix=None),
            # "OPTIONS": {
            #     "charset": values.Value(
            #         "utf8mb4", environ_name="DB_OPTION_CHARSET", environ_prefix=None
            #     )
            # },
        }
    }
    MIGRATION_MODULES = {}

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = values.Value("/static/")
    MEDIA_URL = values.Value("/media/")
    MEDIA_ROOT = os.path.join(DATA_DIR, "media")
    STATIC_ROOT = os.path.join(DATA_DIR, "static")

    # For static files, we want to use a backend that includes a hash in
    # the filename, that is calculated from the file content, so that browsers always
    # get the updated version of each file.
    STATICFILES_STORAGE = values.Value(
        "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    )

    AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

    # AUTHENTICATION DELEGATION
    RICHIE_AUTHENTICATION_DELEGATION = {
        "BASE_URL": values.Value(
            "", environ_name="AUTHENTICATION_BASE_URL", environ_prefix=None
        ),
        "BACKEND": values.Value(
            "openedx-hawthorn",
            environ_name="AUTHENTICATION_BACKEND",
            environ_prefix=None,
        ),
        # PROFILE_URLS are custom links to access to Auth profile views
        # from Richie. Link order will reflect the order of display in frontend.
        # (i) Info - {base_url} is AUTHENTICATION_DELEGATION.BASE_URL
        # (i) If you need to bind user data into href url, wrap the property between ()
        # e.g: for user.username = johndoe, /u/(username) will be /u/johndoe
        "PROFILE_URLS": values.DictValue(
            {
                "dashboard": {
                    "label": _("Dashboard"),
                    "href": _("{base_url:s}/dashboard"),
                },
                "account": {
                    "label": _("Account"),
                    "href": _("{base_url:s}/account/settings"),
                },
                "profile": {
                    "label": _("Profile"),
                    "href": _("{base_url:s}/u/(username)"),
                },
            },
            environ_name="AUTHENTICATION_PROFILE_URLS",
            environ_prefix=None,
        ),
    }

    # LMS
    RICHIE_LMS_BACKENDS = [
        {
            "BASE_URL": values.Value(environ_name="EDX_BASE_URL", environ_prefix=None),
            "BACKEND": values.Value(
                "richie.apps.courses.lms.edx.EdXLMSBackend",
                environ_name="EDX_BACKEND",
                environ_prefix=None,
            ),
            "JS_BACKEND": values.Value(
                "openedx-hawthorn",
                environ_name="EDX_JS_BACKEND",
                environ_prefix=None,
            ),
            "COURSE_REGEX": values.Value(
                r"^.*/courses/(?P<course_id>.*)/course/?$",
                environ_name="EDX_COURSE_REGEX",
                environ_prefix=None,
            ),
            "JS_COURSE_REGEX": values.Value(
                r"^.*/courses/(?<course_id>.*)/course/?$",
                environ_name="EDX_JS_COURSE_REGEX",
                environ_prefix=None,
            ),
            # Course runs synchronization
            "COURSE_RUN_SYNC_NO_UPDATE_FIELDS": [],
            "DEFAULT_COURSE_RUN_SYNC_MODE": "sync_to_public",
        }
    ]
    RICHIE_COURSE_RUN_SYNC_SECRETS = values.ListValue([])

    # Internationalization
    TIME_ZONE = values.Value(
        "Europe/Lisbon", environ_name="TIME_ZONE", environ_prefix=None
    )
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

    # Mapping between edx and richie profile fields
    EDX_USER_PROFILE_TO_DJANGO = {
        "preferred_username": "username",
        "email": "email",
        "name": "full_name",
        "given_name": "first_name",
        "family_name": "last_name",
        "locale": "language",
        "user_id": "user_id",
        "administrator": "is_staff",
    }

    # Templates
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(BASE_DIR, "templates")],
            "OPTIONS": {
                "context_processors": [
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.template.context_processors.media",
                    "django.template.context_processors.csrf",
                    "django.template.context_processors.tz",
                    "sekizai.context_processors.sekizai",
                    "django.template.context_processors.static",
                    "cms.context_processors.cms_settings",
                    "richie.apps.core.context_processors.site_metas",
                    "nau.jira_service_desk.context_processors.jira_widget_key_setting",
                    "nau.chatbot.context_processors.chatbot_widget_js_url_setting",
                    "nau.facebook_pixel.context_processors.facebook_pixel_setting",
                    "nau.google_tag_manager.context_processors.google_tag_manager_setting",
                    "nau.help_desk.context_processors.help_desk_url_setting",
                ],
                "loaders": [
                    "django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader",
                ],
            },
        }
    ]

    # Placeholders
    CMS_PLACEHOLDER_CONF_OVERRIDES = {
        "courses/cms/course_detail.html course_teaser": {
            "name": _("Teaser"),
            "plugins": ["LTIConsumerPlugin", "VideoPlayerPlugin"],
            "limits": {
                "LTIConsumerPlugin": 1,
                "VideoPlayerPlugin": 1,
            },
        },
    }

    MIDDLEWARE = (
        "richie.apps.core.cache.LimitBrowserCacheTTLHeaders",
        "cms.middleware.utils.ApphookReloadMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "dockerflow.django.middleware.DockerflowMiddleware",
        "cms.middleware.user.CurrentUserMiddleware",
        "cms.middleware.page.CurrentPageMiddleware",
        "cms.middleware.toolbar.ToolbarMiddleware",
        "cms.middleware.language.LanguageCookieMiddleware",
        "dj_pagination.middleware.PaginationMiddleware",
    )

    INSTALLED_APPS = (
        # Richie demo stuff
        "base",
        # Richie stuff
        "richie.apps.demo",
        "richie.apps.search",
        "richie.apps.courses",
        "richie.apps.core",
        "richie.plugins.glimpse",
        "richie.plugins.html_sitemap",
        "richie.plugins.large_banner",
        "richie.plugins.nesteditem",
        "richie.plugins.plain_text",
        "richie.plugins.section",
        "richie.plugins.simple_picture",
        "richie.plugins.simple_text_ckeditor",
        "richie.plugins.lti_consumer",
        "richie",
        # Third party apps
        "dj_pagination",
        "dockerflow.django",
        "parler",
        "rest_framework",
        "storages",
        # Django-cms
        "djangocms_admin_style",
        "djangocms_googlemap",
        "djangocms_link",
        "djangocms_picture",
        "djangocms_text_ckeditor",
        "djangocms_video",
        "cms",
        "menus",
        "sekizai",
        "treebeard",
        "filer",
        "easy_thumbnails",
        # django-autocomplete-light
        "dal",
        "dal_select2",
        # Django
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.admin",
        "django.contrib.sites",
        "django.contrib.sitemaps",
        "django.contrib.staticfiles",
        "django.contrib.messages",
        "django.contrib.humanize",
    )

    # Languages
    # - Django
    LANGUAGE_CODE = "en"

    # Careful! Languages should be ordered by priority, as this tuple is used to get
    # fallback/default languages throughout the app.
    # Use "en" as default as it is the language that is most likely to be spoken by any visitor
    # when their preferred language, whatever it is, is unavailable
    LANGUAGES = (("en", _("English")), ("pt", _("Portuguese")))

    # - Django CMS
    CMS_LANGUAGES = {
        "default": {
            "public": True,
            "hide_untranslated": False,
            "redirect_on_fallback": True,
            "fallbacks": ["en", "pt"],
        },
        1: [
            {
                "public": True,
                "code": "en",
                "hide_untranslated": False,
                "name": _("English"),
                "fallbacks": ["pt"],
                "redirect_on_fallback": False,
            },
            {
                "public": True,
                "code": "pt",
                "hide_untranslated": False,
                "name": _("Portuguese"),
                "fallbacks": ["en"],
                "redirect_on_fallback": False,
            },
        ],
    }

    # - Django Parler
    PARLER_LANGUAGES = CMS_LANGUAGES

    # Permisions
    # - Django CMS
    CMS_PERMISSION = True

    # - Django Filer
    FILER_ENABLE_PERMISSIONS = True
    FILER_IS_PUBLIC_DEFAULT = True

    # - Django Pagination
    PAGINATION_INVALID_PAGE_RAISES_404 = True
    PAGINATION_DEFAULT_WINDOW = 2
    PAGINATION_DEFAULT_MARGIN = 1

    # Logging
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            }
        },
        "loggers": {
            "django": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": True,
            }
        },
    }

    # Web Analytics configuration
    WEB_ANALYTICS_ID = values.Value(
        None, environ_name="WEB_ANALYTICS_ID", environ_prefix=None
    )
    WEB_ANALYTICS_LOCATION = values.Value(
        "head", environ_name="WEB_ANALYTICS_LOCATION", environ_prefix=None
    )
    WEB_ANALYTICS_PROVIDER = values.Value(
        "google_analytics", environ_name="WEB_ANALYTICS_PROVIDER", environ_prefix=None
    )

    # Minimum enrollment count value that would be shown on course detail page
    RICHIE_MINIMUM_COURSE_RUNS_ENROLLMENT_COUNT = values.Value(
        50,
        environ_name="RICHIE_MINIMUM_COURSE_RUNS_ENROLLMENT_COUNT",
        environ_prefix=None,
    )

    # Demo
    RICHIE_DEMO_SITE_DOMAIN = "localhost:8080"
    RICHIE_DEMO_FIXTURES_DIR = os.path.join(BASE_DIR, "base", "fixtures")

    # Elasticsearch
    RICHIE_ES_HOST = values.Value(
        "elasticsearch", environ_name="RICHIE_ES_HOST", environ_prefix=None
    )
    RICHIE_ES_INDICES_PREFIX = values.Value(
        default="richie", environ_name="RICHIE_ES_INDICES_PREFIX", environ_prefix=None
    )
    RICHIE_ES_STATE_WEIGHTS = values.ListValue(None)

    # LTI Content
    RICHIE_LTI_PROVIDERS = {
        "lti_provider_demo": {
            "oauth_consumer_key": values.Value(
                "jisc.ac.uk",
                environ_name="LTI_TEST_OAUTH_CONSUMER_KEY",
                environ_prefix=None,
            ),
            "shared_secret": values.Value(
                "secret",
                environ_name="LTI_TEST_SHARED_SECRET",
                environ_prefix=None,
            ),
            "base_url": values.Value(
                "https://lti.tools/saltire/tp",
                environ_name="LTI_TEST_BASE_URL",
                environ_prefix=None,
            ),
            "display_name": "basic-lti-launch-request",
            "inline_ratio": 0.75,
        }
    }

    # Cache
    CACHES = values.DictValue(
        {
            "default": {
                "BACKEND": values.Value(
                    "base.cache.RedisCacheWithFallback",
                    environ_name="CACHE_DEFAULT_BACKEND",
                    environ_prefix=None,
                ),
                "LOCATION": values.Value(
                    "mymaster/redis-sentinel:26379,redis-sentinel:26379/0",
                    environ_name="CACHE_DEFAULT_LOCATION",
                    environ_prefix=None,
                ),
                "OPTIONS": values.DictValue(
                    {
                        "CLIENT_CLASS": "richie.apps.core.cache.SentinelClient",
                    },
                    environ_name="CACHE_DEFAULT_OPTIONS",
                    environ_prefix=None,
                ),
                "TIMEOUT": values.IntegerValue(
                    300, environ_name="CACHE_DEFAULT_TIMEOUT", environ_prefix=None
                ),
            },
            "memory_cache": {
                "BACKEND": values.Value(
                    "django.core.cache.backends.locmem.LocMemCache",
                    environ_name="CACHE_FALLBACK_BACKEND",
                    environ_prefix=None,
                ),
                "LOCATION": values.Value(
                    None,
                    environ_name="CACHE_FALLBACK_LOCATION",
                    environ_prefix=None,
                ),
                "OPTIONS": values.DictValue(
                    {},
                    environ_name="CACHE_FALLBACK_OPTIONS",
                    environ_prefix=None,
                ),
            },
        }
    )

    # For more details about CMS_CACHE_DURATION, see :
    # http://docs.django-cms.org/en/latest/reference/configuration.html#cms-cache-durations
    CMS_CACHE_DURATIONS = values.DictValue(
        {"menus": 3600, "content": 60, "permissions": 3600}
    )

    # Sessions
    SESSION_ENGINE = values.Value("django.contrib.sessions.backends.cache")

    # Sentry
    SENTRY_DSN = values.Value(None, environ_name="SENTRY_DSN")

    # Admin
    # - Django CMS
    # Maximum children nodes to allow a parent to be unfoldable
    # in the page tree admin view
    CMS_PAGETREE_DESCENDANTS_LIMIT = 80

    # Add richie search query analyzer elasticsearch the Portuguese language
    RICHIE_QUERY_ANALYZERS = {"en": "english", "pt": "portuguese"}

    # Add JIRA Service Desk Widget Key
    JIRA_WIDGET_KEY = values.Value(
        None, environ_name="JIRA_WIDGET_KEY", environ_prefix=None
    )

    # Add Facebook Pixel
    FACEBOOK_PIXEL_ID = values.Value(
        None, environ_name="FACEBOOK_PIXEL_ID", environ_prefix=None
    )

    # Add Google Tag Manager
    GOOGLE_TAG_MANAGER_ID = values.Value(
        None, environ_name="GOOGLE_TAG_MANAGER_ID", environ_prefix=None
    )

    # Add NAU Chatbot Widget
    CHATBOT_WIDGET_JS_URL = values.Value(
        None, environ_name="CHATBOT_WIDGET_JS_URL", environ_prefix=None
    )

    # NAU helpdesk URL.
    HELP_DESK_URL = values.Value(
        None, environ_name="HELP_DESK_URL", environ_prefix=None
    )

    # # Allow to change django language related cookies
    LANGUAGE_COOKIE_DOMAIN = values.Value(
        None, environ_name="LANGUAGE_COOKIE_DOMAIN", environ_prefix=None
    )
    LANGUAGE_COOKIE_NAME = values.Value(
        "django_language", environ_name="LANGUAGE_COOKIE_NAME", environ_prefix=None
    )

    # pylint: disable=invalid-name
    @property
    def ENVIRONMENT(self):
        """Environment in which the application is launched."""
        return self.__class__.__name__.lower()

    # pylint: disable=invalid-name
    @property
    def RELEASE(self):
        """
        Return the release information.

        Delegate to the module function to enable easier testing.
        """
        return get_release()

    # pylint: disable=invalid-name
    @property
    def CMS_CACHE_PREFIX(self):
        """
        Set cache prefix specific to release so existing cache is invalidated for new deployments.
        """
        return f"cms_{get_release():s}_"

    @classmethod
    def post_setup(cls):
        """Post setup configuration.
        This is the place where you can configure settings that require other
        settings to be loaded.
        """
        super().post_setup()

        # The SENTRY_DSN setting should be available to activate sentry for an environment
        if cls.SENTRY_DSN is not None:
            sentry_sdk.init(
                dsn=cls.SENTRY_DSN,
                environment=cls.__name__.lower(),
                release=get_release(),
                integrations=[DjangoIntegration()],
            )
            with sentry_sdk.configure_scope() as scope:
                scope.set_extra("application", "backend")

        # Customize DjangoCMS placeholders configuration
        cls.CMS_PLACEHOLDER_CONF = merge_dict(
            cls.CMS_PLACEHOLDER_CONF, cls.CMS_PLACEHOLDER_CONF_OVERRIDES
        )


class Development(Base):
    """
    Development environment settings

    We set DEBUG to True and configure the server to respond from all hosts.
    """

    DEBUG = True
    ALLOWED_HOSTS = ["*"]

    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

    # Django CMS has cache active by default.
    # On development mode we disable the cache
    CMS_PAGE_CACHE = False
    CMS_PLACEHOLDER_CACHE = False
    CMS_PLUGIN_CACHE = False


class Test(Base):
    """Test environment settings"""

    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


class ContinuousIntegration(Test):
    """
    Continous Integration environment settings

    nota bene: it should inherit from the Test environment.
    """


class Production(Base):
    """Production environment settings

    You must define the DJANGO_ALLOWED_HOSTS environment variable in Production
    configuration (and derived configurations):

    DJANGO_ALLOWED_HOSTS="foo.com,foo.fr"
    """

    # Add this so it is possible to debug other environments
    DEBUG = values.Value(False)

    # Security
    SECRET_KEY = values.SecretValue()
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True

    # For more details about CMS_CACHE_DURATION, see :
    # http://docs.django-cms.org/en/latest/reference/configuration.html#cms-cache-durations
    CMS_CACHE_DURATIONS = values.DictValue(
        {"menus": 3600, "content": 1800, "permissions": 86400}
    )

    # By default, Django CMS sends cached responses with a
    # Cache-control: max-age value that reflects the server cache TTL
    # (CMS_CACHE_DURATIONS["content"])
    #
    # The thing is : we can invalidate a server side cache entry, but we cannot
    # invalidate our client browser cache entries. That's why we want to set a
    # long TTL on the server side, but a much lower TTL on the browser cache.
    #
    # This setting allows to define a maximum value for the max-age header
    # returned by Django CMS views.
    MAX_BROWSER_CACHE_TTL = 600

    # Use AWS S3 for media storage
    DEFAULT_FILE_STORAGE = values.Value("storages.backends.s3boto3.S3Boto3Storage")

    # Preprend all all media file paths on S3 bucket with 'media/'
    AWS_LOCATION = values.Value("media")

    # The normal access and secret key to access an AWS S3
    AWS_ACCESS_KEY_ID = values.SecretValue()
    AWS_SECRET_ACCESS_KEY = values.SecretValue()

    AWS_S3_OBJECT_PARAMETERS = {
        "Expires": "Thu, 31 Dec 2099 20:00:00 GMT",
        "CacheControl": "max-age=94608000",
    }

    AWS_S3_REGION_NAME = values.Value("eu-west-1")

    AWS_STORAGE_BUCKET_NAME = values.Value("production-richie-media")

    # So it is possible to use on-premise Ceph instead of AWS cloud
    AWS_S3_ENDPOINT_URL = values.Value(None)

    # Change AWS S3 domain so we can serve the media from a different domain using a CDN
    AWS_S3_CUSTOM_DOMAIN = values.Value(None)

    # Serve media from the CDN using https
    AWS_S3_URL_PROTOCOL = values.Value("https:")

    # Do not overwrite the files on the media S3 Bucket
    AWS_S3_FILE_OVERWRITE = values.Value(False)

    # CDN domain for static/media urls. It is passed to the frontend to load built chunks
    CDN_DOMAIN = values.Value()

    # Enable the deliver of the static asset files like css, images, fonts, etc.
    # nginx will also deliver this files, but during rolling deploy, the nginx could have one
    # version of the files and the app still running a different version.
    STATIC_FILES_URL_ENABLE = values.BooleanValue(False)
