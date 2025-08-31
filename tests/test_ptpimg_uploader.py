import unittest

from ptpimg_uploader import PtpimgUploader


class PtptimgUploaderCase(unittest.TestCase):
    def test_instantiate(self):
        PtpimgUploader("API_KEY")


if __name__ == "__main__":
    unittest.main()
