from django.test import SimpleTestCase, RequestFactory
from ..http_utils import *



class HttpUtilsTests(SimpleTestCase):
    def setUp(self):
        self.req_factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        pass

    def test_is_ajax_header(self):
        request = self.req_factory.get("/get_cemetery_place_data/")
        request.headers = {
            "X-Requested-With": "XMLHttpRequest",
        }
        self.assertTrue(is_ajax_header(request))

        request = self.req_factory.get("/get_cemetery_place_data/")
        self.assertFalse(is_ajax_header(request))

    def test_is_method_get(self):
        request = self.req_factory.get("/get_cemetery_place_data/")
        request.method = "GET"
        self.assertTrue(is_method_get(request))

        request = self.req_factory.get("/get_cemetery_place_data/")
        self.assertTrue(is_method_get(request))

        request = self.req_factory.get("/get_cemetery_place_data/")
        request.method = "POST"
        self.assertFalse(is_method_get(request))

    def test_is_method_post(self):
        request = self.req_factory.get("/get_cemetery_place_data/")
        request.method = "POST"
        self.assertTrue(is_method_post(request))

        request = self.req_factory.get("/get_cemetery_place_data/")
        self.assertFalse(is_method_post(request))

        request = self.req_factory.get("/get_cemetery_place_data/")
        request.method = "GET"
        self.assertFalse(is_method_post(request))

    def test_get_valid_int(self):
        expected = 1
        actual = get_valid_int(expected)
        self.assertEquals(actual, expected)

        expected = 10
        actual = get_valid_int(expected)
        self.assertEquals(actual, expected)

        expected = -1
        actual = get_valid_int(expected)
        self.assertEquals(actual, expected)

        expected = -10
        actual = get_valid_int(expected)
        self.assertEquals(actual, expected)

        expected = 0
        actual = get_valid_int(expected)
        self.assertEquals(actual, expected)

        expected = 0
        actual = get_valid_int("some string")
        self.assertEquals(actual, expected)

        expected = 0
        actual = get_valid_int("123 some string")
        self.assertEquals(actual, expected)

        expected = 0
        actual = get_valid_int([])
        self.assertEquals(actual, expected)

        expected = 7
        actual = get_valid_int([1,2], 7)
        self.assertEquals(actual, expected)

        expected = -1
        actual = get_valid_int({'ok': 123}, -1)
        self.assertEquals(actual, expected)

    def test_get_valid_str(self):
        expected = ""
        actual = get_valid_str(expected)
        self.assertEquals(actual, expected)

        expected = "a string"
        actual = get_valid_str(expected)
        self.assertEquals(actual, expected)

        expected = "777"
        actual = get_valid_str(expected)
        self.assertEquals(actual, expected)

        expected = "123"
        actual = get_valid_str(123)
        self.assertEquals(actual, expected)

        expected = "[123]"
        actual = get_valid_str([123])
        self.assertEquals(actual, expected)

        expected = "123"
        actual = get_valid_str(123, "Yes")
        self.assertEquals(actual, expected)

        expected = "[123]"
        actual = get_valid_str([123], "Yes")
        self.assertEquals(actual, expected)

        expected = "Yes"
        actual = get_valid_str(None, "Yes")
        self.assertEquals(actual, expected)
        
        expected = "{'1': 123}"
        actual = get_valid_str({"1": 123}, -1)
        self.assertEquals(actual, expected)

        expected = "-1"
        actual = get_valid_str(False, "-1")
        self.assertEquals(actual, expected)

        expected = "True"
        actual = get_valid_str(True)
        self.assertEquals(actual, expected)

        expected = ""
        actual = get_valid_str(False)
        self.assertEquals(actual, expected)

        expected = ""
        actual = get_valid_str(None)
        self.assertEquals(actual, expected)

        expected = "a string 567"
        actual = get_valid_str(expected)
        self.assertEquals(actual, expected)

        expected = "  "
        actual = get_valid_str(expected)
        self.assertEquals(actual, expected)

    def test_is_int_valid(self):
        self.assertTrue(is_int_valid(1))
        self.assertTrue(is_int_valid(0))
        self.assertTrue(is_int_valid(-1))
        self.assertTrue(is_int_valid(10))
        self.assertTrue(is_int_valid(-10))
        self.assertTrue(is_int_valid(10, [1,2]))
        self.assertTrue(is_int_valid(10, [1,2,-1]))
        self.assertTrue(is_int_valid(22), [])

        self.assertFalse(is_int_valid(10, [1,2,10]))
        self.assertFalse(is_int_valid(-1, [0,-1,2]))
        self.assertFalse(is_int_valid(""))
        self.assertFalse(is_int_valid("123"))
        self.assertFalse(is_int_valid("a string"))
        self.assertFalse(is_int_valid(None))
        self.assertFalse(is_int_valid(True))
        self.assertFalse(is_int_valid(False))
        self.assertFalse(is_int_valid(-1, [-1]))
        self.assertFalse(is_int_valid(10, [10]))
        self.assertFalse(is_int_valid(10, [20, 10]))

    def test_clean_val(self):
        expected = 7
        actual = clean_val(expected)
        self.assertEquals(actual, expected)

        expected = -7
        actual = clean_val(expected)
        self.assertEquals(actual, expected)

        expected = 0
        actual = clean_val(expected)
        self.assertEquals(actual, expected)

        expected = ""
        actual = clean_val(expected)
        self.assertEquals(actual, expected)

        expected = "a string"
        actual = clean_val(expected)
        self.assertEquals(actual, expected)

        expected = "777 a string"
        actual = clean_val(expected)
        self.assertEquals(actual, expected)

        expected = ""
        actual = clean_val(10, [10], [""])
        self.assertEquals(actual, expected)

        expected = 1
        actual = clean_val(100, [10, 100], ["", 1])
        self.assertEquals(actual, expected)

        expected = 137
        actual = clean_val(expected, [10, 100], ["", 1])
        self.assertEquals(actual, expected)

        expected = -137
        actual = clean_val(expected, [10, 100], ["", 1])
        self.assertEquals(actual, expected)

        expected = ""
        actual = clean_val(-1, [-1], [""])
        self.assertEquals(actual, expected)

        expected = -1
        actual = clean_val("", [""], [-1])
        self.assertEquals(actual, expected)

        expected = 20
        actual = clean_val("", [""], [20])
        self.assertEquals(actual, expected)

        expected = 30
        actual = clean_val("", [1,""], [20,30])
        self.assertEquals(actual, expected)

        expected = -1
        actual = clean_val(30, [1,"", 30], [20,30,-1])
        self.assertEquals(actual, expected)

        expected = -190
        actual = clean_val(-190, [1,"", 30], [20,30,-1])
        self.assertEquals(actual, expected)

        expected = 187
        actual = clean_val(187, [1,"", 30], [20,30,-1])
        self.assertEquals(actual, expected)

        expected = 187
        expected = clean_val(expected, [1,"", 30], [20,30,-1])
        self.assertEquals(expected, 187)

        expected = 30
        expected = clean_val(expected, [1,"", 30], [20,30,-1])
        self.assertEquals(expected, -1)
        self.assertNotEquals(expected, 30)

    def test_get_valid_float(self):
        expected = 1.12
        actual = get_valid_float(expected)
        self.assertEquals(actual, expected)

        expected = 10.005
        actual = get_valid_float("10.005")
        self.assertEquals(actual, expected)

        expected = 51.00519874
        actual = get_valid_float("51.00519874")
        self.assertEquals(actual, expected)

        expected = -1.003456
        actual = get_valid_float(expected)
        self.assertEquals(actual, expected)

        expected = -10.2340678
        actual = get_valid_float("-10.2340678")
        self.assertEquals(actual, expected)

        expected = 0
        actual = get_valid_float(expected)
        self.assertEquals(actual, expected)

        expected = 0
        actual = get_valid_float("some string")
        self.assertEquals(actual, expected)

        expected = 0
        actual = get_valid_float("123 some string")
        self.assertEquals(actual, expected)

        expected = 0
        actual = get_valid_float([])
        self.assertEquals(actual, expected)

        expected = 7.12345667
        actual = get_valid_float([1,2], 7.12345667)
        self.assertEquals(actual, expected)

        expected = -1
        actual = get_valid_float({'ok': 123}, -1)
        self.assertEquals(actual, expected)



