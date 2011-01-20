import sys, os
INTERP = "/home/lazydm/local/bin/python"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)
os.environ['PYTHON_EGG_CACHE'] = '/home/lazydm/eggs'
sys.path.append(os.getcwd())
sys.path.append("/home/lazydm/lazydm")
from paste.deploy import loadapp

from paste.exceptions.errormiddleware import ErrorMiddleware

#def application(environ, start_response):
#    environ['SCRIPT_NAME'] = environ['PATH_INFO']
#    application = loadapp('config:/home/lazydm/lazydm/development.ini')
#    return application(environ, start_response)

application = loadapp('config:/home/lazydm/lazydm/development.ini')
application = ErrorMiddleware(application, debug=True)
