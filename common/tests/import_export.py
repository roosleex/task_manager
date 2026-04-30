from django.test import SimpleTestCase
# import your function
from ..import_export import *
# import widgets from import_export
from import_export.widgets import FloatWidget, IntegerWidget, CharWidget
from unittest.mock import patch
from datetime import datetime



class DummyField:
    def __init__(self, column_name):
        self.column_name = column_name


class DummyResource:
    def __init__(self, fields):
        # simulate import_export resource.fields (OrderedDict-like)
        self.fields = {i: f for i, f in enumerate(fields)}



class UniqueColumnNameTests(SimpleTestCase):

    def test_no_duplicates(self):
        fields = [
            DummyField("id"),
            DummyField("name"),
            DummyField("email"),
        ]
        resource = DummyResource(fields)

        unique_column_name(resource)

        result = [f.column_name for f in resource.fields.values()]
        self.assertEqual(result, ["id", "name", "email"])

    def test_simple_duplicates(self):
        fields = [
            DummyField("name"),
            DummyField("name"),
        ]
        resource = DummyResource(fields)

        unique_column_name(resource)

        result = [f.column_name for f in resource.fields.values()]
        self.assertEqual(result, ["name", "name_2"])

    def test_multiple_duplicates(self):
        fields = [
            DummyField("name"),
            DummyField("name"),
            DummyField("name"),
        ]
        resource = DummyResource(fields)

        unique_column_name(resource)

        result = [f.column_name for f in resource.fields.values()]
        self.assertEqual(result, ["name", "name_2", "name_3"])

    def test_mixed_duplicates(self):
        fields = [
            DummyField("id"),
            DummyField("name"),
            DummyField("name"),
            DummyField("email"),
            DummyField("name"),
        ]
        resource = DummyResource(fields)

        unique_column_name(resource)

        result = [f.column_name for f in resource.fields.values()]
        self.assertEqual(
            result,
            ["id", "name", "name_2", "email", "name_3"]
        )

    def test_already_numbered_names(self):
        fields = [
            DummyField("name"),
            DummyField("name_2"),
            DummyField("name"),
        ]
        resource = DummyResource(fields)

        unique_column_name(resource)

        result = [f.column_name for f in resource.fields.values()]

        # important behavior: check existing suffix conflicts
        self.assertEqual(result, ["name", "name_2", "name_2_1"])


# ==========


class DummyWidget:
    def __init__(self, widget):
        self.widget = widget


class DummyForm:
    def __init__(self, format_value, choices):
        self.cleaned_data = {"format": format_value}
        self.fields = {
            "format": type(
                "Field",
                (),
                {"choices": choices}
            )()
        }


