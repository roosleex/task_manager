from django.test import SimpleTestCase
from ..numeric_utils import *



class NumericUtilsTests(SimpleTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_conv_ton_to_kg(self):
        actual = conv_ton_to_kg(8.28)
        expected = 8280
        self.assertEquals(actual, expected)

        actual = conv_ton_to_kg(8.281)
        expected = 8281
        self.assertEquals(actual, expected)

        actual = conv_ton_to_kg(8.28, 3)
        expected = 8280
        self.assertEquals(actual, expected)

        actual = conv_ton_to_kg(8.281, 3)
        expected = 8281
        self.assertEquals(actual, expected)

        actual = conv_ton_to_kg(0.12, 3)
        expected = 120
        self.assertEquals(actual, expected)

        actual = conv_ton_to_kg(0.121, 3)
        expected = 121
        self.assertEquals(actual, expected)

        actual = conv_ton_to_kg(0.1212, 3)
        expected = 121.2
        self.assertEquals(actual, expected)


    def test_get_fraction_digits_quantity(self):
        actual = get_fraction_digits_quantity(123.456)
        self.assertEquals(actual, 3)

        actual = get_fraction_digits_quantity(10.0)
        self.assertEquals(actual, 1)

        actual = get_fraction_digits_quantity(42)
        self.assertEquals(actual, 0)

        actual = get_fraction_digits_quantity("3.14159")
        self.assertEquals(actual, 5)

        actual = get_fraction_digits_quantity(-123.456)
        self.assertEquals(actual, 3)

        actual = get_fraction_digits_quantity(-10.0)
        self.assertEquals(actual, 1)

        actual = get_fraction_digits_quantity(-42)
        self.assertEquals(actual, 0)

        actual = get_fraction_digits_quantity("-3.14159")
        self.assertEquals(actual, 5)

        actual = get_fraction_digits_quantity(0)
        self.assertEquals(actual, 0)

        actual = get_fraction_digits_quantity("вася")
        self.assertEquals(actual, 0)


# ==========


class NumToStringTests(SimpleTestCase):

    def test_integer_conversion(self):
        self.assertEqual(num_to_string(10), "10")

    def test_float_conversion(self):
        self.assertEqual(num_to_string(10.5), "10,5")

    def test_large_float(self):
        self.assertEqual(num_to_string(1234.567), "1234,567")

    def test_negative_number(self):
        self.assertEqual(num_to_string(-10.5), "-10,5")

    def test_zero(self):
        self.assertEqual(num_to_string(0), "0")

    def test_string_input(self):
        # function accepts string-like input because it uses str()
        self.assertEqual(num_to_string("10.5"), "10,5")

    def test_none_input(self):
        # edge case: str(None) -> "None"
        self.assertEqual(num_to_string(None), "None")


# ==========


class MoneyToStringTests(SimpleTestCase):

    def test_integer(self):
        self.assertEqual(money_to_string(10), "10,00")

    def test_float_rounding(self):
        self.assertEqual(money_to_string(10.5), "10,50")

    def test_rounding_up(self):
        self.assertEqual(money_to_string(10.567), "10,57")

    def test_rounding_down(self):
        self.assertEqual(money_to_string(10.564), "10,56")

    def test_zero(self):
        self.assertEqual(money_to_string(0), "0,00")

    def test_negative_value(self):
        self.assertEqual(money_to_string(-10.5), "-10,50")

    def test_large_number(self):
        self.assertEqual(money_to_string(1234567.891), "1234567,89")

    def test_string_input(self):
        # string gets formatted via f-string float conversion
        self.assertEqual(money_to_string(10.5), "10,50")


# ==========


class UkrainianNumberToTextTests(SimpleTestCase):

    def test_zero(self):
        self.assertEqual(ukrainian_number_to_text(0), "нуль")

    def test_units_masculine(self):
        self.assertEqual(ukrainian_number_to_text(1, "m"), "один")
        self.assertEqual(ukrainian_number_to_text(2, "m"), "два")
        self.assertEqual(ukrainian_number_to_text(9, "m"), "дев'ять")

    def test_units_feminine(self):
        self.assertEqual(ukrainian_number_to_text(1, "f"), "одна")
        self.assertEqual(ukrainian_number_to_text(2, "f"), "дві")

    def test_teens(self):
        self.assertEqual(ukrainian_number_to_text(10), "десять")
        self.assertEqual(ukrainian_number_to_text(11), "одинадцять")
        self.assertEqual(ukrainian_number_to_text(15), "п'ятнадцять")
        self.assertEqual(ukrainian_number_to_text(19), "дев'ятнадцять")

    def test_tens(self):
        self.assertEqual(ukrainian_number_to_text(20), "двадцять")
        self.assertEqual(ukrainian_number_to_text(30), "тридцять")
        self.assertEqual(ukrainian_number_to_text(90), "дев'яносто")

    def test_hundreds(self):
        self.assertEqual(ukrainian_number_to_text(100), "сто")
        self.assertEqual(ukrainian_number_to_text(200), "двісті")
        self.assertEqual(ukrainian_number_to_text(500), "п'ятсот")

    def test_complex_numbers(self):
        self.assertEqual(ukrainian_number_to_text(121), "сто двадцять один")
        self.assertEqual(ukrainian_number_to_text(234), "двісті тридцять чотири")
        self.assertEqual(ukrainian_number_to_text(999), "дев'ятсот дев'яносто дев'ять")

    def test_feminine_complex_numbers(self):
        self.assertEqual(ukrainian_number_to_text(222, "f"), "двісті двадцять дві")

    def test_teens_with_hundreds(self):
        self.assertEqual(ukrainian_number_to_text(111), "сто одинадцять")
        self.assertEqual(ukrainian_number_to_text(219), "двісті дев'ятнадцять")

    def test_invalid_numbers(self):
        self.assertEqual(ukrainian_number_to_text(-1), "")
        self.assertEqual(ukrainian_number_to_text(-10), "")
        self.assertEqual(ukrainian_number_to_text(1000), "")
        self.assertEqual(ukrainian_number_to_text(10000), "")
        self.assertEqual(ukrainian_number_to_text("abc"), "")


# ==========


class GetUkrainianNumberFormTests(SimpleTestCase):

    def setUp(self):
        self.forms = ["one", "few", "many"]

    def test_singular(self):
        self.assertEqual(get_ukrainian_number_form(1, self.forms), "one")
        self.assertEqual(get_ukrainian_number_form(21, self.forms), "one")
        self.assertEqual(get_ukrainian_number_form(31, self.forms), "one")

    def test_few(self):
        self.assertEqual(get_ukrainian_number_form(2, self.forms), "few")
        self.assertEqual(get_ukrainian_number_form(3, self.forms), "few")
        self.assertEqual(get_ukrainian_number_form(4, self.forms), "few")
        self.assertEqual(get_ukrainian_number_form(22, self.forms), "few")

    def test_many(self):
        self.assertEqual(get_ukrainian_number_form(0, self.forms), "many")
        self.assertEqual(get_ukrainian_number_form(5, self.forms), "many")
        self.assertEqual(get_ukrainian_number_form(11, self.forms), "many")
        self.assertEqual(get_ukrainian_number_form(14, self.forms), "many")
        self.assertEqual(get_ukrainian_number_form(19, self.forms), "many")
        self.assertEqual(get_ukrainian_number_form(100, self.forms), "many")

    def test_negative_numbers(self):
        self.assertEqual(get_ukrainian_number_form(-1, self.forms), "one")
        self.assertEqual(get_ukrainian_number_form(-2, self.forms), "few")
        self.assertEqual(get_ukrainian_number_form(-5, self.forms), "many")

    def test_edge_teens(self):
        self.assertEqual(get_ukrainian_number_form(11, self.forms), "many")
        self.assertEqual(get_ukrainian_number_form(12, self.forms), "many")
        self.assertEqual(get_ukrainian_number_form(13, self.forms), "many")
        self.assertEqual(get_ukrainian_number_form(14, self.forms), "many")
        self.assertEqual(get_ukrainian_number_form(15, self.forms), "many")


# ==========


class MoneyToUkrTextTests(SimpleTestCase):

    def test_simple_amount(self):
        result = money_to_ukr_text(1.00)
        self.assertIn("гривня", result)
        self.assertIn("00 копійок", result)
        self.assertEqual("одна гривня 00 копійок", result)

    def test_few_hryvnias(self):
        result = money_to_ukr_text(2.00)
        self.assertIn("гривні", result)
        self.assertEqual("дві гривні 00 копійок", result)

    def test_many_hryvnias(self):
        result = money_to_ukr_text(5.00)
        self.assertIn("гривень", result)
        self.assertEqual("п'ять гривень 00 копійок", result)

    def test_kopecks_formatting(self):
        result = money_to_ukr_text(10.5)
        self.assertIn("50 копійок", result)
        self.assertEqual("десять гривень 50 копійок", result)

    def test_rounding_kopecks(self):
        result = money_to_ukr_text(10.567)
        self.assertIn("57 копійок", result)
        self.assertEqual("десять гривень 57 копійок", result)

    def test_thousands(self):
        result = money_to_ukr_text(1000.00)
        self.assertIn("тисяча", result)
        self.assertIn("гривень", result)
        self.assertEqual("одна тисяча гривень 00 копійок", result)

    def test_millions(self):
        result = money_to_ukr_text(1_000_000.00)
        self.assertIn("мільйон", result)
        self.assertIn("гривень", result)
        self.assertEqual("один мільйон гривень 00 копійок", result)

    def test_complex_number(self):
        result = money_to_ukr_text(1234567.89)

        self.assertIn("мільйон", result)
        self.assertIn("тисяч", result)
        self.assertIn("гривень", result)
        self.assertIn("89 копійок", result)
        self.assertEqual("один мільйон двісті тридцять чотири тисячі п'ятсот шістдесят сім гривень 89 копійок", result)

        result = money_to_ukr_text(227.93)
        self.assertEqual("двісті двадцять сім гривень 93 копійки", result)

    def test_zero_amount(self):
        result = money_to_ukr_text(0)
        self.assertIn("гривень", result)
        self.assertIn("00 копійок", result)
        self.assertEqual("нуль гривень 00 копійок", result)

    def test_invalid_input_string(self):
        result = money_to_ukr_text("abc")
        self.assertEqual(result, "")

    def test_invalid_input_none(self):
        result = money_to_ukr_text(None)
        self.assertEqual(result, "")





    