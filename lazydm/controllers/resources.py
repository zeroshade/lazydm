import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from lazydm.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ResourcesController(BaseController):

    def index(self):
        
        return render('/resources/char_create_index.html');
