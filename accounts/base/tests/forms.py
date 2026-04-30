from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.base.forms import BaseCustomUserCreationForm, BaseCustomUserChangeForm


User = get_user_model()


class BaseCustomUserCreationFormTests(TestCase):

    def test_meta_model(self):
        self.assertIs(BaseCustomUserCreationForm.Meta.model, User)

    def test_meta_fields(self):
        self.assertEqual(
            BaseCustomUserCreationForm.Meta.fields,
            ("email", "username"),
        )

    def test_form_valid_data(self):
        form_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        form = BaseCustomUserCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_form_password_mismatch(self):
        form_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password1": "StrongPass123!",
            "password2": "WrongPass123!",
        }

        form = BaseCustomUserCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_unique_username(self):
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123!",
        )

        form_data = {
            "email": "test2@example.com",
            "username": "testuser",  # duplicate
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        form = BaseCustomUserCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_save(self):
        form_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }

        form = BaseCustomUserCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("StrongPass123!"))


class BaseCustomUserChangeFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123!",
        )

    def test_meta_model(self):
        self.assertIs(BaseCustomUserChangeForm.Meta.model, User)

    def test_meta_fields(self):
        self.assertEqual(
            BaseCustomUserChangeForm.Meta.fields,
            ("email", "username"),
        )

    def test_form_valid_data(self):
        form_data = {
            "email": "new@example.com",
            "username": "newusername",
        }

        form = BaseCustomUserChangeForm(
            data=form_data,
            instance=self.user,
        )

        self.assertTrue(form.is_valid())

    def test_form_missing_fields(self):
        form = BaseCustomUserChangeForm(
            data={},
            instance=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertNotIn("email", form.errors)
        self.assertIn("username", form.errors)

    def test_form_unique_username(self):
        User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="StrongPass123!",
        )

        form_data = {
            "email": "test@example.com",
            "username": "existinguser",  # duplicate
        }

        form = BaseCustomUserChangeForm(
            data=form_data,
            instance=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_form_save(self):
        form_data = {
            "email": "updated@example.com",
            "username": "updateduser",
        }

        form = BaseCustomUserChangeForm(
            data=form_data,
            instance=self.user,
        )

        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertEqual(user.email, "updated@example.com")
        self.assertEqual(user.username, "updateduser")