import sys
import os

ROOT_PROJECT_FOLDER = os.path.dirname(__file__)
path1 = os.path.abspath(os.path.join(ROOT_PROJECT_FOLDER,'..','..','sac_catalogue'))
sys.path.append( path1 )

# for debugging
myFile = file("/tmp/paths.log","wt")
myFile.write("Root: %s\n" % ROOT_PROJECT_FOLDER)
myFile.write("PATH1: %s\n" % path1)
import settings
myFile.write("User: %s\n" % settings.DATABASES)
myFile.close()
#end debugging

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
