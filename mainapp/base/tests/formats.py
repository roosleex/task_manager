from django.test import SimpleTestCase
from ..formats  import *
from ..formats import _insert_line_breaks
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO


class CleanCellTests(SimpleTestCase):

    def test_none_returns_empty_string(self):
        self.assertEqual(clean_cell(None), "")

    def test_string_none_lowercase(self):
        self.assertEqual(clean_cell("none"), "")

    def test_string_none_uppercase(self):
        self.assertEqual(clean_cell("NONE"), "")

    def test_string_none_mixed_case(self):
        self.assertEqual(clean_cell("NoNe"), "")

    def test_string_none_with_spaces(self):
        self.assertEqual(clean_cell("  none  "), "")

    def test_normal_string_returns_same_value(self):
        self.assertEqual(clean_cell("hello"), "hello")

    def test_empty_string_returns_empty_string(self):
        self.assertEqual(clean_cell(""), "")

    def test_whitespace_only_string_returns_whitespace(self):
        # function does NOT strip general strings, only "none"
        self.assertEqual(clean_cell("   "), "   ")

    def test_integer_returns_same_value(self):
        self.assertEqual(clean_cell(123), 123)

    def test_boolean_returns_same_value(self):
        self.assertEqual(clean_cell(True), True)

    def test_float_returns_same_value(self):
        self.assertEqual(clean_cell(12.5), 12.5)


class InsertLineBreaksTests(SimpleTestCase):

    def test_short_text_no_change(self):
        text = "one two"
        result = _insert_line_breaks(text, words_per_line=2)

        self.assertEqual(result, "one two")

    def test_exact_limit_no_change(self):
        text = "one two"
        result = _insert_line_breaks(text, words_per_line=2)

        self.assertEqual(result, "one two")

    def test_three_words_split_default_two(self):
        text = "one two three"
        result = _insert_line_breaks(text, words_per_line=2)

        self.assertEqual(result, "one two\nthree")

    def test_four_words_split_default_two(self):
        text = "one two three four"
        result = _insert_line_breaks(text, words_per_line=2)

        self.assertEqual(result, "one two\nthree four")

    def test_custom_words_per_line(self):
        text = "one two three four five six"
        result = _insert_line_breaks(text, words_per_line=3)

        self.assertEqual(result, "one two three\nfour five six")

    def test_single_word(self):
        text = "hello"
        result = _insert_line_breaks(text, words_per_line=2)

        self.assertEqual(result, "hello")

    def test_empty_string(self):
        text = ""
        result = _insert_line_breaks(text)

        self.assertEqual(result, "")

    def test_none_input(self):
        # function converts to "None"
        result = _insert_line_breaks(None)

        self.assertEqual(result, None)

    def test_non_string_input(self):
        result = _insert_line_breaks(12345, words_per_line=2)

        self.assertEqual(result, 12345)


# ==========
# PDF


