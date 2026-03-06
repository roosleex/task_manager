from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from ..view_utils import *



class ViewUtilsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="will", email="will@email.com", password="testpass123",
            tel="0981122333", is_staff=True, is_active=True,
        )

    def test_is_trusted_user(self):
        actual = is_trusted_user(self.user)
        self.assertTrue(actual)

        actual = is_trusted_user(AnonymousUser())
        self.assertFalse(actual)

        actual = is_trusted_user(None)
        self.assertFalse(actual)

        actual = is_trusted_user("")
        self.assertFalse(actual)

        actual = is_trusted_user(False)
        self.assertFalse(actual)







