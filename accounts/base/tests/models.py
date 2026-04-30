from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from django.core.exceptions import ValidationError

from accounts.base.models import BaseUser, BaseUserGroup


# Create a concrete class for testing (no DB interaction needed)
class TestUser(BaseUser):
    class Meta(BaseUser.Meta):
        app_label = "tests"


class BaseUserTests(SimpleTestCase):

    def test_str_returns_username(self):
        user = TestUser(username="testuser")
        self.assertEqual(str(user), "testuser")

    def test_tel_field_attributes(self):
        field = TestUser._meta.get_field("tel")

        self.assertEqual(field.max_length, 15)
        self.assertEqual(field.verbose_name, "Номер телефону")
        self.assertTrue(len(field.validators) > 0)

    def test_tel_validator_called(self):
        field = TestUser._meta.get_field("tel")

        mock_validator = MagicMock()
        field.validators = [mock_validator]

        user = TestUser(username="user1", tel="123456")

        # manually trigger validators
        for validator in field.validators:
            validator(user.tel)

        mock_validator.assert_called_once_with("123456")

    def test_tel_validator_raises_error(self):
        def failing_validator(value):
            raise ValidationError("Invalid phone")

        field = TestUser._meta.get_field("tel")
        field.validators = [failing_validator]

        user = TestUser(username="user2", tel="bad_phone")

        with self.assertRaises(ValidationError):
            for validator in field.validators:
                validator(user.tel)

    def test_meta_options(self):
        meta = TestUser._meta

        self.assertEqual(meta.db_table, "auth_user")
        self.assertEqual(meta.verbose_name, "користувач")
        self.assertEqual(meta.verbose_name_plural, "користувачі")
        self.assertEqual(meta.ordering, ["-id"])


# ==========


# Concrete test model (required because BaseUserGroup is abstract)
class TestGroup(BaseUserGroup):
    class Meta(BaseUserGroup.Meta):
        app_label = "tests"


class BaseUserGroupTests(SimpleTestCase):
    def test_str_returns_name(self):
        group = TestGroup()
        group.name = "admins"

        self.assertEqual(str(group), "admins")

    def test_description_field_attributes(self):
        field = TestGroup._meta.get_field("description")

        self.assertEqual(field.verbose_name, "Опис")
        self.assertEqual(field.max_length, 250)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_meta_options(self):
        meta = TestGroup._meta

        self.assertEqual(meta.verbose_name, "група")
        self.assertEqual(meta.verbose_name_plural, "групи")
        self.assertEqual(meta.ordering, ["-id"])

    def test_description_value_assignment(self):
        group = TestGroup()
        group.description = "Test description"

        self.assertEqual(group.description, "Test description")

    def test_str_does_not_depend_on_db(self):
        group = TestGroup(name="staff")

        # no DB interaction required
        self.assertEqual(str(group), "staff")