import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from lazydm.lib.base import BaseController, render

log = logging.getLogger(__name__)

class HomeController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/news.mako')
        # or, return a string
        return render('/index.html')
