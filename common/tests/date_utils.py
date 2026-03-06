from django.test import SimpleTestCase
from ..date_utils import *



class DateUtilsTests(SimpleTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_conv_str_to_datetime(self):
        actual = conv_str_to_datetime("2021/05/25", '%Y/%m/%d')
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEqual(str(actual.date()), "2021-05-25")

        actual = conv_str_to_datetime("2021-05-25", '%Y-%m-%d')
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEqual(str(actual.date()), "2021-05-25")

        actual = conv_str_to_datetime("25/05/2021", '%d/%m/%Y')
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEqual(str(actual.date()), "2021-05-25")

        actual = conv_str_to_datetime("25/05/2021", '')
        self.assertEqual(actual, "")

        actual = conv_str_to_datetime("", '%d/%m/%Y')
        self.assertEqual(actual, "")

        actual = conv_str_to_datetime("", '')
        self.assertEqual(actual, "")

        actual = conv_str_to_datetime("-1", '%Y/%m/%d')
        self.assertEqual(actual, "")

    def test_conv_yyyymmdd_to_datetime(self):
        actual = conv_yyyymmdd_to_datetime("2021/05/25", '/')
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEqual(str(actual.date()), "2021-05-25")

        actual = conv_yyyymmdd_to_datetime("2022-12-05", '-')
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEqual(str(actual.date()), "2022-12-05")

        actual = conv_yyyymmdd_to_datetime("2022-12-05")
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEqual(str(actual.date()), "2022-12-05")

        actual = conv_yyyymmdd_to_datetime("20231231", "")
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEqual(str(actual.date()), "2023-12-31")

        actual = conv_yyyymmdd_to_datetime("-1", '-')
        self.assertEqual(actual, "")

    def test_get_years_difference(self):
        dts = conv_yyyymmdd_to_datetime("2023-12-31", '-')
        dte = conv_yyyymmdd_to_datetime("2024-12-31", '-')
        actual = get_years_difference(dts, dte)
        self.assertEqual(actual, 1)

        dts = conv_yyyymmdd_to_datetime("2023-12-31", '-')
        dte = conv_yyyymmdd_to_datetime("2025-12-31", '-')
        actual = get_years_difference(dts, dte)
        self.assertEqual(actual, 2)

        dts = conv_yyyymmdd_to_datetime("2023-12-31", '-')
        dte = conv_yyyymmdd_to_datetime("2025-05-31", '-')
        actual = get_years_difference(dts, dte)
        self.assertEqual(actual, 1)

        dts = conv_yyyymmdd_to_datetime("1950-03-11", '-')
        dte = conv_yyyymmdd_to_datetime("2025-03-10", '-')
        actual = get_years_difference(dts, dte)
        self.assertEqual(actual, 74)

        dts = conv_yyyymmdd_to_datetime("1950-03-11", '-')
        dte = conv_yyyymmdd_to_datetime("2025-03-11", '-')
        actual = get_years_difference(dts, dte)
        self.assertEqual(actual, 75)

        dts = conv_yyyymmdd_to_datetime("2000-04-18", '-')
        dte = conv_yyyymmdd_to_datetime("2024-04-18", '-')
        actual = get_years_difference(dts, dte)
        self.assertEqual(actual, 24)

        dts = conv_yyyymmdd_to_datetime("2000-04-18", '-')
        dte = conv_yyyymmdd_to_datetime("2024-04-17", '-')
        actual = get_years_difference(dts, dte)
        self.assertEqual(actual, 23)

        dts = conv_yyyymmdd_to_datetime("2000-04-18", '-')
        dte = conv_yyyymmdd_to_datetime("2024-04-19", '-')
        actual = get_years_difference(dts, dte)
        self.assertEqual(actual, 24)

        actual = get_years_difference("", "")
        self.assertEqual(actual, 0)

        actual = get_years_difference("one", "two")
        self.assertEqual(actual, 0)

        actual = get_years_difference(1, 2)
        self.assertEqual(actual, 0)