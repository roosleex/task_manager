from django.test import TestCase
from ..html_parser import *


class HtmlParserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.html = """
            select = <select id="id_empty_cemetery_place" name="cemeteryplace-0-cemetery_place">
            <option value="">---------</option>
            <option value="938">№ місця=938, Пашинське</option>
            <option selected="" value="937">№ місця=937, 88888888888999, 888, Пашинське</option>
            <option value="936">№ місця=936, ряд 17, 22 старе, Центральне кладовище</option>
            <option value="935">№ місця=935, 1, 1, Пашинське</option>
            <option value="934">№ місця=934, 1, 1, Пашинське</option>
            <option value="933">№ місця=933, 88888888888999, 888, Пашинське</option>
            <option value="931">№ місця=931, 888, Пашинське</option>
            <option value="930">№ місця=930, 1, 1, Пашинське</option>
            <option value="929">№ місця=929, 1, 1, Пашинське</option>
            <option value="928">№ місця=928, 1, 1, Пашинське</option>
            <option value="926">№ місця=926, ряд 6, 7 нове, Центральне кладовище</option>
            <option value="925">№ місця=925, ряд 1, д/п старе, Центральне кладовище</option>
            <option value="923">№ місця=923, 88888888888999, 888, Пашинське</option>
            <option value="922">№ місця=922, ряд 2, 7 старе, Центральне кладовище</option>
            <option value="919">№ місця=919, ряд 41, 6 старе, Центральне кладовище</option>
            <option value="918">№ місця=918, 88888888888999, 888, Пашинське</option>
            <option value="917">№ місця=917, ряд 17, 22 старе, Центральне кладовище</option>
            <option value="916">№ місця=916, ряд 19, 11 нове, Центральне кладовище</option>
            <option value="915">№ місця=915, 88888888888999, 888, Пашинське</option>
            <option value="913">№ місця=913, 88888888888999, 888, Пашинське</option>
            <option value="900">№ місця=900, Центральне кладовище</option>
            </select>
            """
        cls.html2 = """
            select = <select id="id_empty_cemetery_place2" name="cemeteryplace-0-cemetery_place">
            <option value="">---------</option>
            <option value="934">№ місця=934, 1, 1, Пашинське</option>
            <option value="933">№ місця=933, 88888888888999, 888, Пашинське</option>
            <option value="931">№ місця=931, 888, Пашинське</option>
            <option value="930">№ місця=930, 1, 1, Пашинське</option>
            <option value="929">№ місця=929, 1, 1, Пашинське</option>
            <option value="938">№ місця=938, Пашинське</option>
            <option selected="" value="245">№ місця=245, 88888888888999, 888, Пашинське</option>
            <option value="936">№ місця=936, ряд 17, 22 старе, Центральне кладовище</option>
            <option value="935">№ місця=935, 1, 1, Пашинське</option>
            </select>
            """
        cls.html3 = """
            select = <select id="id_empty_cemetery_place3" name="cemeteryplace-0-cemetery_place">
            <option selected="" value="">---------</option>
            <option value="934">№ місця=934, 1, 1, Пашинське</option>
            <option value="933">№ місця=933, 88888888888999, 888, Пашинське</option>
            <option value="931">№ місця=931, 888, Пашинське</option>
            <option value="930">№ місця=930, 1, 1, Пашинське</option>
            <option value="929">№ місця=929, 1, 1, Пашинське</option>
            <option value="938">№ місця=938, Пашинське</option>
            </select>
            """

    def test_get_select_selected_value(self):
        actual = get_select_selected_value(self.html, "id_empty_cemetery_place")
        expected = "937"
        self.assertEqual(actual, expected)
        #
        actual = get_select_selected_value(self.html2, "id_empty_cemetery_place2")
        expected = "245"
        self.assertEqual(actual, expected)
        #
        actual = get_select_selected_value(self.html3, "id_empty_cemetery_place3")
        expected = ""
        self.assertEqual(actual, expected)