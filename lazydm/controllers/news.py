import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from lazydm.lib.app_globals import Globals

from lazydm.lib.base import BaseController, render
from lazydm.model.article import Article
from lazydm.model.comment import Comment
from lazydm.model.meta import Session

from sqlalchemy.orm import eagerload
from webhelpers.html.tags import ModelTags

log = logging.getLogger(__name__)

class NewsController(BaseController):

    def __before__(self):
        self.news_q = Session.query(Article)

    def index(self):
        # Return a rendered template
        #return render('/news.mako')
        # or, return a string
        c.article = self.news_q.order_by(Article.pub_date).first()
        return render('/index.html')

    def show_id(self, news_id):
        c.modelcomment = ModelTags(None)
        c.article = self.news_q.options(eagerload('comments')).filter_by(id=news_id).one()
        if c.article:
            return render('/news.html')
        abort(404)

    def show_slug(self, news_slug):
        c.article = self.news_q.filter_by(slug=news_slug).one()
        if c.article:
            return render('/news.html')
        abort(404)
