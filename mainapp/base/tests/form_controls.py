from django.test import SimpleTestCase
from ..form_controls import *
from django import forms
from unittest.mock import Mock, patch
from datetime import date
from datetime import datetime
from django.utils.timezone import make_naive


class GetChoicesEmptyDefaultTests(SimpleTestCase):

    def test_returns_list(self):
        result = get_choices_empty_default()
        self.assertIsInstance(result, list)

    def test_returns_single_tuple(self):
        result = get_choices_empty_default()
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], tuple)

    def test_returns_correct_value(self):
        result = get_choices_empty_default()
        self.assertEqual(result, [('', '---------')])

    def test_tuple_structure(self):
        value, label = get_choices_empty_default()[0]
        self.assertEqual(value, '')
        self.assertEqual(label, '---------')


class FullDateTests(SimpleTestCase):

    def test_default_label(self):
        field = FullDate()
        self.assertEqual(field.label, "Дата")

    def test_custom_label(self):
        field = FullDate(label="Start date")
        self.assertEqual(field.label, "Start date")

    def test_default_required_false(self):
        field = FullDate()
        self.assertFalse(field.required)

    def test_custom_required_true(self):
        field = FullDate(required=True)
        self.assertTrue(field.required)

    def test_widget_is_textinput(self):
        field = FullDate()
        self.assertIsInstance(field.widget, forms.TextInput)

    def test_inherits_datefield_behavior_valid(self):
        field = FullDate(required=True)

        value = field.clean("2026-04-16")
        self.assertEqual(str(value), "2026-04-16")

    def test_inherits_datefield_behavior_invalid(self):
        field = FullDate(required=True)

        with self.assertRaises(forms.ValidationError):
            field.clean("invalid-date")


class FullDateMinTests(SimpleTestCase):

    def test_default_label(self):
        field = FullDateMin()
        self.assertEqual(field.label, "Дата початкова")

    def test_custom_label(self):
        field = FullDateMin(label="Start date")
        self.assertEqual(field.label, "Start date")

    def test_default_required_false(self):
        field = FullDateMin()
        self.assertFalse(field.required)

    def test_custom_required_true(self):
        field = FullDateMin(required=True)
        self.assertTrue(field.required)

    def test_widget_is_textinput(self):
        field = FullDateMin()
        self.assertIsInstance(field.widget, forms.TextInput)

    def test_widget_renders_date_input(self):
        field = FullDateMin()
        html = field.widget.render(name="test", value=None)

        self.assertIn('type="date"', html)

    def test_valid_date_clean(self):
        field = FullDateMin(required=True)

        value = field.clean("2026-04-16")
        self.assertEqual(str(value), "2026-04-16")

    def test_invalid_date_raises_error(self):
        field = FullDateMin(required=True)

        with self.assertRaises(forms.ValidationError):
            field.clean("invalid-date")


class FullDateMaxTests(SimpleTestCase):

    def test_default_label(self):
        field = FullDateMax()
        self.assertEqual(field.label, "Дата кінцева")

    def test_custom_label(self):
        field = FullDateMax(label="End date")
        self.assertEqual(field.label, "End date")

    def test_default_required_false(self):
        field = FullDateMax()
        self.assertFalse(field.required)

    def test_custom_required_true(self):
        field = FullDateMax(required=True)
        self.assertTrue(field.required)

    def test_widget_is_textinput(self):
        field = FullDateMax()
        self.assertIsInstance(field.widget, forms.TextInput)

    def test_widget_renders_date_input(self):
        field = FullDateMax()
        html = field.widget.render(name="test", value=None)

        self.assertIn('type="date"', html)

    def test_valid_date_clean(self):
        field = FullDateMax(required=True)

        value = field.clean("2026-04-16")
        self.assertEqual(str(value), "2026-04-16")

    def test_invalid_date_raises_error(self):
        field = FullDateMax(required=True)

        with self.assertRaises(forms.ValidationError):
            field.clean("invalid-date")


