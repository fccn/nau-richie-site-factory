"""
NAU i18n override keys.
"""
from django.utils.translation import gettext_lazy as _

def i18n_override_keys():
    # remove footer key phrase because NAU has it on the logo!
    _("Life-changing learning!")
