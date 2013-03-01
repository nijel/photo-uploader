photo-upload command line reference
===================================

.. program:: photo-upload

Synopsis
++++++++


.. code-block:: text

    photo-upload [options] images

Description
+++++++++++

This manual page explains the photo-upload program. This program is simple
uploader of photos to minilab.

Options
+++++++

.. option:: --version

    Show program's version number and exit.

.. option:: -h, --help

    Show help message and exit.

.. option:: --license
    
    Display program license.

.. option:: -s SERVICE_NAME, --service=SERVICE_NAME

    Name of service to use. Use photo-upload -l to list currently 
    available services.

.. option:: -l, --list-services

    List available services.

.. option:: -b, --open-browser

    Open order in browser after uploading.

.. option:: -B, --use-browser

    Define browser to use when opening web page. Default is autodetected by python
    webbrowser. You can also specify any parameter to browser, the URL will be
    just appended to string you enter here and passed to shell.

.. option:: -d, --debug

    Show debugging output. This includes HTML files received from service.

.. option:: -S SESSION, --session=SESSION

    Existing session to reuse (some services won't work
    without existing session).

Examples
++++++++

Uploading all photos from /folder to default service and opening web browser to finish order:

.. code-block:: sh

    photo-upload -b /folder/*.jpg

Adding one image to existing session on ilikephoto.cz service:

.. code-block:: sh

    photo-upload -s ilikephoto.cz -S f1721a19cc3c95218525a8429d48dab2 /tmp/Obraz024.jpg

Listing currently supported services:

.. code-block:: sh

    photo-upload -l

Uploading photo and opening epiphany to finish order:

.. code-block:: sh

    photo-upload -b -B epiphany image.jpg


Files
+++++

``~/.photo-upload``
-------------------

Configuration file where default options are read. This is standard ini like
format file. You can use same values as long options, just specify them in
[photo-upload] section. Some services might also use this config file, check
their documentation for details. Example configuration file:

.. code-block:: ini

	[photo-upload]

	service = droxi.cz

Some services require additional configuration sections, eg. with login names:

.. code-block:: ini

    [happyfoto.cz]
    user = name
    password = passphrase

Some services may require specifying registration code instead of the password:

.. code-block:: ini

    [imageshack.us]
    user = name
    regcode = 575af6686afe6a0c1d

Imageshack also allows you to choose if the image is private or public, defaulting
to private. To change that, specify public = yes under imageshack.us section.


Licence
+++++++

This program is licensed under GNU/GPL version 2.

Bugs
++++

There are definitely many bugs, reporting to author is welcome. Please include
some useful information when sending bug reports (eg. exception you received
and debug output). Please submit your reports to <http://bugs.cihar.com/>.

See also
++++++++
More information is available on program website:
<http://cihar.com/software/photo-uploader/>.

