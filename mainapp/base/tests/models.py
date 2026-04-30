from django.test import SimpleTestCase
from django.db import models
from ..models import *
from unittest.mock import patch


class FakeModel(models.Model):
    name = models.CharField(max_length=50)
    deleted = models.BooleanField(default=False)

    objects = BaseModelManager()

    class Meta:
        app_label = "mainapp"
        managed = False  # no DB


class BaseModelManagerTests(SimpleTestCase):

    def test_queryset_filters_deleted_false(self):
        qs = FakeModel.objects.get_queryset()

        sql = str(qs.query)

        self.assertIn('NOT "mainapp_fakemodel"."deleted"', sql)

    def test_all_uses_manager_filter(self):
        qs = FakeModel.objects.all()

        sql = str(qs.query)

        self.assertIn('NOT "mainapp_fakemodel"."deleted"', sql)

    def test_manager_always_filters(self):
        qs = FakeModel.objects.get_queryset().filter(name="test")
        sql = str(qs.query)

        self.assertIn('NOT "mainapp_fakemodel"."deleted"', sql)
        self.assertIn('"mainapp_fakemodel"."name"', sql)


# ==========


class FakeModel2(BaseModel):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = "mainapp"
        managed = False  # no DB

    @classmethod
    def get_settings(cls):
        return {"key": "value"}


class BaseModelTests(SimpleTestCase):

    def test_delete_sets_deleted_true_and_calls_save(self):
        obj = FakeModel2(name="test")
        obj.deleted = False

        with patch.object(FakeModel2, "save") as mock_save:
            obj.delete()

        self.assertTrue(obj.deleted)
        mock_save.assert_called_once()

    def test_get_settings_must_be_implemented(self):
        class NoSettingsModel(BaseModel):
            class Meta:
                app_label = "mainapp"
                managed = False

        # abstractmethod is not enforced automatically in Django models,
        # so we test the default behavior
        self.assertIsNone(NoSettingsModel.get_settings())

    def test_custom_get_settings(self):
        result = FakeModel2.get_settings()
        self.assertEqual(result, {"key": "value"})

    def test_default_deleted_field(self):
        obj = FakeModel2(name="test")
        self.assertFalse(obj.deleted)

    def test_manager_filters_deleted_false(self):
        qs = FakeModel2.objects.get_queryset()
        sql = str(qs.query)

        self.assertIn('NOT "mainapp_fakemodel2"."deleted"', sql)


# ==========



