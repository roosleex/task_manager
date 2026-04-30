from django.test import SimpleTestCase
from ..utils import *
from ..date_utils import conv_yyyymmdd_to_datetime
from unittest.mock import patch, call, Mock


class UtilsTests(SimpleTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_is_first_val_greater_than_second_val_true(self):
        result, message = is_first_val_greater_than_second_val(2, 1)
        self.assertTrue(result)
        self.assertEquals(message, "2 > 1")

        result, message = is_first_val_greater_than_second_val(2, 1, "2 більше від 1")
        self.assertTrue(result)
        self.assertEquals(message, "2 більше від 1")

        result, message = is_first_val_greater_than_second_val("2024-04-01", "2024-03-31")
        self.assertTrue(result)
        self.assertEquals(message, "2024-04-01 > 2024-03-31")

        result, message = is_first_val_greater_than_second_val("2024-04-01", "2024-03-31", "Перша дата більша за другу")
        self.assertTrue(result)
        self.assertEquals(message, "Перша дата більша за другу")

        result, message = is_first_val_greater_than_second_val("перший", "друга")
        self.assertTrue(result)
        self.assertEquals(message, "перший > друга")

    def test_is_first_val_greater_than_second_val_false(self):
        result, message = is_first_val_greater_than_second_val(1, 2)
        self.assertFalse(result)
        self.assertEquals(message, "")

        result, message = is_first_val_greater_than_second_val(1, 2, "2 більше від 1")
        self.assertFalse(result)
        self.assertEquals(message, "")

        result, message = is_first_val_greater_than_second_val("2024-03-31", "2024-04-01")
        self.assertFalse(result)
        self.assertEquals(message, "")

        result, message = is_first_val_greater_than_second_val("2024-03-31", "2024-04-01", "Перша дата більша за другу")
        self.assertFalse(result)
        self.assertEquals(message, "")

        result, message = is_first_val_greater_than_second_val("друга", "перший")
        self.assertFalse(result)
        self.assertEquals(message, "")

        result, message = is_first_val_greater_than_second_val("", "перший")
        self.assertFalse(result)
        self.assertEquals(message, "")

        result, message = is_first_val_greater_than_second_val("перший", "")
        self.assertFalse(result)
        self.assertEquals(message, "")

        result, message = is_first_val_greater_than_second_val("", "")
        self.assertFalse(result)
        self.assertEquals(message, "")

        result, message = is_first_val_greater_than_second_val(False, False)
        self.assertFalse(result)
        self.assertEquals(message, "")

        result, message = is_first_val_greater_than_second_val(None, None)
        self.assertFalse(result)
        self.assertEquals(message, "")

        result, message = is_first_val_greater_than_second_val(None, "2024-04-18")
        self.assertFalse(result)
        self.assertEquals(message, "")

        result, message = is_first_val_greater_than_second_val(None, conv_yyyymmdd_to_datetime("2024-04-18", "-"))
        self.assertFalse(result)
        self.assertEquals(message, "")

        result, message = is_first_val_greater_than_second_val(conv_yyyymmdd_to_datetime("2024-04-18", "-"), None)
        self.assertFalse(result)
        self.assertEquals(message, "")


# ==========


class ListGetTests(SimpleTestCase):

    def test_valid_index(self):
        self.assertEqual(list_get([1, 2, 3], 0), 1)
        self.assertEqual(list_get([1, 2, 3], 2), 3)

    def test_index_out_of_range(self):
        self.assertEqual(list_get([1, 2, 3], 3), "")
        self.assertEqual(list_get([1, 2, 3], 100), "")

    def test_negative_index_rejected(self):
        self.assertEqual(list_get([1, 2, 3], -1), "")
        self.assertEqual(list_get([1, 2, 3], -10), "")

    def test_non_integer_index(self):
        self.assertEqual(list_get([1, 2, 3], "1"), "")
        self.assertEqual(list_get([1, 2, 3], None), "")
        self.assertEqual(list_get([1, 2, 3], 1.5), "")

    def test_custom_default_value(self):
        self.assertEqual(list_get([1], 5, default="default"), "default")
        self.assertEqual(list_get([], 0, default=999), 999)

    def test_empty_list(self):
        self.assertEqual(list_get([], 0), "")
        self.assertEqual(list_get([], 10, "fallback"), "fallback")

    def test_default_when_valid_index_but_redundant_check(self):
        # ensures final fallback logic doesn't break valid access
        self.assertEqual(list_get([10, 20, 30], 1, "default"), 20)


# ==========


class EvalStrTests(SimpleTestCase):

    def test_simple_expression(self):
        self.assertEqual(eval_str("1 + 2"), 3)

    def test_with_globals(self):
        result = eval_str("x + 5", globals={"x": 10})
        self.assertEqual(result, 15)

    def test_with_locals(self):
        result = eval_str("y * 2", locals={"y": 4})
        self.assertEqual(result, 8)

    def test_empty_code_raises(self):
        with self.assertRaises(ValueError):
            eval_str("")

    def test_non_string_code_raises(self):
        with self.assertRaises(ValueError):
            eval_str(123)

    def test_forbidden_keyword(self):
        with self.assertRaises(ValueError):
            eval_str("__import__('os')")

    def test_dunder_blocked(self):
        with self.assertRaises(ValueError):
            eval_str("().__class__")

    def test_runtime_error_wrapped(self):
        with self.assertRaises(ValueError) as ctx:
            eval_str("1 / 0")

        self.assertIn("Error evaluating expression", str(ctx.exception))

    def test_no_builtins_available(self):
        with self.assertRaises(ValueError):
            eval_str("len([1,2,3])")


# ==========


class LatinToUkrainianTests(SimpleTestCase):

    def test_basic_transliteration(self):
        self.assertEqual(latin_to_ukrainian("A"), "А")
        self.assertEqual(latin_to_ukrainian("B"), "В")
        self.assertEqual(latin_to_ukrainian("X"), "Х")

    def test_word_transliteration(self):
        self.assertEqual(latin_to_ukrainian("TAXI"), "ТАХІ")
        self.assertEqual(latin_to_ukrainian("HOME"), "НОМЕ")

    def test_mixed_characters(self):
        # characters not in map should stay unchanged
        self.assertEqual(latin_to_ukrainian("ABCZ"), "АВСZ")

    def test_lowercase_not_transliterated(self):
        # lowercase letters are not in the map
        self.assertEqual(latin_to_ukrainian("abc"), "abc")

    def test_numbers_and_symbols(self):
        self.assertEqual(latin_to_ukrainian("A1-B2"), "А1-В2")

    def test_empty_string(self):
        self.assertEqual(latin_to_ukrainian(""), "")

    def test_no_changes(self):
        self.assertEqual(latin_to_ukrainian("123!@#"), "123!@#")

    def test_full_mapping(self):
        self.assertEqual(
            latin_to_ukrainian("ABCEHIKMOPTXY"),
            "АВСЕНІКМОРТХУ"
        )


# ==========


class SortDictByUkUaTests(SimpleTestCase):
    @patch("common.utils.locale.strxfrm")
    @patch("common.utils.locale.setlocale")
    def test_sorting_order(self, mock_setlocale, mock_strxfrm):
        # Make sorting deterministic
        mock_strxfrm.side_effect = lambda x: x

        data = {"в": 1, "а": 2, "б": 3}

        result = sort_dict_by_uk_ua(data)

        self.assertEqual(list(result.keys()), ["а", "б", "в"])

    @patch("common.utils.locale.strxfrm")
    @patch("common.utils.locale.setlocale")
    def test_setlocale_called_and_restored(self, mock_setlocale, mock_strxfrm):
        mock_strxfrm.side_effect = lambda x: x
        mock_setlocale.side_effect = ["old_locale", None, None]

        data = {"b": 1}

        sort_dict_by_uk_ua(data)

        mock_setlocale.assert_has_calls([
            call(locale.LC_ALL),                     # save current
            call(locale.LC_ALL, "uk_UA.UTF-8"),     # set Ukrainian locale
            call(locale.LC_ALL, "old_locale"),      # restore
        ])

    @patch("common.utils.locale.strxfrm")
    @patch("common.utils.locale.setlocale")
    def test_empty_dict(self, mock_setlocale, mock_strxfrm):
        mock_setlocale.side_effect = ["old_locale", None, None]

        result = sort_dict_by_uk_ua({})

        self.assertEqual(result, {})

    @patch("common.utils.locale.strxfrm")
    @patch("common.utils.locale.setlocale")
    def test_single_item(self, mock_setlocale, mock_strxfrm):
        mock_setlocale.side_effect = ["old_locale", None, None]

        data = {"а": 1}

        result = sort_dict_by_uk_ua(data)

        self.assertEqual(result, {"а": 1})

    @patch("common.utils.locale.strxfrm")
    @patch("common.utils.locale.setlocale")
    def test_sorting_called_with_keys(self, mock_setlocale, mock_strxfrm):
        mock_strxfrm.side_effect = lambda x: x

        data = {"z": 1, "x": 2}

        sort_dict_by_uk_ua(data)

        mock_strxfrm.assert_any_call("z")
        mock_strxfrm.assert_any_call("x")


# ==========


class IsTrustedUserTests(SimpleTestCase):

    def test_trusted_user_returns_true(self):
        user = Mock()
        user.is_staff = True
        user.is_active = True
        user.is_authenticated = True

        self.assertTrue(is_trusted_user(user))

    def test_not_staff_returns_false(self):
        user = Mock()
        user.is_staff = False
        user.is_active = True
        user.is_authenticated = True

        self.assertFalse(is_trusted_user(user))

    def test_not_active_returns_false(self):
        user = Mock()
        user.is_staff = True
        user.is_active = False
        user.is_authenticated = True

        self.assertFalse(is_trusted_user(user))

    def test_not_authenticated_returns_false(self):
        user = Mock()
        user.is_staff = True
        user.is_active = True
        user.is_authenticated = False

        self.assertFalse(is_trusted_user(user))

    def test_none_user_returns_false(self):
        self.assertFalse(is_trusted_user(None))

    def test_partial_user_missing_attribute(self):
        user = Mock(spec=[])  # no attributes
        self.assertFalse(is_trusted_user(user))


# ==========






