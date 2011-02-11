from repoze.what.plugins.quickstart import setup_sql_auth
from lazydm.model.meta import Session, Base
from lazydm.model.repoze import User, Group, Permission

def add_auth(app, config):
    """
    Add authentication middleware to app
    We're going to define post-login and post-logout pages
    to do some cool things.

    """
    # we need to provide repoze.what with translations as described here:
    # http://what.repoze.org/docs/plugins/quickstart/
    return setup_sql_auth(app, User, Group, Permission, Session,
                login_url='/login/',
                post_login_url='/login/continue/',
                post_logout_url='/logout/continue/',
                login_handler='/login/submit/',
                logout_handler='/logout/',
                cookie_secret=config.get('cookie_secret'),
                translations={
                    'user_name': 'username',
                    'group_name': 'name',
                    'permission_name': 'name',
                })
