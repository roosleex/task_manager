from django.test import SimpleTestCase, RequestFactory
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import Group
from django.contrib.admin.sites import AdminSite

from accounts.base.admin import (
    BaseCustomGroupAdmin,
    BaseCustomUserAdmin,
)

from django.contrib.auth import get_user_model
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
User = get_user_model()


class DummyAdminSite(AdminSite):
    pass


class BaseCustomGroupAdminTests(SimpleTestCase):
    def setUp(self):
        self.site = DummyAdminSite()
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.admin = BaseCustomGroupAdmin(Group, self.site)

    @patch("accounts.base.admin.settings")
    @patch("django.contrib.auth.admin.GroupAdmin.get_actions")
    def test_get_actions_delete_disabled(self, mock_super, mock_settings):
        mock_settings.USER_GROUP_CONFIG = {
            "fields": [],
            "list_display": [],
            "is_delete_selected_action": False,
        }

        mock_super.return_value = {
            "delete_selected": "delete_action",
            "other_action": "something",
        }

        actions = self.admin.get_actions(self.request)

        self.assertNotIn("delete_selected", actions)
        self.assertIn("other_action", actions)

    @patch("accounts.base.admin.settings")
    @patch("django.contrib.auth.admin.GroupAdmin.get_actions")
    def test_get_actions_delete_enabled(self, mock_super, mock_settings):
        mock_settings.USER_GROUP_CONFIG = {
            "fields": [],
            "list_display": [],
            "is_delete_selected_action": True,
        }

        mock_super.return_value = {
            "delete_selected": "delete_action",
            "other_action": "something",
        }

        actions = self.admin.get_actions(self.request)

        self.assertIn("delete_selected", actions)
        self.assertIn("other_action", actions)


class BaseCustomUserAdminTests(SimpleTestCase):
    def setUp(self):
        self.site = DummyAdminSite()
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.admin = BaseCustomUserAdmin(User, self.site)

    @patch("accounts.base.admin.settings")
    @patch("django.contrib.auth.admin.UserAdmin.get_actions")
    def test_get_actions_delete_disabled(self, mock_super, mock_settings):
        mock_settings.USER_CONFIG = {
            "list_display": ["username"],
            "is_delete_selected_action": False,
        }

        mock_super.return_value = {
            "delete_selected": "delete_action",
            "other_action": "something",
        }

        actions = self.admin.get_actions(self.request)

        self.assertNotIn("delete_selected", actions)
        self.assertIn("other_action", actions)

    @patch("accounts.base.admin.settings")
    @patch("django.contrib.auth.admin.UserAdmin.get_actions")
    def test_get_actions_delete_enabled(self, mock_super, mock_settings):
        mock_settings.USER_CONFIG = {
            "list_display": ["username"],
            "is_delete_selected_action": True,
        }

        mock_super.return_value = {
            "delete_selected": "delete_action",
            "other_action": "something",
        }

        actions = self.admin.get_actions(self.request)

        self.assertIn("delete_selected", actions)
        self.assertIn("other_action", actions)

    def test_forms_are_assigned(self):
        self.assertIs(self.admin.add_form, CustomUserCreationForm)
        self.assertIs(self.admin.form, CustomUserChangeForm)

    def test_model_is_correct(self):
        self.assertIs(self.admin.model, User)

    def test_add_fieldsets_structure(self):
        fieldsets = self.admin.add_fieldsets

        self.assertEqual(len(fieldsets), 1)
        name, opts = fieldsets[0]

        self.assertIsNone(name)
        self.assertIn("username", opts["fields"])
        self.assertIn("password1", opts["fields"])
        self.assertIn("password2", opts["fields"])

    def test_fieldsets_contains_tel(self):
        """
        Ensure 'tel' field is appended to fieldsets
        """
        all_fields = []

        for _, opts in self.admin.fieldsets:
            all_fields.extend(opts.get("fields", []))

        self.assertIn("tel", all_fields)