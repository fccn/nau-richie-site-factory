"""
Chatbot widget context processor
"""
from django.conf import settings
from django.utils.translation import get_language_from_request

from richie.apps.courses.models import Organization


def chatbot_widget_js_url_setting(request):
    """
    Chatbot widget context processor
    """
    context = {}
    if hasattr(settings, "CHATBOT_WIDGET_JS_URL"):
        context["CHATBOT_WIDGET_JS_URL"] = getattr(settings, "CHATBOT_WIDGET_JS_URL")
        chatbot_param_course = ""
        if hasattr(request, "current_page"):
            page = request.current_page or None
            language = get_language_from_request(request, check_path=True)
            if page:
                organizations_codes = Organization.get_organizations_codes(
                    page, language
                )
                if len(organizations_codes) > 0:
                    org_code = organizations_codes[0]
                else:
                    org_code = ""

                course = getattr(page, "course", None)
                course_code = getattr(course, "code", None)

                if org_code and course_code:
                    page_title = page.get_title()
                    chatbot_param_course = f"{page_title}-{org_code}-{course_code}"

        context["CHATBOT_PARAM_COURSE"] = chatbot_param_course
    return context
