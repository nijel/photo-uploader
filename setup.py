#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Photo uploader, setup script.
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__license__ = '''
Copyright © 2007 - 2008 Michal Čihař

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

from distutils.core import setup
import distutils.command.build_scripts
import re
import os
import sys
import phoupl
from stat import ST_MODE

try:
    import pycurl
except ImportError:
    print 'You need PycURL for Photo-Uploader, download it from <http://pycurl.sourceforge.net/>'
    sys.exit(1)

# check if Python is called on the first line with this expression
first_line_re = re.compile('^#!.*python[0-9.]*([ \t].*)?$')

class build_scripts_phoupl(distutils.command.build_scripts.build_scripts, object):
    '''
    This is mostly distutils copy, it just renames script according
    to platform (.py for Windows, without extension for others)
    '''
    def copy_scripts (self):
        """Copy each script listed in 'self.scripts'; if it's marked as a
        Python script in the Unix way (first line matches 'first_line_re',
        ie. starts with "\#!" and contains "python"), then adjust the first
        line to refer to the current Python interpreter as we copy.
        """
        self.mkpath(self.build_dir)
        outfiles = []
        for script in self.scripts:
            adjust = 0
            script = distutils.util.convert_path(script)
            outfile = os.path.join(self.build_dir, os.path.splitext(os.path.basename(script))[0])
            if sys.platform == 'win32':
                outfile += os.extsep + 'py'
            outfiles.append(outfile)

            if not self.force and not distutils.dep_util.newer(script, outfile):
                distutils.log.debug("not copying %s (up-to-date)", script)
                continue

            # Always open the file, but ignore failures in dry-run mode --
            # that way, we'll get accurate feedback if we can read the
            # script.
            try:
                f = open(script, "r")
            except IOError:
                if not self.dry_run:
                    raise
                f = None
            else:
                first_line = f.readline()
                if not first_line:
                    self.warn("%s is an empty file (skipping)" % script)
                    continue

                match = first_line_re.match(first_line)
                if match:
                    adjust = 1
                    post_interp = match.group(1) or ''

            if adjust:
                distutils.log.info("copying and adjusting %s -> %s", script,
                         self.build_dir)
                if not self.dry_run:
                    outf = open(outfile, "w")
                    if not distutils.sysconfig.python_build:
                        outf.write("#!%s%s\n" %
                                   (os.path.normpath(sys.executable),
                                    post_interp))
                    else:
                        outf.write("#!%s%s\n" %
                                   (os.path.join(
                            distutils.sysconfig.get_config_var("BINDIR"),
                            "python" + distutils.sysconfig.get_config_var("EXE")),
                                    post_interp))
                    outf.writelines(f.readlines())
                    outf.close()
                if f:
                    f.close()
            else:
                f.close()
                self.copy_file(script, outfile)

        if os.name == 'posix':
            for file in outfiles:
                if self.dry_run:
                    distutils.log.info("changing mode of %s", file)
                else:
                    oldmode = os.stat(file)[ST_MODE] & 07777
                    newmode = (oldmode | 0555) & 07777
                    if newmode != oldmode:
                        distutils.log.info("changing mode of %s from %o to %o",
                                 file, oldmode, newmode)
                        os.chmod(file, newmode)

    # copy_scripts ()

setup(name = 'photo-uploader',
    version = phoupl.__version__,
    description = 'Simple tool to upload photos to minilab',
    long_description = '',
    author = "Michal Čihař",
    author_email = "michal@cihar.com",
    maintainer = "Michal Čihař",
    maintainer_email = "michal@cihar.com",
    platforms = ['Linux', 'Mac OSX', 'Windows XP/2000/NT', 'Windows 95/98/ME'],
    keywords = ['photo', 'image', 'order', 'print'],
    url = 'http://cihar.com/software/photo-uploader/',
    download_url = 'http://cihar.com/software/photo-uploader/',
    license = 'GPL',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: Microsoft :: Windows :: Windows 95/98/2000',
        'Operating System :: Microsoft :: Windows :: Windows NT/2000',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Natural Language :: English',
    ],
    packages = ['phoupl', 'phoupl.services'],
    scripts = ['photo-upload.py'],
    data_files = [
        (os.path.join('share','man','man1'), ['photo-upload.1'])
        ],
    # Override certain command classes with our own ones
    cmdclass = {
        'build_scripts': build_scripts_phoupl,
        },
    )

# vim: ts=4 sw=4 expandtab