class PDFTests(SimpleTestCase):

    def test_title(self):
        self.assertEqual(PDF().get_title(), "pdf")

    def test_extension(self):
        self.assertEqual(PDF().get_extension(), "pdf")

    def test_content_type(self):
        self.assertEqual(PDF().get_content_type(), "application/pdf")

    def test_can_export(self):
        self.assertTrue(PDF().can_export())

    def test_can_import(self):
        self.assertFalse(PDF().can_import())

    def make_dataset(self):
        dataset = Mock()
        dataset.headers = ["A", "B"]

        dataset.dict = [
            {"A": "a1", "B": "b1"},
            {"A": "a2", "B": "b2"},
        ]
        return dataset
    
    # @patch("reportlab.platypus.SimpleDocTemplate")
    # @patch("reportlab.platypus.Table")
    # @patch("reportlab.platypus.TableStyle")
    # @patch("reportlab.pdfbase.ttfonts.TTFont")
    # @patch("reportlab.pdfbase.pdfmetrics.registerFont")
    # @patch("mainapp.base.formats.os.path.join", return_value="/fake/font.ttf")
    # @patch("common.import_export.is_report_resource", return_value=False)
    # @patch("mainapp.base.formats.clean_cell", side_effect=lambda x: x)
    # def test_export_data_basic(
    #     self,
    #     mock_clean,
    #     mock_report,
    #     mock_join,
    #     mock_register,
    #     mock_table_style,
    #     mock_table,
    #     mock_doc,
    #     mock_ttfont,
    # ):
    #     pdf = PDF()
    #     dataset = self.make_dataset()

    #     mock_buffer = MagicMock()
    #     mock_doc.return_value = MagicMock()
    #     mock_doc.return_value.build.return_value = None

    #     with patch("io.BytesIO", return_value=mock_buffer):
    #         mock_buffer.getvalue.return_value = b"PDF-DATA"

    #         result = pdf.export_data(dataset)

    #         self.assertEqual(result, b"PDF-DATA")
    #         mock_doc.return_value.build.assert_called_once()

    # @patch("common.import_export.is_report_resource", return_value=True)
    # @patch("reportlab.platypus.SimpleDocTemplate")
    # @patch("reportlab.platypus.Table")
    # @patch("reportlab.platypus.TableStyle")
    # @patch("reportlab.pdfbase.pdfmetrics.registerFont")
    # @patch("mainapp.base.formats.os.path.join", return_value="/fake/font.ttf")
    # @patch("mainapp.base.formats.clean_cell", side_effect=lambda x: x)
    # def test_export_data_totals_row(
    #     self,
    #     mock_clean,
    #     mock_join,
    #     mock_register,
    #     mock_table_style,
    #     mock_table,
    #     mock_doc,
    #     mock_is_report
    # ):
    #     pdf = PDF()

    #     dataset = self.make_dataset()

    #     mock_buffer = MagicMock()
    #     mock_doc.return_value = MagicMock()
    #     mock_doc.return_value.build.return_value = None

    #     with patch("io.BytesIO", return_value=mock_buffer):
    #         mock_buffer.getvalue.return_value = b"PDF"

    #         result = pdf.export_data(dataset, resource=Mock())

    #         self.assertEqual(result, b"PDF")
    #         mock_is_report.assert_called_once()

    # def test_dataset_is_iterated(self):
    #     pdf = PDF()
    #     dataset = self.make_dataset()

    #     with patch("reportlab.platypus.SimpleDocTemplate") as doc, \
    #         patch("reportlab.platypus.Table"), \
    #         patch("reportlab.platypus.TableStyle"), \
    #         patch("reportlab.pdfbase.pdfmetrics.registerFont"), \
    #         patch("os.path.join", return_value="/fake"), \
    #         patch("mainapp.base.formats.clean_cell", side_effect=lambda x: x), \
    #         patch("common.import_export.is_report_resource", return_value=False), \
    #         patch("io.BytesIO") as bio:

    #         bio.return_value.getvalue.return_value = b"x"

    #         pdf.export_data(dataset)

    #         # ensure dataset accessed
    #         self.assertEqual(len(dataset.dict), 2)	


# ==========
# XLSX


def make_ws():
    ws = MagicMock()

    # header row (row 1)
    cell1 = MagicMock()
    cell1.value = "Header1"
    cell1.column_letter = "A"

    cell2 = MagicMock()
    cell2.value = "Header2"
    cell2.column_letter = "B"

    ws.__getitem__.return_value = [cell1, cell2]

    # columns iteration
    ws.columns = [[cell1], [cell2]]

    ws.column_dimensions = {
        "A": MagicMock(width=10),
        "B": MagicMock(width=10),
    }

    ws.row_dimensions = {}

    return ws


# class XLSXTests(SimpleTestCase):

#     @patch("mainapp.base.formats.load_workbook")
#     @patch("mainapp.base.formats.BytesIO")
#     @patch("mainapp.base.formats._insert_line_breaks", side_effect=lambda x, **k: x)
#     @patch("mainapp.base.formats.clean_cell", side_effect=lambda x: x)
#     def test_export_data_basic(
#         self,
#         mock_clean,
#         mock_breaks,
#         mock_bytesio,
#         mock_load_wb,
#     ):
#         xlsx = XLSX()

#         dataset = Mock()
#         dataset.headers = ["H1", "H2"]

#         # mock super().export_data
#         with patch.object(
#             XLSX.__bases__[0],
#             "export_data",
#             return_value=b"binary-xlsx",
#         ):
#             mock_stream = MagicMock()
#             mock_bytesio.return_value = mock_stream

#             wb = MagicMock()
#             ws = make_ws()
#             wb.active = ws
#             mock_load_wb.return_value = wb

#             result = xlsx.export_data(dataset)

#             self.assertIsInstance(result, bytes)
#             self.assertTrue(len(result) > 0)


# ==========



