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

class PtpimgUploader:
    """ Upload image or image URL to the ptpimg.me image hosting """

    def __init__(self):
        # Get api key from env var
        self.api_key = os.getenv('PTPIMG_API_KEY')
        if not self.api_key:
            print('Cannot evaluate PTPIMG_API_KEY env variable')
            exit(1)

    @staticmethod
    def __handle_result(json):
        image_url = 'https://ptpimg.me/{0}.{1}'.format(json[0]['code'], json[0]['ext'])
        print(image_url)
        # Copy to clipboard if possible
        try:
            import pyperclip
            pyperclip.copy(image_url)
        except ImportError:
            print("pyperclip not found. To copy link to cliboard please install it.")

    def __perform(self, data, files):
        # Compose request
        headers = {'referer': 'https://ptpimg.me/index.php'}
        full_data = {'api_key': self.api_key}
        if data:
            full_data.update(data)
        url = 'https://ptpimg.me/upload.php'

        resp = requests.post(url, headers=headers, data=full_data, files=files)
        # pylint: disable=no-member
        if resp.status_code == requests.codes.ok and resp.json():
            #print('Successful response', r.json())
            # r.json() is like this: [{'code': 'ulkm79', 'ext': 'jpg'}]
            self.__handle_result(resp.json())
        else:
            print(('Failed. Status {0}:\n{1}').format(resp.status_code, resp.content))
            exit(1)

    def upload_file(self, filename):
        """ Upload a file using form """
        file_data = open(filename, 'rb')
        if not file_data:
            print('Cannot open file', filename)
            exit(1)

        mimetypes.init()
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type or mime_type.split('/')[0] != 'image':
            print('Unknown image file type', mime_type)
            exit(1)

        self.__perform(None, {'file-upload[0]': (os.path.basename(filename), file_data, mime_type)})

    def upload_url(self, url):
        """ Upload an image URL using form """
        self.__perform({'link-upload': url}, None)


USAGE = 'Usage: {0} filename|url'.format(sys.argv[0])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(USAGE)
        exit(1)

    arg = sys.argv[1]
    if arg and os.path.exists(arg):
        PtpimgUploader().upload_file(arg)
    elif arg and arg[0:4] == 'http':
        PtpimgUploader().upload_url(arg)
    else:
        print(USAGE)
        exit(1)
