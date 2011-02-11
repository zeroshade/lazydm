"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
from webhelpers.html.tags import *
from webhelpers.pylonslib.secure_form import secure_form
from webhelpers.html.builder import HTML
from webhelpers.html.converters import format_paragraphs as para
from pylons import url
from datetime import datetime
from pytz import timezone
from repoze.what.plugins.pylonshq import is_met
from repoze.what.predicates import not_anonymous
from lazydm.model.repoze import User

from webhelpers.pylonslib import Flash as _Flash
flash = _Flash()
