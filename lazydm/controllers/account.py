import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from lazydm.lib.helpers import flash
from lazydm.lib.base import BaseController, render
from repoze.what.predicates import not_anonymous, has_permission
from repoze.what.plugins.pylonshq import ActionProtector

from lazydm.model.repoze import User

log = logging.getLogger(__name__)

class AccountController(BaseController):

    def login(self):
        """
        This is where the login form will be rendered
        The login counter will tell if the user has tried to login
        with the wrong credentials
        """
        identity = request.environ.get('repoze.who.identity')
        came_from = str(request.GET.get('came_from', '')) or \
                    url(controller='account', action='welcome')
        if identity:
            redirect(url(came_from))
        else:
            c.came_from = came_from
            c.login_counter = request.environ['repoze.who.logins'] + 1
            if c.login_counter > 1:
                flash('Incorrect Username or Password','error')
            return render('/login.html')
    
    def logout(self):
        came_from = str(request.GET.get('came_from', '')) or \
                    url(controller='home', action='index')
        redirect(url(came_from))
    
    @ActionProtector(not_anonymous())
    def welcome(self):
        """
        Greet the user if she logged in successfully or redirect back
        to the login form otherwise(using ActionProtector decorator).
        """
        identity = request.environ.get('repoze.who.identity')
        return 'Welcome back %s' % identity['repoze.who.userid']

    @ActionProtector(not_anonymous())
    def test_user_access(self):
        return User.get(request.environ['repoze.what.credentials']['repoze.what.userid']).fullname

    @ActionProtector(has_permission('admin'))
    def test_admin_access(self):
        return 'You are inside admin section'
