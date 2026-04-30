from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UserGroup



#Tests for User model
class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="will", email="will@email.com", password="testpass123",
            tel="0981122333"
        )
        cls.admin_user = User.objects.create_superuser(
            username="superadmin", email="superadmin@email.com", password="testpass123",
            tel="0961617333"
        )
        cls.row = cls.user     
    
    def test_constants(self):
        pass

    def test_fields(self):
        self.assertEqual(self.row._meta.get_field("tel").verbose_name, "Номер телефону")
        self.assertEqual(self.row._meta.get_field("tel").max_length, 15)
        # self.assertTrue(self.row.history != None)

    def test_model_meta(self):
        self.assertEqual(self.row._meta.db_table, 'auth_user')
        self.assertEqual(self.row._meta.verbose_name, "користувач")
        self.assertEqual(self.row._meta.verbose_name_plural, "користувачі")
        self.assertEqual(self.row._meta.ordering, ["-id"])

    def test_model_content(self):
        self.assertEqual(self.user.username, "will")
        self.assertEqual(self.user.email, "will@email.com")
        self.assertEqual(self.user.tel, "0981122333")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        # self.assertTrue(self.user.history != None)
        #
        self.assertEqual(self.admin_user.username, "superadmin")
        self.assertEqual(self.admin_user.email, "superadmin@email.com")
        self.assertEqual(self.admin_user.tel, "0961617333")
        self.assertTrue(self.admin_user.is_active)
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)
        # self.assertTrue(self.admin_user.history != None)
       
    def test_str(self):
        self.assertEqual(self.user.__str__(), self.user.username)
        self.assertEqual(self.admin_user.__str__(), self.admin_user.username)

    

#Tests for UserGroup model
class UserGroupTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.row = UserGroup.objects.create(name="Група 1", description="Опис групи 1")   
    
    def test_constants(self):
        pass

    def test_fields(self):
        self.assertEqual(self.row._meta.get_field("description").verbose_name, "Опис")
        self.assertEqual(self.row._meta.get_field("description").max_length, 250)
        self.assertEqual(self.row._meta.get_field("description").null, True)
        self.assertEqual(self.row._meta.get_field("description").blank, True)
        # self.assertTrue(self.row.history != None)

    def test_model_meta(self):
        self.assertEqual(self.row._meta.verbose_name, "група")
        self.assertEqual(self.row._meta.verbose_name_plural, "групи")
        self.assertEqual(self.row._meta.ordering, ["-id"])

    def test_model_content(self):
        self.assertEqual(self.row.name, "Група 1")
        self.assertEqual(self.row.description, "Опис групи 1")
        # self.assertTrue(self.row.history != None)
       
    def test_str(self):
        self.assertEqual(self.row.__str__(), self.row.name)



     
        
