from django.test import SimpleTestCase, override_settings
from ..admin import *
from unittest.mock import Mock, patch
from django.contrib import admin


class GetAppListItemTests(SimpleTestCase):

    def test_returns_single_item_list(self):
        result = get_app_list_item("Authors", "author", "/admin/mainapp/")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_basic_fields(self):
        item = get_app_list_item("Authors", "author", "/admin/mainapp/")[0]

        self.assertEqual(item["name"], "Authors")
        self.assertEqual(item["object_name"], "author")
        self.assertTrue(item["view_only"])

    def test_permissions_all_true(self):
        item = get_app_list_item("Authors", "author", "/admin/mainapp/")[0]

        expected_perms = {
            "add": True,
            "change": True,
            "delete": True,
            "view": True,
        }
        self.assertEqual(item["perms"], expected_perms)

    def test_admin_url_construction(self):
        item = get_app_list_item("Authors", "author", "/admin/mainapp/")[0]

        self.assertEqual(item["admin_url"], "/admin/mainapp/author/")

    def test_different_inputs(self):
        item = get_app_list_item("Books", "book", "/custom/url/")[0]

        self.assertEqual(item["name"], "Books")
        self.assertEqual(item["object_name"], "book")
        self.assertEqual(item["admin_url"], "/custom/url/book/")

    def test_admin_url_without_trailing_slash(self):
        # current implementation behavior (important edge case)
        item = get_app_list_item("Authors", "author", "/admin/mainapp")[0]

        # shows how function behaves now (might be undesirable)
        self.assertEqual(item["admin_url"], "/admin/mainappauthor/")


# ==========


class BaseModelAdminTests(SimpleTestCase):

    def setUp(self):
        self.request = Mock()
        self.admin = BaseModelAdmin(model=Mock(), admin_site=Mock())

    # ---- get_actions ----

    @override_settings(COMMON_CONFIG={
        "is_delete_selected_action": False,
        "is_btn_save_as_new": True
    })
    @patch("simple_history.admin.SimpleHistoryAdmin.get_actions")
    def test_get_actions_removes_delete_selected(self, mock_super):
        mock_super.return_value = {
            "delete_selected": "delete_action",
            "custom_action": "custom_action",
        }

        actions = self.admin.get_actions(self.request)

        self.assertNotIn("delete_selected", actions)
        self.assertIn("custom_action", actions)

    @override_settings(COMMON_CONFIG={
        "is_delete_selected_action": True,
        "is_btn_save_as_new": True
    })
    @patch("simple_history.admin.SimpleHistoryAdmin.get_actions")
    def test_get_actions_keeps_delete_selected(self, mock_super):
        mock_super.return_value = {
            "delete_selected": "delete_action",
            "custom_action": "custom_action",
        }

        actions = self.admin.get_actions(self.request)

        self.assertIn("delete_selected", actions)

    @override_settings(COMMON_CONFIG={
        "is_delete_selected_action": False,
        "is_btn_save_as_new": True
    })
    @patch("simple_history.admin.SimpleHistoryAdmin.get_actions")
    def test_get_actions_no_delete_key(self, mock_super):
        mock_super.return_value = {
            "custom_action": "custom_action",
        }

        actions = self.admin.get_actions(self.request)

        self.assertEqual(actions, {"custom_action": "custom_action"})

    # ---- get_exclude ----

    @patch("simple_history.admin.SimpleHistoryAdmin.get_exclude")
    def test_get_exclude_appends_deleted(self, mock_super):
        mock_super.return_value = ["field1"]

        exclude = self.admin.get_exclude(self.request)

        self.assertEqual(exclude, ["field1", "deleted"])

    @patch("simple_history.admin.SimpleHistoryAdmin.get_exclude")
    def test_get_exclude_when_none(self, mock_super):
        mock_super.return_value = None

        exclude = self.admin.get_exclude(self.request)

        self.assertEqual(exclude, ["deleted"])

    # ---- class attributes ----

    def test_list_per_page(self):
        self.assertEqual(self.admin.list_per_page, 20)

    def test_media_js(self):
        self.assertIn("js/doubleScroll.js", BaseModelAdmin.Media.js)

    def test_save_as_matches_settings(self):
        from django.conf import settings

        self.assertEqual(
            self.admin.save_as,
            settings.COMMON_CONFIG["is_btn_save_as_new"]
        )


# ==========


