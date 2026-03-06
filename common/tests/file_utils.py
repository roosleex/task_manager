from django.test import SimpleTestCase, RequestFactory
from ..file_utils import *
from datetime import date
from ..date_utils import conv_yyyymmdd_to_datetime



class FileUtilsTests(SimpleTestCase):
    def setUp(self):
        self.req_factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        pass

    def test_get_file_export_response(self):
        # TODO
        pass

    def test_get_image_path(self):
        path = "uploads/admin/cemetery_name/"
        actual = get_image_path(path, 0)
        expected = path + "%Y/%m/%d/"
        self.assertEqual(actual, expected)

        actual = get_image_path(path, 1)
        d = date.today()
        expected = path + str(d.year) + "/" + '{:02d}'.format(d.month) + "/" + '{:02d}'.format(d.day) + "/"
        self.assertEqual(actual, expected)

        d = conv_yyyymmdd_to_datetime("2024-01-02")
        actual = get_image_path(path, 2, d)
        expected = path + "2024/01/02/"
        self.assertEqual(actual, expected)

    def test_get_file_uniq_name(self):
        actual = get_file_uniq_name("txt")
        print(actual.split(".")[-1])
        self.assertTrue(actual != "")
        self.assertTrue(len(actual) > 30)
        self.assertEqual(actual.split(".")[-1], "txt")

        actual = get_file_uniq_name("jpg")
        self.assertTrue(actual != "")
        self.assertTrue(len(actual) > 30)
        self.assertEqual(actual.split(".")[-1], "jpg")

        actual = get_file_uniq_name("jpeg")
        self.assertTrue(actual != "")
        self.assertTrue(len(actual) > 30)
        self.assertEqual(actual.split(".")[-1], "jpeg")





    