class ModifyWidgetsTests(SimpleTestCase):

    def test_pdf_format_direct(self):
        fields = [
            DummyWidget(FloatWidget()),
            DummyWidget(IntegerWidget()),
            DummyWidget(CharWidget()),
        ]
        resource = DummyResource(fields)

        # capture original value for CharWidget
        original_char_value = fields[2].widget.coerce_to_string

        modify_widgets(resource, file_format="pdf")

        self.assertTrue(fields[0].widget.coerce_to_string)
        self.assertTrue(fields[1].widget.coerce_to_string)

        # ensure CharWidget was NOT modified
        self.assertEqual(fields[2].widget.coerce_to_string, original_char_value)

    def test_non_pdf_format(self):
        fields = [
            DummyWidget(FloatWidget()),
            DummyWidget(IntegerWidget()),
        ]
        resource = DummyResource(fields)

        modify_widgets(resource, file_format="xlsx")

        self.assertFalse(fields[0].widget.coerce_to_string)
        self.assertFalse(fields[1].widget.coerce_to_string)

    def test_format_from_export_form(self):
        fields = [
            DummyWidget(FloatWidget()),
            DummyWidget(IntegerWidget()),
        ]
        resource = DummyResource(fields)

        form = DummyForm(
            format_value="1",
            choices=[("1", "pdf"), ("2", "xlsx")]
        )

        modify_widgets(resource, export_form=form)

        self.assertTrue(fields[0].widget.coerce_to_string)
        self.assertTrue(fields[1].widget.coerce_to_string)

    def test_empty_format_and_no_form(self):
        fields = [
            DummyWidget(FloatWidget()),
            DummyWidget(IntegerWidget()),
        ]
        resource = DummyResource(fields)

        modify_widgets(resource)

        self.assertFalse(fields[0].widget.coerce_to_string)
        self.assertFalse(fields[1].widget.coerce_to_string)

    def test_empty_format_with_form_no_match(self):
        fields = [
            DummyWidget(FloatWidget()),
        ]
        resource = DummyResource(fields)

        form = DummyForm(
            format_value="99",
            choices=[("1", "pdf"), ("2", "xlsx")]
        )

        modify_widgets(resource, export_form=form)

        self.assertFalse(fields[0].widget.coerce_to_string)

    def test_mixed_widgets(self):
        fields = [
            DummyWidget(FloatWidget()),
            DummyWidget(CharWidget()),
            DummyWidget(IntegerWidget()),
        ]
        resource = DummyResource(fields)

        original_char_value = fields[1].widget.coerce_to_string

        modify_widgets(resource, file_format="pdf")

        self.assertTrue(fields[0].widget.coerce_to_string)
        self.assertTrue(fields[2].widget.coerce_to_string)

        # ensure CharWidget unchanged
        self.assertEqual(fields[1].widget.coerce_to_string, original_char_value)



class AppendTotalsTests(SimpleTestCase):

    class DummyObj:
        def __init__(self):
            self.totals_info = "totals"
            self.cols_info = "cols"

    class DummyQuery:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    class DummyDataset(list):
        def append(self, row):
            super().append(row)

    @patch("reports.base.report.complete_totals_data")
    def test_append_totals_basic(self, mock_totals):
        obj = self.DummyObj()

        queryset = [
            self.DummyQuery(a=1, b=2),
            self.DummyQuery(a=3, b=4),
        ]

        dataset = self.DummyDataset()

        mock_totals.return_value = [[10, 20, 30]]

        append_totals(obj, queryset, dataset)

        self.assertEqual(len(dataset), 1)
        self.assertEqual(dataset[0], ["Всього:", 20, 30])

    @patch("reports.base.report.complete_totals_data")
    def test_append_totals_zero_values(self, mock_totals):
        obj = self.DummyObj()

        queryset = [self.DummyQuery(a=1)]

        dataset = self.DummyDataset()

        mock_totals.return_value = [[0, 0, 5]]

        append_totals(obj, queryset, dataset)

        self.assertEqual(dataset[0], ["Всього:", "", 5])

    @patch("reports.base.report.complete_totals_data")
    def test_append_totals_pdf_format(self, mock_totals):
        obj = self.DummyObj()

        queryset = [self.DummyQuery(a=1)]

        dataset = self.DummyDataset()

        mock_totals.return_value = [[0, 12.5, 7.75]]

        append_totals(obj, queryset, dataset, file_format="pdf")

        self.assertEqual(dataset[0], ["Всього:", "12,5", "7,75"])

    @patch("reports.base.report.complete_totals_data")
    def test_no_totals_data(self, mock_totals):
        obj = self.DummyObj()

        queryset = [self.DummyQuery(a=1)]

        dataset = self.DummyDataset()

        mock_totals.return_value = []

        append_totals(obj, queryset, dataset)

        self.assertEqual(len(dataset), 0)

    @patch("reports.base.report.complete_totals_data")
    def test_empty_first_row(self, mock_totals):
        obj = self.DummyObj()

        queryset = [self.DummyQuery(a=1)]

        dataset = self.DummyDataset()

        mock_totals.return_value = [[]]

        append_totals(obj, queryset, dataset)

        self.assertEqual(len(dataset), 0)

    @patch("reports.base.report.complete_totals_data")
    def test_queryset_meta_removed(self, mock_totals):
        obj = self.DummyObj()

        q = self.DummyQuery(a=1)
        q._meta = "should be removed"

        queryset = [q]

        dataset = self.DummyDataset()

        mock_totals.return_value = [[1, 2]]

        append_totals(obj, queryset, dataset)

        # Just ensure it didn't crash and appended correctly
        self.assertEqual(dataset[0][0], "Всього:")



