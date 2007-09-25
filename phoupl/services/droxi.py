# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo-Uploader wrapper for Droxi service.
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

class DroxiService(phoupl.core.PhotoUploader):
    def _connect(self):
        # Use preseeded session
        if self._session is not None:
            self.msg('Reusing session %s' % self._session)
            return

        # Init session...
        self.msg('Initialising session...')
        self.get('http://foto.droxi.cz/')
        self.cookies = self._curl.getinfo(pycurl.INFO_COOKIELIST)
        self._session = self.cookies[0].split('\t')[6]
        self.msg('Created session %s' % self._session)

        # Select photo and not photoalbum...
        self.msg('Selecting photo order...')
        self.post('http://foto.droxi.cz/index.php',
                [
                    ('scripttest', '0'), 
                    ('vyber', 'fotka')
                ])

        # Select fast/cheaper/simple order...
        self.msg('Selecting fast/cheaper/simple order...')
        self.post('http://foto.droxi.cz/typ-zakazky/index.php',
                [
                    ('krok_zpet', '4'), 
                    ('set_ordertype', 'disc'), 
                    ('pokracovat', 'some text')
                ])

    def _upload(self, image):
        self.post(
                'http://foto.droxi.cz/vlozit-fotografie/upload.php?ilikephoto=%s&verze=droxi' % self._session,
                [
                    ('sessionid',  self._session), 
                    ('f1', (pycurl.FORM_FILE, image)), 
                    ('nf1', ''),
                    ('pokracovat', 'some text')
                ])

    def _post_upload(self):
        self.msg('''
You can review them here:
http://foto.droxi.cz/prehled-vlozenych-fotografii/?ilikephoto=%s
You can finish order here:
http://foto.droxi.cz/format-fotografii/?ilikephoto=%s
''' %(self._session, self._session))

    def get_review_url(self):
        return 'http://foto.droxi.cz/prehled-vlozenych-fotografii/?ilikephoto=%s' % self._session

phoupl.register_service('droxi.cz', DroxiService)
