from django.test import SimpleTestCase
from ..utils import *
from ..date_utils import conv_yyyymmdd_to_datetime



class UtilsTests(SimpleTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_is_first_val_greater_than_second_val_true(self):
        result, message = is_first_val_greater_than_second_val(2, 1)
        self.assertTrue(result)
        self.assertEqual(message, "2 > 1")

        result, message = is_first_val_greater_than_second_val(2, 1, "2 більше від 1")
        self.assertTrue(result)
        self.assertEqual(message, "2 більше від 1")

        result, message = is_first_val_greater_than_second_val("2024-04-01", "2024-03-31")
        self.assertTrue(result)
        self.assertEqual(message, "2024-04-01 > 2024-03-31")

        result, message = is_first_val_greater_than_second_val("2024-04-01", "2024-03-31", "Перша дата більша за другу")
        self.assertTrue(result)
        self.assertEqual(message, "Перша дата більша за другу")

        result, message = is_first_val_greater_than_second_val("перший", "друга")
        self.assertTrue(result)
        self.assertEqual(message, "перший > друга")

    def test_is_first_val_greater_than_second_val_false(self):
        result, message = is_first_val_greater_than_second_val(1, 2)
        self.assertFalse(result)
        self.assertEqual(message, "")

        result, message = is_first_val_greater_than_second_val(1, 2, "2 більше від 1")
        self.assertFalse(result)
        self.assertEqual(message, "")

        result, message = is_first_val_greater_than_second_val("2024-03-31", "2024-04-01")
        self.assertFalse(result)
        self.assertEqual(message, "")

        result, message = is_first_val_greater_than_second_val("2024-03-31", "2024-04-01", "Перша дата більша за другу")
        self.assertFalse(result)
        self.assertEqual(message, "")

        result, message = is_first_val_greater_than_second_val("друга", "перший")
        self.assertFalse(result)
        self.assertEqual(message, "")

        result, message = is_first_val_greater_than_second_val("", "перший")
        self.assertFalse(result)
        self.assertEqual(message, "")

        result, message = is_first_val_greater_than_second_val("перший", "")
        self.assertFalse(result)
        self.assertEqual(message, "")

        result, message = is_first_val_greater_than_second_val("", "")
        self.assertFalse(result)
        self.assertEqual(message, "")

        result, message = is_first_val_greater_than_second_val(False, False)
        self.assertFalse(result)
        self.assertEqual(message, "")

        result, message = is_first_val_greater_than_second_val(None, None)
        self.assertFalse(result)
        self.assertEqual(message, "")

        result, message = is_first_val_greater_than_second_val(None, "2024-04-18")
        self.assertFalse(result)
        self.assertEqual(message, "")

        result, message = is_first_val_greater_than_second_val(None, conv_yyyymmdd_to_datetime("2024-04-18", "-"))
        self.assertFalse(result)
        self.assertEqual(message, "")

        result, message = is_first_val_greater_than_second_val(conv_yyyymmdd_to_datetime("2024-04-18", "-"), None)
        self.assertFalse(result)
        self.assertEqual(message, "")



