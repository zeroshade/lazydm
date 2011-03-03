"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_jinja2 as render

from paste.request import construct_url
from paste.httpexceptions import HTTPMovedPermanently

from lazydm.model.meta import Session

from webhelpers.pylonslib.grid import PylonsObjectGrid
from webhelpers.html.builder import HTML

class CustomObjectGrid(PylonsObjectGrid):
    def default_header_column_format(self, column_number, column_name, header_label):
        return HTML.th(header_label,class_="c%d %s" % (column_number,column_name))

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()
