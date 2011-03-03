import logging
import formencode

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from lazydm.lib.helpers import flash
from lazydm.lib.base import BaseController, render
from lazydm.lib.filters import slugify
from repoze.what.predicates import not_anonymous, has_permission
from repoze.what.plugins.pylonshq import ControllerProtector

from pylons.decorators.secure import authenticate_form
from lazydm.model.forms import ArticleForm
from lazydm.model.article import Article
from lazydm.model.repoze import User
from lazydm.model.meta import Session
from sqlalchemy.sql.expression import desc

from webhelpers.html.builder import HTML
from webhelpers.html.tags import ModelTags

log = logging.getLogger(__name__)

@ControllerProtector(has_permission('admin',msg="You must be an admin to access this page"),"denial_handler")
class AdminController(BaseController):
    
    @staticmethod
    def denial_handler(reason):
        log.info("Testing: " + str(response.status_int))
        if response.status_int == 403:
            abort(response.status_int,detail=reason)
        else:
            flash(reason,"error")
    
    def manage(self,type,id):
        if type == 'article':
            c.articles = Session.query(Article).order_by(desc(Article.pub_date)).all()
            return render('/admin/manage_news.html')
        elif type == 'comments':
            c.article = Session.query(Article).filter_by(id=id).order_by(desc(Article.pub_date)).one()
            return render('/admin/manage_comments.html')
            
    def index(self):
        c.articleModel = ModelTags(None)
        if session.get('form_errors'):
            c.form_errors = session.get('form_errors')
            del session['form_errors']
            c.articleModel = ModelTags(session.get('new_article'))
            del session['new_article']
            session.save()
        return render('/admin/post_news.html')

    def __new_article(self):
        schema = ArticleForm()
        try: 
            form_result = schema.to_python(request.params)
        except formencode.validators.Invalid, error:
            article = Article(title=error.value['title'],content=error.value['content'])
            d = {}
            for key,error in error.error_dict.items():
                d[key] = error.msg
            session['new_article'] = article
            session['form_errors'] = d
            session.save()
#           log.info(session)
            redirect(url(controller='admin',action='index'))
        else:
            article = Article(title=form_result['title'],content=form_result['content'],
                              author_id=User.getCurrent().id,slug=slugify(form_result['title']))
            Session.add(article)
            Session.commit()
            return "Article Posted!"

    @authenticate_form
    def add_new(self, type):
        if type == "article":
            return self.__new_article()
