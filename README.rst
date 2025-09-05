===============
ptpimg_uploader
===============

.. image:: https://img.shields.io/pypi/v/ptpimg-uploader.svg
   :alt: PyPI version
   :target: https://pypi.python.org/pypi/ptpimg-uploader

.. image:: https://github.com/theirix/ptpimg-uploader/workflows/build/badge.svg
    :alt: Build Status
    :target: https://github.com/theirix/ptpimg-uploader/actions

Upload image file or image URL to the ptpimg.me image hosting.

Features
--------

* Upload local image files
* Rehost images from image services (e.g., from imgur)
* Copy resulting URL to clipboard
* BBCode formatting support
* Command-line and programmatic usage

Installation
------------

Using pip (recommended):

.. code-block:: bash

    pip install ptpimg_uploader

Using setup.py:

.. code-block:: bash

    python setup.py install

Manual Dependencies:

* Required: ``requests`` package
    * Debian/Ubuntu: ``apt-get install python3-requests``
    * Other systems: ``pip3 install requests``

* Optional: ``pyperclip`` package for clipboard support
    * Install via: ``pip3 install pyperclip``

API Key Setup
-------------

1. Login to https://ptpimg.me
2. Open browser developer tools (View -> Developer -> View Source in Chrome)
3. Find ``api_key`` in the page source
4. Copy the hexadecimal string (format: ``xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx``)

Set your API key using either:

Environment variable (recommended):

.. code-block:: bash

    # Add to your ~/.bashrc or ~/.zshenv
    export PTPIMG_API_KEY=your-api-key-here

Or use the command-line option: ``-k`` / ``--api-key``

Usage
-----

Get help:

.. code-block:: bash

    ptpimg_uploader -h

Upload a local image:

.. code-block:: bash

    ptpimg_uploader ~/seed/mytorrent/folder.jpg

Rehost from URL:

.. code-block:: bash

    ptpimg_uploader https://i.imgur.com/eaT6j3X.jpg

Multiple uploads (mix-and-match files and URLs):

.. code-block:: bash

    ptpimg_uploader ~/seed/mytorrent/folder.jpg https://i.imgur.com/eaT6j3X.jpg

Additional command-line options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``--bbcode``: URLs will be wrapped in BBCode ``[img]`` tags

.. code-block:: bash

    ptpimg_uploader --bbcode ~/seed/mytorrent/folder.jpg

* ``--clip``: Place a resulting URL to clipboard (if `pyperclip` package is installed)

.. code-block:: bash

    ptpimg_uploader --clip ~/seed/mytorrent/folder.jpg

* ``--nobell``: Disable completion sound. If output is a terminal, a bell will be ringed on completion.

Programmatic Usage
------------------

The package can be used as a library via the ``upload`` function for programmatic access.

License
-------

BSD

Acknowledgments
---------------

* mjpieters - a great refactoring and Python packaging
* lukacoufyl - fixing image upload order