class ExportResourceDataTests(SimpleTestCase):

    def test_dict_with_datetime(self):
        dt = datetime(2025, 10, 8, 21, 31, 6)

        data = {"created": dt}

        result = export_resource_data(data)

        self.assertIsInstance(result["created"], str)
        self.assertEqual(len(result["created"].split(".")), 3)

    def test_list_with_datetime(self):
        dt = datetime(2025, 10, 8, 21, 31, 6)

        data = [dt]

        result = export_resource_data(data)

        self.assertIsInstance(result[0], str)

    def test_iso_string_parsing(self):
        data = {"created": "2025-10-08T21:31:06"}

        result = export_resource_data(data)

        self.assertIsInstance(result["created"], str)
        self.assertIn(".", result["created"])  # formatted output

    def test_invalid_string_not_changed(self):
        data = {"created": "not-a-date"}

        result = export_resource_data(data)

        self.assertEqual(result["created"], "not-a-date")

    def test_non_datetime_non_string(self):
        data = {"value": 123}

        result = export_resource_data(data)

        self.assertEqual(result["value"], 123)

    @patch("common.import_export.is_naive", return_value=True)
    @patch("common.import_export.make_aware")
    @patch("common.import_export.localtime")
    def test_naive_datetime_becomes_formatted(
        self, mock_localtime, mock_make_aware, mock_is_naive
    ):
        dt = datetime(2025, 10, 8, 21, 31, 6)

        aware_dt = datetime(2025, 10, 8, 21, 31, 6)

        mock_make_aware.return_value = aware_dt
        mock_localtime.return_value = aware_dt

        data = {"created": dt}

        result = export_resource_data(data)

        self.assertIsInstance(result["created"], str)

    @patch("common.import_export.is_naive", return_value=False)
    @patch("common.import_export.localtime")
    def test_aware_datetime_skip_make_aware(self, mock_localtime, mock_is_naive):
        dt = datetime(2025, 10, 8, 21, 31, 6)

        mock_localtime.return_value = dt

        data = {"created": dt}

        result = export_resource_data(data)

        self.assertIsInstance(result["created"], str)

    def test_mixed_dict_values(self):
        dt = datetime(2025, 10, 8, 21, 31, 6)

        data = {
            "a": dt,
            "b": "2025-10-08T21:31:06",
            "c": 100,
        }

        result = export_resource_data(data)

        self.assertIsInstance(result["a"], str)
        self.assertIsInstance(result["b"], str)
        self.assertEqual(result["c"], 100)

    def test_unsupported_type(self):
        result = export_resource_data(12345)
        self.assertEqual(result, 12345)



class DehydrateDateTimeTests(SimpleTestCase):

    def test_valid_datetime(self):
        value = datetime(2025, 7, 29, 9, 53, 27)

        result = dehydrate_date_time(value)

        self.assertEqual(result, "29.07.2025 09:53:27")

    def test_none_value(self):
        result = dehydrate_date_time(None)

        self.assertEqual(result, "")

    def test_falsey_value_empty_string(self):
        result = dehydrate_date_time("")

        self.assertEqual(result, "")

    def test_zero_like_value(self):
        # edge case: 0 is falsy
        result = dehydrate_date_time(0)

        self.assertEqual(result, "")

    def test_datetime_with_microseconds(self):
        value = datetime(2025, 7, 29, 9, 53, 27, 251029)

        result = dehydrate_date_time(value)

        self.assertEqual(result, "29.07.2025 09:53:27")

    def test_aware_datetime(self):
        # Django doesn't care about tz for strftime formatting
        value = datetime(2025, 7, 29, 9, 53, 27)

        result = dehydrate_date_time(value)

        self.assertTrue("2025" in result)
        self.assertEqual(result, "29.07.2025 09:53:27")






