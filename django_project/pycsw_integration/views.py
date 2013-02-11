import os.path
from ConfigParser import SafeConfigParser

# from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pycsw import server

CONFIGURATION = {
    'server': {
        'home': '.',
        'mimetype': 'application/xml; charset=UTF-8',
        'encoding': 'UTF-8',
        'language': 'en-US',
        'maxrecords': '10',
        'pretty_print': 'true',
        'profiles': 'apiso,dif,fgdc,atom,ebrim',
        # 'loglevel': 'INFO',
        # 'logfile': '/tmp/bla.log'
    },
    'repository': {
        'database': 'postgresql+psycopg2://dodobas:@/sac_new2',
        'mappings': os.path.join(os.path.dirname(__file__), 'mappings.py'),
        'table': 'pycsw_catalogue'
    },
}

CSW = {
    'metadata:main': {
        'identification_title': 'Open Data Catalog CSW',
        'identification_abstract': 'Open Data Catalog is an open data catalog based on Django, Python and PostgreSQL. It was originally developed for OpenDataPhilly.org, a portal that provides access to open data sets, applications, and APIs related to the Philadelphia region. The Open Data Catalog is a generalized version of the original source code with a simple skin. It is intended to display information and links to publicly available data in an easily searchable format. The code also includes options for data owners to submit data for consideration and for registered public users to nominate a type of data they would like to see openly available to the public.',
        'identification_keywords': 'odc,Open Data Catalog,catalog,discovery',
        'identification_keywords_type': 'theme',
        'identification_fees': 'None',
        'identification_accessconstraints': 'None',
        'provider_name': 'a@b.com',
        'provider_url': 'https://github.com/azavea/Open-Data-Catalog',
        'contact_name': 'a@b.com',
        'contact_position': 'a@b.com',
        'contact_address': 'TBA',
        'contact_city': 'City',
        'contact_stateorprovince': 'State',
        'contact_postalcode': '12345',
        'contact_country': 'United States of America',
        'contact_phone': '+01-xxx-xxx-xxxx',
        'contact_fax': '+01-xxx-xxx-xxxx',
        'contact_email': 'a@b.com',
        'contact_url': 'https://github.com/azavea/Open-Data-Catalog/',
        'contact_hours': '0800h - 1600h EST',
        'contact_instructions': 'During hours of service. Off on weekends.',
        'contact_role': 'pointOfContact',
    }
}


@csrf_exempt
def csw(request):
    """CSW WSGI wrapper"""
    # serialize settings.CSW into SafeConfigParser
    # object for interaction with pycsw
    mdict = dict(CSW, **CONFIGURATION)

    # TODO: pass just dict when pycsw supports it
    config = SafeConfigParser()
    for section, options in mdict.iteritems():
        config.add_section(section)
        for k, v in options.iteritems():
            config.set(section, k, v)

    # update server.url
    server_url = '%s://%s%s' % \
        (request.META['wsgi.url_scheme'],
         request.META['HTTP_HOST'],
         request.META['PATH_INFO'])

    config.set('server', 'url', server_url)

    env = request.META.copy()
    env.update({
        'local.app_root': os.path.dirname(__file__),
        'REQUEST_URI': request.build_absolute_uri(),
    })
    csw = server.Csw(config, env)
    content = csw.dispatch_wsgi()
    return HttpResponse(content, content_type=csw.contenttype)
