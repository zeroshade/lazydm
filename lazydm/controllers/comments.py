import logging
import formencode

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from lazydm.lib.base import BaseController, render
from lazydm.model.article import Article
from lazydm.model.comment import Comment
from lazydm.model.meta import Session

from lazydm.model.forms import CommentForm
from sqlalchemy.orm.exc import NoResultFound
from webhelpers.html.tags import ModelTags

from pylons.decorators.secure import authenticate_form

log = logging.getLogger(__name__)

class CommentsController(BaseController):

    #~ @authenticate_form
    #~ def __before__(self):
		#~ self.query_obj = Session.query(Article)

    def form(self, type, id):
        return type + " " + id

    def __validate_obj(self, type, id):
        if type == 'article':
            return self.__validate_article(type,id)

    def __validate_article(self, type, id):
        query_obj = Session.query(Article)
        try:
            article = query_obj.filter_by(id = id).one()
            if request.params['type'] != type or \
               request.params['com_id'] != str(article.id) or \
               request.params['com_slug'] != article.slug:
                   return "What we have here is a failure to communicate!"
            c.article = article
            c.comment_id = c.article.id
            c.comment_slug = c.article.slug
        except NoResultFound, error:
            return error
        else:
            return False

    def __com_url(self, type, id, anchor, partial=False):
        arglist = {}
        if partial:
            arglist['partial'] = 1
        if type == 'article':
            return url(controller='news',action='show_id',
                                 news_id=id,anchor=anchor, **arglist)

    @authenticate_form
    def add(self, type, id):
        schema = CommentForm()
        ret = self.__validate_obj(type, id)
        if ret:
            return "Failure %s" % ret
            
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
#                log.info(session)
                redirect(self.__com_url(type, id, 'comment-form-section'))
        else:
            com = Comment(user=form_result['user'],email=form_result['email'],
                        website=form_result['website'],content=form_result['content'], 
                        type=type,ip_addr=request.environ.get('REMOTE_ADDR'))
            if type == 'article':
                com.article_id = id
            Session.add(com)
            Session.commit()
            
            anchor = 'comments'
            if 'partial' in request.params:
                c.link_url = self.__com_url(type, id, anchor)
                c.partial_url = self.__com_url(type, id, anchor, True)
                return render('/refresh_comments.html')
            else:
                redirect(self.__com_url(type, id, anchor))

