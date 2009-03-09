# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader wrapper for HappyFoto.cz service.
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

import phoupl
import phoupl.happyfoto
import pycurl
import re

MATCHER_SHOW = re.compile('<a href="(http://uloz.to/[^"]*)">http://uloz.to/')
MATCHER_SESSION = re.compile('action="/ul/upload.cgi\?tmp_sid=([^"]*)"')

class HappyFotoCZService(phoupl.core.PhotoUploader, phoupl.happyfoto.HappyFoto):
    def _connect(self):
        phoupl.happyfoto.HappyFoto.__init__(self, 'happyfoto.cz', 4)
        phoupl.happyfoto.HappyFoto._connect(self)

    def _upload(self, image):
        phoupl.happyfoto.HappyFoto._upload(self, image)

    def get_review_url(self):
        phoupl.happyfoto.HappyFoto.get_review_url(self)

# Register service
phoupl.register_service(
        'happyfoto.cz',
        HappyFotoCZService,
        'http://happyfoto.cz/',
        ['new'],
        'Happy Foto.cz',
        ['cz'],
        ['cze']
        )
