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
        self.assertEquals(str(actual.date()), "2021-05-25")

        actual = conv_str_to_datetime("2021-05-25", '%Y-%m-%d')
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEquals(str(actual.date()), "2021-05-25")

        actual = conv_str_to_datetime("25/05/2021", '%d/%m/%Y')
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEquals(str(actual.date()), "2021-05-25")

        actual = conv_str_to_datetime("25/05/2021", '')
        self.assertEquals(actual, "")

        actual = conv_str_to_datetime("", '%d/%m/%Y')
        self.assertEquals(actual, "")

        actual = conv_str_to_datetime("", '')
        self.assertEquals(actual, "")

        actual = conv_str_to_datetime("-1", '%Y/%m/%d')
        self.assertEquals(actual, "")

    def test_conv_yyyymmdd_to_datetime(self):
        actual = conv_yyyymmdd_to_datetime("2021/05/25", '/')
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEquals(str(actual.date()), "2021-05-25")

        actual = conv_yyyymmdd_to_datetime("2022-12-05", '-')
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEquals(str(actual.date()), "2022-12-05")

        actual = conv_yyyymmdd_to_datetime("2022-12-05")
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEquals(str(actual.date()), "2022-12-05")

        actual = conv_yyyymmdd_to_datetime("20231231", "")
        # print(f"actual.date() = {actual.date()}")
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEquals(str(actual.date()), "2023-12-31")

        actual = conv_yyyymmdd_to_datetime("-1", '-')
        self.assertEquals(actual, "")

    def test_get_years_difference(self):
        dts = conv_yyyymmdd_to_datetime("2023-12-31", '-')
        dte = conv_yyyymmdd_to_datetime("2024-12-31", '-')
        actual = get_years_difference(dts, dte)
        self.assertEquals(actual, 1)

        dts = conv_yyyymmdd_to_datetime("2023-12-31", '-')
        dte = conv_yyyymmdd_to_datetime("2025-12-31", '-')
        actual = get_years_difference(dts, dte)
        self.assertEquals(actual, 2)

        dts = conv_yyyymmdd_to_datetime("2023-12-31", '-')
        dte = conv_yyyymmdd_to_datetime("2025-05-31", '-')
        actual = get_years_difference(dts, dte)
        self.assertEquals(actual, 1)

        dts = conv_yyyymmdd_to_datetime("1950-03-11", '-')
        dte = conv_yyyymmdd_to_datetime("2025-03-10", '-')
        actual = get_years_difference(dts, dte)
        self.assertEquals(actual, 74)

        dts = conv_yyyymmdd_to_datetime("1950-03-11", '-')
        dte = conv_yyyymmdd_to_datetime("2025-03-11", '-')
        actual = get_years_difference(dts, dte)
        self.assertEquals(actual, 75)

        dts = conv_yyyymmdd_to_datetime("2000-04-18", '-')
        dte = conv_yyyymmdd_to_datetime("2024-04-18", '-')
        actual = get_years_difference(dts, dte)
        self.assertEquals(actual, 24)

        dts = conv_yyyymmdd_to_datetime("2000-04-18", '-')
        dte = conv_yyyymmdd_to_datetime("2024-04-17", '-')
        actual = get_years_difference(dts, dte)
        self.assertEquals(actual, 23)

        dts = conv_yyyymmdd_to_datetime("2000-04-18", '-')
        dte = conv_yyyymmdd_to_datetime("2024-04-19", '-')
        actual = get_years_difference(dts, dte)
        self.assertEquals(actual, 24)

        actual = get_years_difference("", "")
        self.assertEquals(actual, 0)

        actual = get_years_difference("one", "two")
        self.assertEquals(actual, 0)

        actual = get_years_difference(1, 2)
        self.assertEquals(actual, 0)


    def test_get_month_min_datetime(self):
        actual = get_month_min_datetime("2025-07")
        expected = datetime.datetime(2025, 7, 1, 0, 0, 0)
        self.assertEquals(actual, expected)

        actual = get_month_min_datetime("2025-08")
        expected = datetime.datetime(2025, 8, 1, 0, 0, 0)
        self.assertEquals(actual, expected)


    def test_get_month_max_datetime(self):
        actual = get_month_max_datetime("2025-01")
        expected = datetime.datetime(2025, 1, 31, 23, 59, 59)
        self.assertEquals(actual, expected)

        actual = get_month_max_datetime("2025-02")
        expected = datetime.datetime(2025, 2, 28, 23, 59, 59)
        self.assertEquals(actual, expected)

        actual = get_month_max_datetime("2025-11")
        expected = datetime.datetime(2025, 11, 30, 23, 59, 59)
        self.assertEquals(actual, expected)



    def test_get_month_min_date(self):
        actual = get_month_min_date("2025-07")
        expected = date(2025, 7, 1)
        self.assertEquals(actual, expected)

        actual = get_month_min_date("2025-08")
        expected = date(2025, 8, 1)
        self.assertEquals(actual, expected)


    def test_get_month_max_date(self):
        actual = get_month_max_date("2025-01")
        expected = date(2025, 1, 31)
        self.assertEquals(actual, expected)

        actual = get_month_max_date("2025-02")
        expected = date(2025, 2, 28)
        self.assertEquals(actual, expected)

        actual = get_month_max_date("2025-11")
        expected = date(2025, 11, 30)
        self.assertEquals(actual, expected)

    
    def test_get_very_min_date(self):
        actual = get_very_min_date()
        expected = "1000-01-01"
        self.assertEquals(actual, expected)

    
    def test_get_very_max_date(self):
        actual = get_very_max_date()
        expected = "3000-01-01"
        self.assertEquals(actual, expected)