class AllModelsNamesTests(SimpleTestCase):

    # ---- helpers ----

    def make_model(self, name, exists=True, raise_exc=False):
        model = Mock()
        model.__name__ = name

        if raise_exc:
            model.objects.exists.side_effect = Exception("error")
        else:
            model.objects.exists.return_value = exists

        model._meta.verbose_name = name.lower()
        return model

    # ---- get_model_choices ----

    @patch("django.apps.apps.get_app_config")
    def test_get_model_choices_filters_and_formats(self, mock_get_app_config):
        model1 = self.make_model("Book", exists=True)
        model2 = self.make_model("Author", exists=False)  # should be skipped
        model3 = self.make_model("HistoricalBook", exists=True)  # skipped by name

        mock_app = Mock()
        mock_app.get_models.return_value = [model1, model2, model3]
        mock_get_app_config.return_value = mock_app

        field = AllModelsNames("mainapp")

        self.assertEqual(field.choices, [
            ("Book", "Book"),
        ])

    @patch("django.apps.apps.get_app_config")
    def test_get_model_choices_handles_exceptions(self, mock_get_app_config):
        model1 = self.make_model("Book", exists=True)
        model2 = self.make_model("BrokenModel", raise_exc=True)

        mock_app = Mock()
        mock_app.get_models.return_value = [model1, model2]
        mock_get_app_config.return_value = mock_app

        field = AllModelsNames("mainapp")

        self.assertEqual(field.choices, [
            ("Book", "Book"),
        ])

    # ---- init behavior ----

    @patch("django.apps.apps.get_app_config")
    def test_default_label_and_required(self, mock_get_app_config):
        mock_app = Mock()
        mock_app.get_models.return_value = []
        mock_get_app_config.return_value = mock_app

        field = AllModelsNames("mainapp")

        self.assertEqual(field.label, "Довідник")
        self.assertTrue(field.required)

    @patch("django.apps.apps.get_app_config")
    def test_custom_label(self, mock_get_app_config):
        mock_app = Mock()
        mock_app.get_models.return_value = []
        mock_get_app_config.return_value = mock_app

        field = AllModelsNames("mainapp", label="Custom")

        self.assertEqual(field.label, "Custom")

    @patch("django.apps.apps.get_app_config")
    def test_choices_passed_to_choicefield(self, mock_get_app_config):
        model = self.make_model("Book", exists=True)

        mock_app = Mock()
        mock_app.get_models.return_value = [model]
        mock_get_app_config.return_value = mock_app

        field = AllModelsNames("mainapp")

        self.assertIsInstance(field, forms.ChoiceField)
        self.assertEqual(field.choices, [("Book", "Book")])


class MonthInputTests(SimpleTestCase):

    def setUp(self):
        self.widget = MonthInput()

    # ---- input_type ----

    def test_input_type_is_month(self):
        self.assertEqual(self.widget.input_type, "month")

    # ---- format_value ----

    def test_format_value_with_date(self):
        value = date(2026, 4, 16)

        result = self.widget.format_value(value)

        self.assertEqual(result, "2026-04")

    def test_format_value_with_string(self):
        value = "2026-04"

        result = self.widget.format_value(value)

        # falls back to parent behavior
        self.assertEqual(result, value)

    def test_format_value_with_none(self):
        result = self.widget.format_value(None)

        self.assertIsNone(result)

    def test_format_value_with_non_date_object(self):
        value = 12345

        result = self.widget.format_value(value)

        # fallback to parent (string conversion usually)
        self.assertEqual(result, str(value))


class MonthDateTests(SimpleTestCase):

    def setUp(self):
        self.field = MonthDate()

    # ---- init ----

    def test_default_label(self):
        self.assertEqual(self.field.label, "Місяць")

    def test_custom_label(self):
        field = MonthDate(label="Month")
        self.assertEqual(field.label, "Month")

    def test_default_required_false(self):
        self.assertFalse(self.field.required)

    def test_custom_required_true(self):
        field = MonthDate(required=True)
        self.assertTrue(field.required)

    def test_widget_is_monthinput(self):
        self.assertIsInstance(self.field.widget, MonthInput)

    # ---- to_python ----

    def test_to_python_valid_value(self):
        result = self.field.to_python("2026-04")

        self.assertEqual(result, date(2026, 4, 1))

    def test_to_python_single_digit_month(self):
        result = self.field.to_python("2026-4")

        self.assertEqual(result, date(2026, 4, 1))

    def test_to_python_empty_value(self):
        self.assertIsNone(self.field.to_python(""))
        self.assertIsNone(self.field.to_python(None))

    def test_to_python_invalid_format(self):
        with self.assertRaises(forms.ValidationError):
            self.field.to_python("invalid")

    def test_to_python_invalid_month(self):
        with self.assertRaises(forms.ValidationError):
            self.field.to_python("2026-13")

    def test_to_python_invalid_structure(self):
        with self.assertRaises(forms.ValidationError):
            self.field.to_python("2026")  # missing month

    # ---- integration with clean() ----

    def test_clean_valid(self):
        field = MonthDate(required=True)

        result = field.clean("2026-04")
        self.assertEqual(result, date(2026, 4, 1))

    def test_clean_required_error(self):
        field = MonthDate(required=True)

        with self.assertRaises(forms.ValidationError):
            field.clean("")


