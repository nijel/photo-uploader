# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader module
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__license__ = '''
Copyright © 2007 Michal Čihař

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

__version__ = '0.2'

# Import main module
import core


'''
Dictionary holding all available services.
'''
SERVICE_DB = {}

def register_service(name, handler, url, features):
    '''
    Registration handler for adding service.
    '''
    SERVICE_DB[name] = {
            'Class': handler,
            'URL': url,
            'Features': features,
            }


def list_services():
    '''
    Returns list of available services.
    '''
    return SERVICE_DB.keys()

def get_service_info(name):
    '''
    Returns information about service.
    '''
    return {
            'URL' : SERVICE_DB[name]['URL'],
            'Features' : SERVICE_DB[name]['Features'],
            }

def upload_photos(service, images, debug = False, msgcallback = None, session = None):
    '''
    Uploads photos to defined service.
    '''
    service = SERVICE_DB[service]['Class'](debug, msgcallback, session)
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
