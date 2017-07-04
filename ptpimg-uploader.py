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


mimetypes.init()


class UploadFailed(Exception):
    def __str__(self):
        msg, *args = self.args
        return msg.format(*args)


class PtpimgUploader:
    """ Upload image or image URL to the ptpimg.me image hosting """

    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def _handle_result(res):
        image_url = 'https://ptpimg.me/{0}.{1}'.format(
            res[0]['code'], res[0]['ext'])
        return image_url

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
                return self._handle_result(resp.json())
            except ValueError as e:
                raise UploadFailed(
                    'Failed decoding body:\n{0}\n{1!r}', e, resp.content
                    ) from None
        else:
            raise UploadFailed(
                'Failed. Status {0}:\n{1}', resp.status_code, resp.content)

    def upload_file(self, filename):
        """ Upload a file using form """
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type or mime_type.split('/')[0] != 'image':
            raise ValueError('Unknown image file type {}'.format(mime_type))

        name = os.path.basename(filename)
        try:
            # until https://github.com/shazow/urllib3/issues/303 is resolved,
            # only use the filename if it is Latin-1 safe
            name.encode('latin1')
        except UnicodeEncodeError:
            name = 'justfilename'
        with open(filename, 'rb') as f:
            return self._perform({'file-upload[0]': (name, f, mime_type)})

    def upload_url(self, url):
        """ Upload an image URL using form """
        return self._perform(**{'link-upload': url})


def upload(api_key, file_or_url):
    if os.path.exists(file_or_url):
        return PtpimgUploader(api_key).upload_file(file_or_url)
    elif file_or_url.startswith('http'):
        return PtpimgUploader(api_key).upload_url(file_or_url)
    else:
        raise ValueError('Not an existing file or image URL: {}'.format(file_or_url))


def main():
    USAGE = 'Usage: {0} filename|url'.format(sys.argv[0])
    if len(sys.argv) != 2:
        print(USAGE)
        sys.exit(1)

    # Get api key from env var
    if 'PTPIMG_API_KEY' not in os.environ:
        print('Cannot evaluate PTPIMG_API_KEY env variable')
        sys.exit(1)

    arg = sys.argv[1]
    try:
        image_url = upload(os.environ['PTPIMG_API_KEY'], arg)
        print(image_url)
        # Copy to clipboard if possible
        try:
            import pyperclip
            pyperclip.copy(image_url)
        except ImportError:
            pass
    except ValueError:
        print(USAGE)
        sys.exit(1)
    except UploadFailed as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
