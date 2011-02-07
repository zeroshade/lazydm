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
                login_url='/account/login/',
                post_login_url='/account/login/',
                post_logout_url='/',
                login_handler='/account/login_handler/',
                logout_handler='/account/logout/',
                cookie_secret=config.get('cookie_secret'),
                translations={
                    'user_name': 'username',
                    'group_name': 'name',
                    'permission_name': 'name',
                })
