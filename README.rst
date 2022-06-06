===============
ptpimg_uploader
===============

|PyPI version| |Build Status| 

Upload image file or image URL to the ptpimg.me image hosting.


Installation
------------

Using pip:

.. code-block:: bash

    pip install ptpimg_uploader


Using setup.py:

.. code-block:: bash

    python setup.py install


Manually:

  * Install python3 package ``requests`` (usually ``apt-get install python3-requests`` or ``pip3 install requests``).

  * If you want clipboard support, install ``pyperclip`` too.


API key
-------

To find your PTPImg API key, login to https://ptpimg.me, open the page source
(i.e. "View->Developer->View source" menu in Chrome), find the string api_key
and copy the hexademical string from the value attribute. Your API key should
look like 43fe0fee-f935-4084-8a38-3e632b0be68c.

You can export your ptpimg.me API key (usually in .bashrc or .zshenv) using:

.. code-block:: bash

    export PTPIMG_API_KEY=<your hex key>


or use the ``-k`` / ``--api-key`` command-line switch.

How to use
----------

Run

.. code-block:: bash

    ptpimg_uploader -h


to get command-line help.

To upload an image file:

.. code-block:: bash

    ptpimg_uploader ~/seed/mytorrent/folder.jpg


To rehost an imgur image:

.. code-block:: bash

    ptpimg_uploader https://i.imgur.com/eaT6j3X.jpg


An uploaded URL will be printed to the console.

If ``--bbcode`` parameter is specified, URLS will be wrapped in BBCode ``[img]`` tags:

.. code-block:: bash

    ptpimg_uploader --bbcode ~/seed/mytorrent/folder.jpg


If pyperclip python package is installed, the URL will be additionally copied to the clipboard.
Additionally, you can upload an URL from the clipboard:

.. code-block:: bash

    ptpimg_uploader --clip

If output is a terminal, a bell will be ringed on completion (can be disabled with a ``--nobell`` parameter).

You can specify multiple files and URLs on the command line:

.. code-block:: bash

    ptpimg_uploader ~/seed/mytorrent/folder.jpg https://i.imgur.com/eaT6j3X.jpg


The resulting URLs are printed each on separate line, and copied to your
clipboard with newlines in between.

License
-------

BSD

Acknowledgments
---------------

* mjpieters - a great refactoring and Python packaging
* lukacoufyl - fixing image upload order

.. |Build Status| image:: https://github.com/theirix/ptpimg-uploader/workflows/Upload%20Python%20Package/badge.svg
   :target: https://github.com/theirix/ptpimg-uploader/actions
.. |PyPI version| image:: https://img.shields.io/pypi/v/ptpimg-uploader.svg
   :target: https://pypi.python.org/pypi/ptpimg-uploader
