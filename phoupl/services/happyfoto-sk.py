# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader wrapper for HappyFoto.sk service.
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

class HappyFotoSKService(phoupl.core.PhotoUploader, phoupl.happyfoto.HappyFoto):
    def _connect(self):
        phoupl.happyfoto.HappyFoto.__init__(self, 'happyfoto.sk', 11)
        phoupl.happyfoto.HappyFoto._connect(self)

    def _upload(self, image):
        phoupl.happyfoto.HappyFoto._upload(self, image)

    def get_review_url(self):
        return phoupl.happyfoto.HappyFoto.get_review_url(self)

# Register service
phoupl.register_service(
        'happyfoto.sk',
        HappyFotoSKService,
        'http://happyfoto.sk/',
        ['new'],
        'Happy Foto.sk',
        ['sk'],
        ['svk']
        )
