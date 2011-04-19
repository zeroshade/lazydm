import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from sqlalchemy.sql.expression import desc

from lazydm.lib.base import BaseController, render
from randomdotorg import RandomDotOrg as RDO
from lazydm.model.meta import Session
from lazydm.model.race import Race
import json

log = logging.getLogger(__name__)

class raceEncode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Race):
            return { 
                    'name' : obj.name, 
                    'stat_mods' : obj.stats(), 
                    'book' : { 
                                'title' : obj.book.title,
                                'id' : obj.book.id
                             },
                    'personal' : obj.personal()
                    }
        else:
            return json.JSONEncoder.default(self,obj)

class ResourcesController(BaseController):

    def getrandom(self):
        if not 'sides' in request.GET or not 'num' in request.GET:
            abort(500)
        sides = (int)(request.GET['sides'])
        num = (int)(request.GET['num'])
        r = RDO()
        return json.dumps(r.randrange(1,sides,1,num))

    def index(self):
        c.races = Session.query(Race).order_by(desc(Race.id)).all()
        tmp = {}
        for r in c.races:
            tmp[r.id] = r
        c.jsonrace = json.dumps(tmp, cls=raceEncode)
        return render('/resources/char_create_index.html');
