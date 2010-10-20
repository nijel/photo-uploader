# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader wrapper for ilikePhoto service.
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__license__ = '''
Copyright © 2007 - 2010 Michal Čihař

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
import phoupl.ilikephoto
import pycurl

class ILikePhotoService(phoupl.core.PhotoUploader, phoupl.ilikephoto.ILikePhoto):
    def _connect(self):
        phoupl.ilikephoto.ILikePhoto.__init__(self, 'http://sberna.ilikephoto.cz', 'sberna')
        # Use preseeded session
        if self._session is not None:
            self.msg('Reusing session %s' % self._session)
            return

        # Init session...
        self.ipl_init_session()

        self.msg('Entering service...')
        self.post('http://sberna.ilikephoto.cz/',
                [
                    ('vstup', 'fotka')
                ])

        self.msg('Confirming conditions...')
        self.post('http://sberna.ilikephoto.cz/vstup-do-fotosberny/index.php',
                [
                    ('souhlasim', 'ano'),
                ])

    def _upload(self, image):
        self.ipl_upload(image)

    def _post_upload(self):
        self.ipl_post_upload()

    def get_review_url(self):
        return self.ipl_get_review_url()

# Register service
phoupl.register_service(
        'ilikephoto.cz',
        ILikePhotoService,
        'http://sberna.ilikephoto.cz/',
        ['new', 'reuse', 'cookie'],
        'ilikePHOTO',
        ['cz'],
        ['cze']
        )
