# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader wrapper for ilikePhoto service.
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

import phoupl
import pycurl

class ILikePhotoService(phoupl.core.PhotoUploader):
    def _connect(self):
        if self._session is None:
            raise Exception("Need created session, please go to http://sberna.ilikephoto.cz/ and obtain one!")
        self.msg('Reusing session %s' % self._session)

    def _upload(self, image):
        self.post(
                'http://sberna.ilikephoto.cz/vlozit-fotografie/upload.php?ilikephoto=%s&verze=sberna' % self._session,
                [
                    ('sessionid',  self._session), 
                    ('f1', (pycurl.FORM_FILE, image)), 
                    ('nf1', ''),
                    ('pokracovat', 'some text')
                ])

    def _post_upload(self):
        self.msg('''
You can review them here:
http://sberna.ilikephoto.cz/prehled-vlozenych-fotografii/?ilikephoto=%s
You can finish order here:
http://sberna.ilikephoto.cz/termin-zpracovani/?ilikephoto=%s
''' %(self._session, self._session))

    def get_review_url(self):
        return 'http://sberna.ilikephoto.cz/prehled-vlozenych-fotografii/?ilikephoto=%s' % self._session

phoupl.register_service('ilikephoto.cz', ILikePhotoService)
