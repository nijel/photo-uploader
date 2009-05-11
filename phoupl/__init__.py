# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader module
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__license__ = '''
Copyright © 2007 - 2009 Michal Čihař

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License version 2 as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

__version__ = '0.8'

# Import main module
import core
import config

# Import other required modules
import copy


SERVICE_DB = {}
'''
Dictionary holding all available services.
'''

def register_service(name,
        handler,
        url = '',
        features = None,
        fullname = None,
        countries = None,
        languages = None,
        servicetype = 'digilab'
        ):
    '''
    Registration handler for adding service.

    Parameters handler, url and features should be allways filled, rest
    is optional.

    @param handler: Class to handle uploads.
    @type handler: Class

    @param url: URL with service information.
    @type URL: string

    @param features: Features supported by service, check README for
    their listing.
    @type features: list of strings

    @param fullname: Printable name of service. This should be unique
    among all services in one country.
    @type fullname: string

    @param countries: List of countries where service is available as
    ISO 3166 codes.
    @type countries: list of strings

    @param languages: List od languages as ISO 639-2 language codes
    supported by service.
    @type languages: list of strings

    @param servicetype: Type of service
    @type servicetype: string, currently one of digilab, storage
    '''
    if features is None:
        features = []
    SERVICE_DB[name] = {
            'Class': handler,
            'URL': url,
            'Features': features,
            }
    if fullname is not None:
        SERVICE_DB[name]['FullName'] = fullname
    if countries is not None:
        SERVICE_DB[name]['Countries'] = countries
    if languages is not None:
        SERVICE_DB[name]['Languages'] = languages
    SERVICE_DB[name]['Type'] = servicetype

def list_services():
    '''
    Returns list of available services.
    '''
    return SERVICE_DB.keys()

def get_service_info(name):
    '''
    Returns information about service.

    @param name: Name of service.
    @type name: string
    '''
    result = copy.deepcopy(SERVICE_DB[name])
    del result['Class']
    return result

def upload_photos(service, images, debug = False,
        msgcallback = None, session = None, configstorage = None):
    '''
    Uploads photos to defined service.
    '''
    service = SERVICE_DB[service]['Class'](
        debug,
        msgcallback,
        session,
        configstorage)
    service.upload(images)
    return service.get_review_url()

import os

SERVICES_DIR = './services'
SERVICES_ABS_DIR = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            SERVICES_DIR))

# We register all services here
for filename in os.listdir(SERVICES_ABS_DIR):
    module_name, ext = os.path.splitext(filename)
    if ext == '.py' and module_name != '__init__':
        __import__('phoupl.services.%s' % module_name)
