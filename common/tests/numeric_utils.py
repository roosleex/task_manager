from django.test import SimpleTestCase
from ..numeric_utils import *



class NumericUtilsTests(SimpleTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_conv_ton_to_kg(self):
        actual = conv_ton_to_kg(8.28)
        expected = 8280
        self.assertEqual(actual, expected)

        actual = conv_ton_to_kg(8.281)
        expected = 8281
        self.assertEqual(actual, expected)

        actual = conv_ton_to_kg(8.28, 3)
        expected = 8280
        self.assertEqual(actual, expected)

        actual = conv_ton_to_kg(8.281, 3)
        expected = 8281
        self.assertEqual(actual, expected)

        actual = conv_ton_to_kg(0.12, 3)
        expected = 120
        self.assertEqual(actual, expected)

        actual = conv_ton_to_kg(0.121, 3)
        expected = 121
        self.assertEqual(actual, expected)

        actual = conv_ton_to_kg(0.1212, 3)
        expected = 121.2
        self.assertEqual(actual, expected)


    def test_get_fraction_digits_quantity(self):
        actual = get_fraction_digits_quantity(123.456)
        self.assertEqual(actual, 3)

        actual = get_fraction_digits_quantity(10.0)
        self.assertEqual(actual, 1)

        actual = get_fraction_digits_quantity(42)
        self.assertEqual(actual, 0)

        actual = get_fraction_digits_quantity("3.14159")
        self.assertEqual(actual, 5)

        actual = get_fraction_digits_quantity(-123.456)
        self.assertEqual(actual, 3)

        actual = get_fraction_digits_quantity(-10.0)
        self.assertEqual(actual, 1)

        actual = get_fraction_digits_quantity(-42)
        self.assertEqual(actual, 0)

        actual = get_fraction_digits_quantity("-3.14159")
        self.assertEqual(actual, 5)

        actual = get_fraction_digits_quantity(0)
        self.assertEqual(actual, 0)

        actual = get_fraction_digits_quantity("вася")
        self.assertEqual(actual, 0)
        
       



    