"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
    always_scan=config['debug'])
    map.minimization = False
    map.explicit = False
    map.append_slash = True
    
    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')
    
    # CUSTOM ROUTES HERE
    map.connect('/', controller='home')
    map.connect('/news/', controller='news')
    #~ map.connect('/about/', controller='about')
    map.connect('/resources/', controller='resources')
    map.connect('/contact/', controller='contact')
    
    map.connect('/news/{news_id:\d+}/', controller='news', action='show_id')
    map.connect('/news/{news_slug:[a-z\-]+}/', controller='news', action='show_slug')
    
    map.connect('/comment/add/{type:(article)}/{id:\d+}/', controller='comments',action='add')
    
    map.connect('/account/{action}/', controller='account')
    map.connect('/login/', controller='account', action='login')
    map.connect('login', '/login/submit/', controller='account', action='login_handler')
    map.connect('/login/continue/', controller='account', action='login')
    map.connect('logout', '/logout/', controller='account', action='logout_handler')
    map.connect('/logout/continue/', controller='account', action='logout')
    
    map.connect('/admin/manage/{type}/', controller='admin', action='manage', id=0)
    map.connect('/admin/manage/{type}/{id:\d+}/', controller='admin', action='manage')
    map.connect('/admin/add_new/article/', controller='admin', action='index')
    map.connect('/admin/add/{type}/', controller='admin', action='add_new')
    
    map.connect('/tools/random/', controller='resources', action='getrandom', conditions=dict(method=['GET']))
    
    #map.connect('/admin/{action}/', controller='admin')

    return map