class GetParamsDictFromQueryTests(SimpleTestCase):

    def test_basic_query(self):
        qs = "?a=1&b=2"

        result = get_params_dict_from_query(qs)

        self.assertEqual(result, {"a": "1", "b": "2"})

    def test_without_question_mark(self):
        qs = "a=1&b=2"

        result = get_params_dict_from_query(qs)

        self.assertEqual(result, {"a": "1", "b": "2"})

    def test_empty_query(self):
        qs = ""

        result = get_params_dict_from_query(qs)

        self.assertEqual(result, {})

    def test_blank_values(self):
        qs = "?a=&b=2&c="

        result = get_params_dict_from_query(qs)

        self.assertEqual(result, {"a": "", "b": "2", "c": ""})

    def test_multiple_values_same_key(self):
        qs = "?a=1&a=2&b=3"

        result = get_params_dict_from_query(qs)

        # takes first value
        self.assertEqual(result, {"a": "1", "b": "3"})

    def test_url_encoded_values(self):
        qs = "?name=John%20Doe&city=New%20York"

        result = get_params_dict_from_query(qs)

        self.assertEqual(result, {"name": "John Doe", "city": "New York"})

    def test_special_characters(self):
        qs = "?q=%40test%2Bvalue&sym=%26%3D"

        result = get_params_dict_from_query(qs)

        self.assertEqual(result, {"q": "@test+value", "sym": "&="})

    def test_only_key_no_value(self):
        qs = "?a&b=2"

        result = get_params_dict_from_query(qs)

        self.assertEqual(result, {"a": "", "b": "2"})

    def test_trailing_ampersand(self):
        qs = "?a=1&b=2&"

        result = get_params_dict_from_query(qs)

        self.assertEqual(result, {"a": "1", "b": "2"})



class SetGetItemTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_set_new_key(self):
        request = self.factory.get("/test/?a=1")

        result = set_GET_item(request, "b", "2")

        self.assertTrue(result)
        self.assertEqual(request.GET["b"], "2")
        self.assertEqual(request.GET["a"], "1")  # existing preserved

    def test_update_existing_key(self):
        request = self.factory.get("/test/?a=1")

        set_GET_item(request, "a", "100")

        self.assertEqual(request.GET["a"], "100")

    def test_empty_query(self):
        request = self.factory.get("/test/")

        set_GET_item(request, "new", "value")

        self.assertEqual(request.GET["new"], "value")

    def test_multiple_keys(self):
        request = self.factory.get("/test/?a=1&b=2")

        set_GET_item(request, "c", "3")

        self.assertEqual(request.GET["a"], "1")
        self.assertEqual(request.GET["b"], "2")
        self.assertEqual(request.GET["c"], "3")

    def test_mutability_restored(self):
        request = self.factory.get("/test/?a=1")

        set_GET_item(request, "b", "2")

        # After function, GET should be immutable again
        with self.assertRaises(AttributeError):
            request.GET["c"] = "3"





