"""Setup the lazydm application"""
import logging

import pylons.test

from lazydm.config.environment import load_environment
from lazydm.model.meta import Session, Base
from lazydm.model.article import Article
from lazydm.model.comment import Comment
from lazydm.model.repoze import User, Group, Permission
from lazydm.model.book import Book
from lazydm.model.race import Race

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup lazydm here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    log.info("Creating tables....")
    Base.metadata.create_all(bind=Session.bind)
    log.info("Success!!")

    log.info("Adding initial users, groups and permissions...")
    g = Group()
    g.name = u'admin'
    Session.add(g)

    p = Permission()
    p.name = u'admin'
    p.groups.append(g)
    Session.add(p)

    u = User()
    u.username = u'admin'
    u.fullname = u'admin'
    u._set_password('zero')
    u.email = u'admin@example.com'
    u.groups.append(g)
    Session.add(u)

    u = User()
    u.username = u'test'
    u.fullname = u'Zero'
    u._set_password('test')
    u.email = u'test@example.com'
    Session.add(u)
    Session.commit()
    
    log.info("Adding Data...")
    con = u'<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diamvoluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diamvoluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diamvoluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna</p>\n\n'
    con += u'<img src="/img/flower.png" />\n\n'
    con += u'<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diamvoluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diamvoluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diamvoluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna</p>\n\n'
    con += u'<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diamvoluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diamvoluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diamvoluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna</p>'

    Session.add(Article(author_id=u.id,title=u'Testing This Post',slug=u'testing-this-post',
                        content=con))

    content = u'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diamvoluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diamvoluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diamvoluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumyeirmod tempor invidunt ut labore et dolore magna'
    Session.add(Comment(user=u'Benjamin Franklin', email=u'zotthewizard@gmail.com', content=content, article_id=1,type='article',ip_addr='192.168.1.1'))
    Session.add(Comment(user=u'George Washington', email=u'wtf@gmail.com', content=content, article_id=1,type='article',ip_addr='192.168.1.1'))
    Session.commit()
    
    b = Book(title="Player's Handbook")
    Session.add(b)
    Session.commit()
    
    r = Race()
    r.name = 'Elf'
    r._dex = 2
    r._con = -2
    r.book = b
    r.male_ft = 4
    r.female_ft = 4
    r.male_in = 5
    r.female_in = 5
    r.male_lb = 85
    r.female_lb = 80
    r.height_mod = "2d6"
    r.weight_mod = "1d6"
    
    Session.add(r)
    Session.commit()
    
    log.info("Success!!")
