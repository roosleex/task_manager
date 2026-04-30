from django.test import SimpleTestCase
from django import forms
from ..restricted_select import *
from django.db import models


class RestrictedSelectTests(SimpleTestCase):

    def test_media_includes_custom_js(self):
        widget = RestrictedSelect()
        media = widget.media

        self.assertIn("js/forms/restricted_select_loader.js", media._js)

    def test_media_preserves_parent_media(self):
        widget = RestrictedSelect()
        media = widget.media

        parent_media = super(RestrictedSelect, widget).media

        for js_file in parent_media._js:
            self.assertIn(js_file, media._js)

    def test_media_is_combined_correctly(self):
        widget = RestrictedSelect()
        media = widget.media

        # Ensure it's not just the custom file
        self.assertGreaterEqual(len(media._js), 1)

        # Ensure our file is last (since += appends)
        self.assertEqual(media._js[-1], "js/forms/restricted_select_loader.js")

    def test_multiple_access_returns_consistent_media(self):
        widget = RestrictedSelect()

        media1 = widget.media
        media2 = widget.media

        self.assertEqual(media1._js, media2._js)


# ==========
# BoundRestrictedModelChoiceField


class FakeRestrictedField(forms.Field):
    def __init__(self, *args, **kwargs):
        self.restrict_on_form_field = "parent"
        self.restrict_on_relation = "category"
        self.restricted_select_model_name = "product"
        self.restricted_select_model_app_label = "shop"
        self.restricted_select_name = "child"
        self.clear_restricted_selects_onevent = "child"
        self.select_name_with_param_for_curr_select_load = "parent_id"
        super().__init__(*args, **kwargs)

    def get_bound_field(self, form, field_name):
        return BoundRestrictedModelChoiceField(form, self, field_name)


class TestForm(forms.Form):
    parent = forms.CharField()
    child = FakeRestrictedField()


class BoundRestrictedModelChoiceFieldTests(SimpleTestCase):

    def setUp(self):
        self.form = TestForm()
        self.bound_field = self.form["child"]

    def test_build_widget_attrs_adds_custom_attributes(self):
        attrs = {}
        result = self.bound_field.build_widget_attrs(attrs)

        self.assertEqual(result["restrict_on_form_field"], "parent")
        self.assertEqual(result["restrict_on_relation"], "category")
        self.assertEqual(result["restricted_select_model_name"], "product")
        self.assertEqual(result["restricted_select_model_app_label"], "shop")
        self.assertEqual(result["restricted_select_name"], "child")
        self.assertEqual(result["clear_restricted_selects_onevent"], "child")
        self.assertEqual(
            result["select_name_with_param_for_curr_select_load"], "parent_id"
        )

    def test_uses_parent_field_html_name(self):
        attrs = {}
        result = self.bound_field.build_widget_attrs(attrs)

        parent_bound = self.form["parent"]
        self.assertEqual(
            result["restrict_on_form_field"],
            parent_bound.html_name
        )

    def test_preserves_existing_attrs(self):
        attrs = {"class": "form-control"}
        result = self.bound_field.build_widget_attrs(attrs)

        self.assertIn("class", result)
        self.assertEqual(result["class"], "form-control")

    def test_returns_new_attrs_dict(self):
        attrs = {}
        result = self.bound_field.build_widget_attrs(attrs)

        self.assertIsInstance(result, dict)

    def test_multiple_calls_consistent(self):
        attrs1 = self.bound_field.build_widget_attrs({})
        attrs2 = self.bound_field.build_widget_attrs({})

        self.assertEqual(attrs1, attrs2)


# ==========
# RestrictedModelChoiceField


class FakeModel3(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = "mainapp"
        managed = False  # no DB


class RestrictedModelChoiceFieldTests(SimpleTestCase):

    def get_field(self, **kwargs):
        return RestrictedModelChoiceField(
            queryset=FakeModel3.objects.none(),
            **kwargs
        )

    def test_defaults_are_empty_strings(self):
        field = self.get_field()

        self.assertEqual(field.restrict_on_form_field, "")
        self.assertEqual(field.restrict_on_relation, "")
        self.assertEqual(field.restricted_select_model_name, "")
        self.assertEqual(field.restricted_select_model_app_label, "")
        self.assertEqual(field.restricted_select_name, "")
        self.assertEqual(field.clear_restricted_selects_onevent, "")
        self.assertEqual(field.select_name_with_param_for_curr_select_load, "")

    def test_custom_values_are_set(self):
        field = self.get_field(
            restrict_on_form_field="parent",
            restrict_on_relation="category",
            restricted_select_model_name="product",
            restricted_select_model_app_label="shop",
            restricted_select_name="child",
            clear_restricted_selects_onevent="child",
            select_name_with_param_for_curr_select_load="parent_id",
        )

        self.assertEqual(field.restrict_on_form_field, "parent")
        self.assertEqual(field.restrict_on_relation, "category")
        self.assertEqual(field.restricted_select_model_name, "product")
        self.assertEqual(field.restricted_select_model_app_label, "shop")
        self.assertEqual(field.restricted_select_name, "child")
        self.assertEqual(field.clear_restricted_selects_onevent, "child")
        self.assertEqual(
            field.select_name_with_param_for_curr_select_load, "parent_id"
        )

    def test_none_values_are_converted_to_empty_strings(self):
        field = self.get_field(
            restrict_on_form_field=None,
            restrict_on_relation=None,
            restricted_select_model_name=None,
            restricted_select_model_app_label=None,
            restricted_select_name=None,
            clear_restricted_selects_onevent=None,
            select_name_with_param_for_curr_select_load=None,
        )

        self.assertEqual(field.restrict_on_form_field, "")
        self.assertEqual(field.restrict_on_relation, "")
        self.assertEqual(field.restricted_select_model_name, "")
        self.assertEqual(field.restricted_select_model_app_label, "")
        self.assertEqual(field.restricted_select_name, "")
        self.assertEqual(field.clear_restricted_selects_onevent, "")
        self.assertEqual(
            field.select_name_with_param_for_curr_select_load, ""
        )

    def test_widget_is_restricted_select(self):
        field = self.get_field()
        self.assertEqual(field.widget.__class__.__name__, "RestrictedSelect")

    def test_get_bound_field_returns_custom_class(self):
        field = self.get_field()

        class TestForm(forms.Form):
            test = field

        form = TestForm()
        bound = form["test"]

        self.assertIsInstance(bound, BoundRestrictedModelChoiceField)

    def test_field_works_inside_form(self):
        field = self.get_field(restrict_on_form_field="parent")

        class TestForm(forms.Form):
            parent = forms.CharField()
            child = field

        form = TestForm()
        bound = form["child"]

        attrs = bound.build_widget_attrs({})

        self.assertIn("restrict_on_form_field", attrs)
        self.assertEqual(attrs["restrict_on_form_field"], "parent")


# ==========


