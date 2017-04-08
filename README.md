# ptpimg-uploader

Upload image file or image URL to the ptpimg.me image hosting.

## Installation

1. Install python3 package requests (usually apt-get install python3-requests or pip3 install requests).

2. Export your ptpimg.me API key (usually in .bashrc or .zshenv):

    export PTPIMG_API_KEY=<your hex key>

## How to use:

To upload an image file:

    python3 ptpimg-uploader.py ~/seed/mytorrent/folder.jpg

To rehost an imgur image:

    python3 ptpimg-uploader.py https://i.imgur.com/eaT6j3X.jpg

An uploaded URL will be printed to the console.
If pyperclip python package is installed, the URL will be additionally copied to the clipboard.
