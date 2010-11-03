# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4 tw=78:
'''
Photo-Uploader configuration manager.
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

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os

class Config:
    '''
    Configuration handler for photo-uploader. It only wraps ConfigParser to
    make it more convenient to use.
    '''

    def __init__(self, filename, defaults = None):
        '''
        Creates new configuration object, loads config from filename and
        applies defaults.
        '''
        self._config = configparser.ConfigParser()
        self._config.read(os.path.expanduser(filename))
        if defaults is None:
            defaults = {}
        self._defaults = defaults

    def get(self, section, option):
        '''
        Reads string value from configuration, if it is not found, it tries to
        apply defaults, if even this fails, exception is raised.
        '''
        try:
            return self._config.get(section, option)
        except (configparser.NoOptionError, configparser.NoSectionError):
            if section not in self._defaults:
                raise
            if option not in self._defaults[section]:
                raise
            return self._defaults[section][option]

    def getint(self, section, option):
        '''
        Reads integer value from configuration, if it is not found, it tries
        to apply defaults, if even this fails, exception is raised.
        '''
        try:
            return self._config.getint(section, option)
        except (configparser.NoOptionError, configparser.NoSectionError):
            if section not in self._defaults:
                raise
            if option not in self._defaults[section]:
                raise
            return self._defaults[section][option]

    def getbool(self, section, option):
        '''
        Reads boolean value from configuration, if it is not found, it tries
        to apply defaults, if even this fails, exception is raised.
        '''
        try:
            return self._config.getboolean(section, option)
        except (configparser.NoOptionError, configparser.NoSectionError):
            if section not in self._defaults:
                raise
            if option not in self._defaults[section]:
                raise
            return self._defaults[section][option]
