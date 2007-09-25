# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader module
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__license__ = '''
Copyright (c) 2003 - 2007 Michal Čihař

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

__version__ = '0.0'
__all__ = [
        'core',
        ]

# Import main module
import core


'''
Dictionary holding all available services.
'''
SERVICE_DB = {}

def register_service(name, handler):
    '''
    Registration handler for adding service.
    '''
    SERVICE_DB[name] = handler

def upload_photos(service, images, debug = False, msgcallback = None):
    '''
    Uploads photos to defined service.
    '''
    service = SERVICE_DB[service](debug, msgcallback)
    service.upload(images)
    return service.get_review_url()


# We register all services here
# TODO: This should load dynamically everything from services
import services.droxi
