from django.test import SimpleTestCase, RequestFactory
from ..file_utils import *
from datetime import date
from ..date_utils import conv_yyyymmdd_to_datetime
from django.http import HttpResponse, HttpResponseBadRequest



class FileUtilsTests(SimpleTestCase):
    def setUp(self):
        self.req_factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        pass
        

    def test_get_image_path(self):
        path = "uploads/admin/cemetery_name/"
        actual = get_image_path(path, 0)
        expected = path + "%Y/%m/%d/"
        self.assertEquals(actual, expected)

        actual = get_image_path(path, 1)
        d = date.today()
        expected = path + str(d.year) + "/" + '{:02d}'.format(d.month) + "/" + '{:02d}'.format(d.day) + "/"
        self.assertEquals(actual, expected)

        d = conv_yyyymmdd_to_datetime("2024-01-02")
        actual = get_image_path(path, 2, d)
        expected = path + "2024/01/02/"
        self.assertEquals(actual, expected)

    def test_get_file_uniq_name(self):
        actual = get_file_uniq_name("txt")
        print(actual.split(".")[-1])
        self.assertTrue(actual != "")
        self.assertTrue(len(actual) > 30)
        self.assertEquals(actual.split(".")[-1], "txt")

        actual = get_file_uniq_name("jpg")
        self.assertTrue(actual != "")
        self.assertTrue(len(actual) > 30)
        self.assertEquals(actual.split(".")[-1], "jpg")

        actual = get_file_uniq_name("jpeg")
        self.assertTrue(actual != "")
        self.assertTrue(len(actual) > 30)
        self.assertEquals(actual.split(".")[-1], "jpeg")



class GetFileExportResponseTests(SimpleTestCase):

    def test_xlsx_response_success(self):
        file_data = b"dummy excel content"
        file_name = "test_file"

        response = get_file_export_response("xlsx", file_data, file_name)

        # Check response type
        self.assertIsInstance(response, HttpResponse)

        # Check content
        self.assertEqual(response.content, file_data)

        # Check content type
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Check Content-Disposition header
        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="test_file.xlsx"'
        )

    def test_invalid_format(self):
        response = get_file_export_response("csv", b"data", "file")

        # Should return bad request
        self.assertIsInstance(response, HttpResponseBadRequest)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid request")

    def test_empty_file_data(self):
        file_data = b""
        file_name = "empty"

        response = get_file_export_response("xlsx", file_data, file_name)

        self.assertEqual(response.content, b"")
        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="empty.xlsx"'
        )

    def test_filename_with_special_chars(self):
        file_data = b"data"
        file_name = "my file @123"

        response = get_file_export_response("xlsx", file_data, file_name)

        self.assertEqual(
            response["Content-Disposition"],
            'attachment; filename="my file @123.xlsx"'
        )





    
