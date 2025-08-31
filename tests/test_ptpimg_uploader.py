import os
import unittest

import requests_mock

from ptpimg_uploader import NotFoundError, PtpimgUploader, UploadFailed, upload


class PtptimgUploaderCase(unittest.TestCase):

    def setUp(self):
        self.upload_url = "https://ptpimg.me/upload.php"
        self.image_url = "https://acme.org/cat.jpg"
        self.image_path = os.path.join(os.path.dirname(__file__), "test.jpg")

        self.mock = requests_mock.Mocker()
        self.mock.start()

    def tearDown(self):
        self.mock.stop()

    def test_instantiate(self):
        PtpimgUploader("dummykey")

    def test_upload_file_ok(self):
        self.mock.register_uri(
            method="POST",
            url=self.upload_url,
            json=[{"code": "ulkm79", "ext": "jpg"}],
        )
        uploader = PtpimgUploader("dummykey")
        resp = uploader.upload_file(self.image_path)
        self.assertEqual(resp, ["https://ptpimg.me/ulkm79.jpg"])

    def test_upload_file_missing(self):
        self.mock.register_uri(
            method="POST",
            url=self.upload_url,
            json=[{"code": "ulkm79", "ext": "jpg"}],
        )
        uploader = PtpimgUploader("dummykey")
        with self.assertRaises(NotFoundError):
            uploader.upload_file("missing.jpg")

    def test_upload_url_ok(self):
        self.mock.register_uri(
            method="POST",
            url=self.upload_url,
            json=[{"code": "ulkm79", "ext": "jpg"}],
        )
        self.mock.register_uri(
            method="GET",
            url=self.image_url,
            content=b"dummyjpgimage",
            headers={"content-type": "image/jpeg"},
        )
        uploader = PtpimgUploader("dummykey")
        resp = uploader.upload_url(self.image_url)
        self.assertEqual(resp, ["https://ptpimg.me/ulkm79.jpg"])

    def test_upload_url_missing(self):
        self.mock.register_uri(
            method="POST",
            url=self.upload_url,
            json=[{"code": "ulkm79", "ext": "jpg"}],
        )
        self.mock.register_uri(
            method="GET", url=self.image_url, content=b"", status_code=404
        )
        uploader = PtpimgUploader("dummykey")
        with self.assertRaises(NotFoundError):
            uploader.upload_url(self.image_url)

    def test_upload_file_ptpimg_error(self):
        self.mock.register_uri(method="POST", url=self.upload_url, status_code=400)
        uploader = PtpimgUploader("dummykey")
        with self.assertRaises(UploadFailed):
            uploader.upload_file(self.image_path)

    def test_upload_standalone(self):
        self.mock.register_uri(
            method="POST",
            url=self.upload_url,
            json=[{"code": "ulkm79", "ext": "jpg"}],
        )
        self.mock.register_uri(
            method="GET",
            url=self.image_url,
            content=b"dummyjpgimage",
            headers={"content-type": "image/jpeg"},
        )

        results = upload("dummykey", [self.image_path, self.image_url])
        self.assertEqual(results, ["https://ptpimg.me/ulkm79.jpg"] * 2)


if __name__ == "__main__":
    unittest.main()
