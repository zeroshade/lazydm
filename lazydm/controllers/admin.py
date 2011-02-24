import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from lazydm.lib.helpers import flash
from lazydm.lib.base import BaseController, render
from repoze.what.predicates import not_anonymous, has_permission
from repoze.what.plugins.pylonshq import ControllerProtector

log = logging.getLogger(__name__)

@ControllerProtector(has_permission('admin',\
                    msg="You must be an admin to access this page"),"denial_handler")
class AdminController(BaseController):
    
    @staticmethod
    def denial_handler(reason):
        log.info("Testing: " + str(response.status_int))
        if response.status_int == 403:
            abort(response.status_int,detail=reason)
        else:
            flash(reason,"error")
            
    
    def index(self):
        # Return a rendered template
        #return render('/admin.mako')
        # or, return a string
        return render('/admin/post_news.html')
