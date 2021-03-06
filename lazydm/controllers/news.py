import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from sqlalchemy.sql.expression import desc

from lazydm.lib.base import BaseController, render
from lazydm.model.article import Article
from lazydm.model.comment import Comment
from lazydm.model.meta import Session

from sqlalchemy.orm import joinedload
from webhelpers.html.tags import ModelTags

log = logging.getLogger(__name__)

class NewsController(BaseController):

    def __before__(self):
        c.comment_type = 'article'
        self.news_q = Session.query(Article).options(joinedload(Article.comments))
        if 'page' in request.params:
            c.page = request.params['page']
        else:
            c.page = 1

    def _comments(self):
        c.CommentPage = c.article.getComments(5,c.page)

    def index(self):
        c.articles = self.news_q.order_by(desc(Article.pub_date)).all()
        return render('/news_index.html')

    def _resolve_page(self):
        self._comments()
        c.comment_id = c.article.id
        c.comment_slug = c.article.slug
        c.modelcomment = ModelTags(None)
        if session.get('form_errors'):
            c.form_errors = session.get('form_errors')
            del session['form_errors']
            c.modelcomment = ModelTags(session.get('com_object'))
            del session['com_object']
            session.save()
        if 'partial' in request.params:
            return render('/comment_list.html')
        else:
            return render('/news.html')
        
    def show_id(self, news_id):
        c.article = self.news_q.filter_by(id=news_id).one()
        if c.article:
            return self._resolve_page()
        abort(404)

    def show_slug(self, news_slug):
        c.article = self.news_q.filter_by(slug=news_slug).one()
        if c.article:
            return self._resolve_page()
        abort(404)