class CustomSelectTests(SimpleTestCase):

    # ---- init basics ----

    @patch("mainapp.base.form_controls.get_choices_empty_default")
    def test_label_and_required(self, mock_empty):
        mock_empty.return_value = [("", "EMPTY")]

        field = CustomSelect(
            label="Test Label",
            required=True,
            choices=[]
        )

        self.assertEqual(field.label, "Test Label")
        self.assertTrue(field.required)

    # ---- choices merging ----

    @patch("mainapp.base.form_controls.get_choices_empty_default")
    def test_choices_are_combined(self, mock_empty):
        mock_empty.return_value = [("", "EMPTY")]

        field = CustomSelect(
            label="Test",
            required=False,
            choices=[("a", "A"), ("b", "B")]
        )

        self.assertEqual(
            field.choices,
            [("", "EMPTY"), ("a", "A"), ("b", "B")]
        )

    @patch("mainapp.base.form_controls.get_choices_empty_default")
    def test_choices_with_empty_list(self, mock_empty):
        mock_empty.return_value = [("", "EMPTY")]

        field = CustomSelect(
            label="Test",
            required=False,
            choices=[]
        )

        self.assertEqual(field.choices, [("", "EMPTY")])

    # ---- override via kwargs ----

    @patch("mainapp.base.form_controls.get_choices_empty_default")
    def test_kwargs_choices_override(self, mock_empty):
        mock_empty.return_value = [("", "EMPTY")]

        field = CustomSelect(
            "Test",
            False,
            **{"choices": [("override", "Override")]}
        )

        self.assertEqual(field.choices, [('', 'EMPTY'), ('override', 'Override')])

    # ---- integration ----

    @patch("mainapp.base.form_controls.get_choices_empty_default")
    def test_is_choicefield_instance(self, mock_empty):
        mock_empty.return_value = []

        field = CustomSelect(
            label="Test",
            required=False,
            choices=[]
        )

        self.assertIsInstance(field, forms.ChoiceField)

    @patch("mainapp.base.form_controls.get_choices_empty_default")
    def test_valid_choice_clean(self, mock_empty):
        mock_empty.return_value = [("", "EMPTY")]

        field = CustomSelect(
            label="Test",
            required=True,
            choices=[("a", "A")]
        )

        result = field.clean("a")
        self.assertEqual(result, "a")

    @patch("mainapp.base.form_controls.get_choices_empty_default")
    def test_invalid_choice_raises_error(self, mock_empty):
        mock_empty.return_value = [("", "EMPTY")]

        field = CustomSelect(
            label="Test",
            required=True,
            choices=[("a", "A")]
        )

        with self.assertRaises(forms.ValidationError):
            field.clean("invalid")


class FullDateTimeInputTests(SimpleTestCase):

    def test_widget_is_split_datetime_widget(self):
        widget = FullDateTimeInput()

        self.assertIsInstance(widget, forms.SplitDateTimeWidget)

    def test_date_widget_attributes(self):
        widget = FullDateTimeInput()

        self.assertEqual(widget.widgets[0].input_type, "date")
        self.assertEqual(widget.widgets[0].attrs["class"], "form-control")

    def test_time_widget_attributes(self):
        widget = FullDateTimeInput()

        self.assertEqual(widget.widgets[1].input_type, "time")
        self.assertEqual(widget.widgets[1].attrs["class"], "form-control")
        self.assertEqual(widget.widgets[1].attrs["step"], 1)

    def test_accepts_custom_attrs(self):
        widget = FullDateTimeInput(attrs={"id": "custom-id"})
        html = widget.render(name="dt", value=None)
        self.assertIn('name="dt', html)

    def test_widget_has_two_subwidgets(self):
        widget = FullDateTimeInput()

        self.assertEqual(len(widget.widgets), 2)

    def test_date_widget_is_text_input_type_date(self):
        widget = FullDateTimeInput()

        date_widget = widget.widgets[0]
        self.assertEqual(date_widget.input_type, "date")  # SplitDateTimeWidget uses TextInput internally

    def test_time_widget_step_is_one(self):
        widget = FullDateTimeInput()

        self.assertEqual(widget.widgets[1].attrs["step"], 1)


class FullDateTimeTests(SimpleTestCase):

    # ---- init behavior ----

    def test_label_and_required(self):
        field = FullDateTime("Test Label", True)

        self.assertEqual(field.label, "Test Label")
        self.assertTrue(field.required)

    def test_widget_is_custom_widget(self):
        field = FullDateTime("Test", False)

        self.assertIsInstance(field.widget, FullDateTimeInput)

    # ---- validation ----

    def test_valid_split_datetime_input(self):
        field = FullDateTime("Test", True)

        value = field.clean(["2026-04-16", "12:30:00"])

        expected = datetime(2026, 4, 16, 12, 30, 0)

        self.assertEqual(make_naive(value), expected)

    def test_invalid_datetime_raises_error(self):
        field = FullDateTime("Test", True)

        with self.assertRaises(forms.ValidationError):
            field.clean(["invalid-date", "invalid-time"])

    def test_empty_value_when_required(self):
        field = FullDateTime("Test", True)

        with self.assertRaises(forms.ValidationError):
            field.clean(["", ""])

    # ---- optional behavior ----

    def test_not_required_allows_empty(self):
        field = FullDateTime("Test", False)

        self.assertIsNone(field.clean(["", ""]))





