#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Upload image file or image URL to the ptpimg.me image hosting.

Usage:
    python3 ptpimg-uploader.py image-file.jpg
    python3 ptpimg-uploader.py https://i.imgur.com/00000.jpg
"""

import sys
import os
import mimetypes
import requests


try:
    import pyperclip
except ImportError:
    # noop version
    class pyperclip:
        def copy(url): pass


mimetypes.init()


class PtpimgUploader:
    """ Upload image or image URL to the ptpimg.me image hosting """

    def __init__(self):
        # Get api key from env var
        self.api_key = os.getenv('PTPIMG_API_KEY')
        if not self.api_key:
            print('Cannot evaluate PTPIMG_API_KEY env variable')
            sys.exit(1)

    @staticmethod
    def _handle_result(res):
        image_url = 'https://ptpimg.me/{0}.{1}'.format(
            res[0]['code'], res[0]['ext'])
        print(image_url)
        # Copy to clipboard if possible
        pyperclip.copy(image_url)

    def _perform(self, files=None, **data):
        # Compose request
        headers = {'referer': 'https://ptpimg.me/index.php'}
        data['api_key'] = self.api_key
        url = 'https://ptpimg.me/upload.php'

        resp = requests.post(url, headers=headers, data=data, files=files)
        # pylint: disable=no-member
        if resp.status_code == requests.codes.ok:
            try:
                # print('Successful response', r.json())
                # r.json() is like this: [{'code': 'ulkm79', 'ext': 'jpg'}]
                self._handle_result(resp.json())
            except ValueError as e:
                print('Failed decoding body:\n{0}\n{1!r}'.format(
                    e, resp.content))
        else:
            print('Failed. Status {0}:\n{1}'.format(
                resp.status_code, resp.content))
            sys.exit(1)

    def upload_file(self, filename):
        """ Upload a file using form """
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type or mime_type.split('/')[0] != 'image':
            print('Unknown image file type', mime_type)
            sys.exit(1)

        name = os.path.basename(filename)
        try:
            # until https://github.com/shazow/urllib3/issues/303 is resolved,
            # only use the filename if it is Latin-1 safe
            name.encode('latin1')
        except UnicodeEncodeError:
            name = 'justfilename'
        with open(filename, 'rb') as f:
            self._perform({'file-upload[0]': (name, f, mime_type)})

    def upload_url(self, url):
        """ Upload an image URL using form """
        self._perform(**{'link-upload': url})


USAGE = 'Usage: {0} filename|url'.format(sys.argv[0])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(USAGE)
        sys.exit(1)

    arg = sys.argv[1]
    if os.path.exists(arg):
        PtpimgUploader().upload_file(arg)
    elif arg.startswith('http'):
        PtpimgUploader().upload_url(arg)
    else:
        print(USAGE)
        sys.exit(1)
