#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
Upload image file or image URL to the ptpimg.me image hosting.

Usage:
    python3 ptpimg-uploader.py image-file.jpg
    python3 ptpimg-uploader.py https://i.imgur.com/00000.jpg
    python3 ptpimg-uploader.py --clip
"""

import contextlib
import mimetypes
import os
from io import BytesIO
from sys import stdout

import requests

mimetypes.init()


class UploadFailed(Exception):
    def __str__(self):
        msg, *args = self.args
        return msg.format(*args)


class PtpimgUploader:
    """ Upload image or image URL to the ptpimg.me image hosting """

    def __init__(self, api_key, timeout=None):
        self.api_key = api_key
        self.timeout = timeout

    @staticmethod
    def _handle_result(res):
        image_url = 'https://ptpimg.me/{0}.{1}'.format(
            res['code'], res['ext'])
        return image_url

    def _perform(self, resp):
        if resp.status_code == requests.codes.ok:
            try:
                # print('Successful response', r.json())
                # r.json() is like this: [{'code': 'ulkm79', 'ext': 'jpg'}]
                return [self._handle_result(r) for r in resp.json()]
            except ValueError as e:
                raise UploadFailed(
                    'Failed decoding body:\n{0}\n{1!r}', e, resp.content
                ) from None
        else:
            raise UploadFailed(
                'Failed. Status {0}:\n{1}', resp.status_code, resp.content)

    def _send_upload(self, files: dict):
        headers = {'referer': 'https://ptpimg.me/index.php'}
        data = {'api_key': self.api_key}
        service_url = 'https://ptpimg.me/upload.php'
        return requests.post(service_url, headers=headers, data=data, files=files)

    def upload_file(self, filename):
        """ Upload file using form """
        # The ExitStack closes files for us when the with block exits
        with contextlib.ExitStack() as stack:
            open_file = stack.enter_context(open(filename, 'rb'))
            mime_type, _ = mimetypes.guess_type(filename)
            if not mime_type or mime_type.split('/')[0] != 'image':
                raise ValueError(
                    'Unknown image file type {}'.format(mime_type))

            name = os.path.basename(filename)
            try:
                # until https://github.com/shazow/urllib3/issues/303 is
                # resolved, only use the filename if it is Latin-1 safe
                e_name = name.encode('latin-1', 'replace')
                name = e_name.decode('latin-1')
            except UnicodeEncodeError:
                name = 'justfilename'

            files = {'file-upload[]': (
                name, open_file, mime_type)}
            resp = self._send_upload(files=files)

        return self._perform(resp)

    def upload_url(self, url):
        """ Upload image URL """
        with contextlib.ExitStack() as stack:
            resp = requests.get(url, timeout=self.timeout)
            if resp.status_code != requests.codes.ok:
                raise ValueError(
                    'Cannot fetch url {} with error {}'.format(url, resp.status_code))

            mime_type = resp.headers['content-type']
            if not mime_type or mime_type.split('/')[0] != 'image':
                raise ValueError(
                    'Unknown image file type {}'.format(mime_type))

            open_file = stack.enter_context(BytesIO(resp.content))

            files = {'file-upload[]': (
                'justfilename', open_file, mime_type)}
            resp = self._send_upload(files)

            return self._perform(resp)


def _partition(files_or_urls):
    file_url_list = []
    for file_or_url in files_or_urls:
        if os.path.exists(file_or_url):
            file_url_list.append({'type': 'file',
                                  'path': file_or_url})
        elif file_or_url.startswith('http'):
            file_url_list.append({'type': 'url',
                                  'path': file_or_url})
        else:
            raise ValueError(
                'Not an existing file or image URL: {}'.format(file_or_url))
    return file_url_list


def upload(api_key, files_or_urls, timeout=None):
    uploader = PtpimgUploader(api_key, timeout)
    file_url_list = _partition(files_or_urls)
    results = []
    if file_url_list:
        for file_or_url in file_url_list:
            if file_or_url['type'] == 'file':
                results += uploader.upload_file(file_or_url['path'])
            elif file_or_url['type'] == 'url':
                results += uploader.upload_url(file_or_url['path'])
    return results


def main():
    import argparse
    import sys

    try:
        import pyperclip
    except ImportError:
        pyperclip = None

    nargs = "+"
    if "--clip" in sys.argv and pyperclip:
        nargs = "*"

    parser = argparse.ArgumentParser(description="PTPImg uploader")
    parser.add_argument('images', metavar='filename|url', nargs=nargs)
    parser.add_argument(
        '-k', '--api-key', default=os.environ.get('PTPIMG_API_KEY'),
        help='PTPImg API key (or set the PTPIMG_API_KEY environment variable)')
    if pyperclip is not None:
        parser.add_argument(
            '-n', '--dont-copy', action='store_false', default=True,
            dest='clipboard',
            help='Do not copy the resulting URLs to the clipboard')
        parser.add_argument(
            '--clip', action='store_true', default=False,
            help='copy from image from clipboard. Image can either ' +
                 'be a path to the image, a url to the image')
    parser.add_argument(
        '-b', '--bbcode', action='store_true', default=False,
        help='Output links in BBCode format (with [img] tags)')
    parser.add_argument(
        '--nobell', action='store_true', default=False,
        help='Do not bell in a terminal on completion')

    args = parser.parse_args()
    images = args.images
    if pyperclip is not None and args.clip:
        images.append(pyperclip.paste())

    if not args.api_key:
        parser.error('Please specify an API key')
    try:
        image_urls = upload(args.api_key, images)
        if args.bbcode:
            printed_urls = ['[img]{}[/img]'.format(image_url) for image_url in image_urls]
        else:
            printed_urls = image_urls
        print(*printed_urls, sep='\n')
        # Copy to clipboard if possible
        if getattr(args, 'clipboard', False):
            pyperclip.copy('\n'.join(image_urls))
        # Ring a terminal if we are in terminal and allowed to do this
        if not args.nobell and stdout.isatty():
            stdout.write('\a')
            stdout.flush()
    except (UploadFailed, ValueError) as e:
        parser.error(str(e))


if __name__ == '__main__':
    main()