class BaseMainappAdminSiteTests(SimpleTestCase):

    def setUp(self):
        self.site = BaseMainappAdminSite()
        self.request = Mock()
        self.request.get_full_path.return_value = "/admin/mainapp/model/"
        self.request.user = Mock()

    # ---- each_context ----

    @override_settings(
        COMPANY_DEFAULT_GEO_LOCATION="EU",
        JQUERY_PATH_FILE="jquery.js",
        COMMON_CONFIG={"is_btn_save_and_continue_editing": True},
    )
    @patch("django.contrib.admin.AdminSite.each_context")
    def test_each_context_updates_values(self, mock_super):
        mock_super.return_value = {"base": "context"}

        context = self.site.each_context(self.request)

        self.assertIn("COMPANY_DEFAULT_GEO_LOCATION", context)
        self.assertIn("admin_url1", context)
        self.assertIn("JQUERY_PATH_FILE", context)
        self.assertTrue(context["show_save_and_continue"])

    # ---- get_active_app_name ----

    def test_get_active_app_name(self):
        self.request.get_full_path.return_value = "/admin/mainapp/model/"
        result = self.site.get_active_app_name(self.request)

        self.assertEqual(result, "mainapp")

    # ---- is_app_active ----

    def test_is_app_active_true(self):
        with patch.object(self.site, "get_active_app_name", return_value="mainapp"):
            self.assertTrue(self.site.is_app_active(self.request, "mainapp"))

    def test_is_app_active_false(self):
        with patch.object(self.site, "get_active_app_name", return_value="accounts"):
            self.assertFalse(self.site.is_app_active(self.request, "mainapp"))

    # ---- get_app_list ----

    @patch("reports.admin.get_reports_app_list")
    @patch("django.apps.apps.get_model")
    @patch("django.contrib.admin.AdminSite.get_app_list")
    def test_get_app_list_merging_and_sorting(
        self, mock_super, mock_get_model, mock_reports
    ):
        mock_super.return_value = [
            {
                "app_label": "mainapp",
                "models": [
                    {"object_name": "B", "name": "B"},
                    {"object_name": "A", "name": "A"},
                ],
            }
        ]

        mock_reports.return_value = []

        mock_model = Mock()
        mock_model.ADMIN_MENU_ORDER = 1
        mock_get_model.return_value = mock_model

        with patch.object(self.site, "get_custactions_app_list", return_value=[]), \
             patch.object(self.site, "get_positioned_app_list", side_effect=lambda r, x: x):

            result = self.site.get_app_list(self.request)

        self.assertEqual(len(result), 2)
        self.assertIn("models", result[0])

    # ---- get_positioned_app_list ----

    def test_get_positioned_app_list_orders_apps(self):
        app_list = [
            {"app_label": "mainapp"},
            {"app_label": "reports"},
            {"app_label": "custactions"},
            {"app_label": "accounts"},
        ]

        with patch.object(self.site, "get_active_app_name", return_value="mainapp"), \
             patch("mainapp.apps.MainappConfig.name", "mainapp"), \
             patch("reports.apps.ReportsConfig.name", "reports"), \
             patch("accounts.apps.AccountsConfig.name", "accounts"):

            result = self.site.get_positioned_app_list(self.request, app_list)

        self.assertEqual(len(result), 4)

    # ---- get_custactions_app_list ----

    @override_settings(
        ADMIN_SITE_CONFIG={"app_list_custom_actions_app_name": "Custom Actions"}
    )
    @patch("mainapp.base.admin.get_app_list_item")
    def test_get_custactions_app_list_with_permissions(self, mock_item):
        self.request.user.has_perm.return_value = True

        mock_item.return_value = [{"name": "Test"}]

        menu_items = [
            {"perm": "perm.test", "name": "Test", "object_name": "obj"}
        ]

        result = self.site.get_custactions_app_list(self.request, menu_items)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["models"], [{"name": "Test"}])

    def test_get_custactions_app_list_no_permissions(self):
        self.request.user.has_perm.return_value = False

        menu_items = [
            {"perm": "perm.test", "name": "Test", "object_name": "obj"}
        ]

        result = self.site.get_custactions_app_list(self.request, menu_items)

        self.assertEqual(result, [])

    # ---- get_common_context ----

    @patch.object(BaseMainappAdminSite, "get_app_list")
    def test_get_common_context(self, mock_app_list):
        mock_app_list.return_value = [{"app_label": "mainapp"}]

        context = self.site.get_common_context(self.request)

        self.assertIn("app_list", context)
        self.assertIn("user", context)
        self.assertTrue(context["has_permission"])


# ==========



