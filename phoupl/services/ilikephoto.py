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
        # Init session...
        self.msg('Initialising session...')
        self.get('http://sberna.ilikephoto.cz/')
        self.cookies = self._curl.getinfo(pycurl.INFO_COOKIELIST)
        self.sessionid = self.cookies[0].split('\t')[6]

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
        self.post(
                'http://sberna.ilikephoto.cz/vlozit-fotografie/upload.php?ilikephoto=%s&verze=sberna' % self.sessionid,
                [
                    ('sessionid',  self.sessionid), 
                    ('f1', (pycurl.FORM_FILE, image)), 
                    ('nf1', ''),
                    ('pokracovat', 'some text')
                ])

    def _post_upload(self):
        self.msg('''
You can review them here:
http://sberna.ilikephoto.cz/prehled-vlozenych-fotografii/?ilikephoto=%s
You can finish order here:
http://foto.droxi.cz/termin-zpracovani/?ilikephoto=%s
''' %(self.sessionid, self.sessionid))

    def get_review_url(self):
        return 'http://sberna.ilikephoto.cz/prehled-vlozenych-fotografii/?ilikephoto=%s' % self.sessionid

phoupl.register_service('ilikephoto.cz', ILikePhotoService)