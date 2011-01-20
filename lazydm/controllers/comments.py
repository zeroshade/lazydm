import logging
import formencode

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from lazydm.lib.app_globals import Globals

from lazydm.lib.base import BaseController, render
from lazydm.model.article import Article
from lazydm.model.comment import Comment
from lazydm.model.meta import Session

from lazydm.model.forms import CommentForm
from sqlalchemy.orm.exc import NoResultFound
from webhelpers.html.tags import ModelTags

from pylons.decorators import validate
from pylons.decorators.secure import authenticate_form

log = logging.getLogger(__name__)

class CommentsController(BaseController):

    #~ @authenticate_form
    #~ def __before__(self):
		#~ self.query_obj = Session.query(Article)

    def form(self, type, id):
        return type + " " + id

    @authenticate_form
    def add(self, type, id):
        schema = CommentForm()
        query_obj = Session.query(Article)
        try:
            article = query_obj.filter_by(id = id).one()
            if request.params['type'] != type or \
               request.params['article_id'] != str(article.id) or \
               request.params['article_slug'] != article.slug:
                   return "What we have here is a failure to communicate!"
            c.article = article
        except NoResultFound, error:
            return "Failure: %s" % error
        try: 
            form_result = schema.to_python(request.params)
        except formencode.validators.Invalid, error:
            com = Comment(user=error.value['user'], email=error.value['email'],
                          content=error.value['content'], website=error.value['website'])
            if 'partial' in request.params:
                c.form_result = error.value
                c.form_errors = error.error_dict or {}
                c.modelcomment = ModelTags(com)
                return render('/comment-form.html')
            else:
                d = {}
                for key,error in error.error_dict.items():
                    d[key] = error.msg
                session['com_object'] = com
                session['form_errors'] = d
                session.save()
                log.info(session)
                redirect(url(controller='news',action='show_id',news_id=id,anchor='comment-form-section'))
        else:
            Session.add(Comment(user=form_result['user'],email=form_result['email'],
                        website=form_result['website'],content=form_result['content'], article_id=request.params['article_id']))
            Session.commit()
            if 'partial' in request.params:
                c.link_url = url(controller='news',action='show_id',news_id=id,
                                 anchor='comments')
                c.partial_url = url(controller='news',action='show_id',news_id=id,
                                 anchor='comments',partial=1)
                return render('/refresh_comments.html')
            else:
                redirect(url(controller='news',action='show_id',news_id=id,anchor='comments'))
