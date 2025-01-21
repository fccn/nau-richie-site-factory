"""
API routes exposed by our base app.
"""

from django.urls import re_path

from .views import redirect_edx_resources

# Support course OpenEdX routes, like the about, course, course mode choose and studio url.
# https://www.ap.nau.edu.pt/courses/course-v1:acme+00001+session01/about
# https://www.ap.nau.edu.pt/courses/course-v1:acme+00001+session01/course/
# https://www.ap.nau.edu.pt/course_modes/choose/course-v1:acme+00001+session01
# https://www.ap.nau.edu.pt/settings/details/course-v1:acme+00001+session01
COURSE_KEY_PATTERN = (
    r"(course-v1:)(?P<organization>.+)(\+)(?P<course>.+)(\+)(?P<session>.+)"
)

# http://open-fun.fr/universities/acme/
ORGANIZATION_KEY_PATTERN = r"(?P<organization>[^\/]*)"

urlpatterns = [
    re_path(
        rf".*/{COURSE_KEY_PATTERN}/?.*",
        redirect_edx_resources,
        name="redirect_edx_courses",
    ),
    re_path(
        rf"redirects/partners/{ORGANIZATION_KEY_PATTERN}/?$",
        redirect_edx_resources,
        name="redirect_edx_courses",
    ),
]
