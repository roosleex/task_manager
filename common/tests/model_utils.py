from django.test import TestCase, SimpleTestCase
from django.db import models
from django.apps import apps
from ..model_utils import *
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib import admin
from unittest.mock import Mock, patch


# --- Test models ---
class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я автора")

    class Meta:
        app_label = "mainapp"


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="Назва книги")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name="Ім'я автора"
    )

    class Meta:
        app_label = "mainapp"


# Register models dynamically (important for tests)
apps.register_model("mainapp", Author)
apps.register_model("mainapp", Book)


# --- Tests ---
class GetFieldsVerboseNamesTests(TestCase):

    def test_empty_inputs(self):
        self.assertEqual(get_fields_verbose_names("", "mainapp"), {})
        self.assertEqual(get_fields_verbose_names("Book", ""), {})
        self.assertEqual(get_fields_verbose_names(None, "mainapp"), {})

    def test_basic_fields(self):
        result = get_fields_verbose_names("Book", "mainapp")

        self.assertIn("title", result)
        self.assertEqual(result["title"], "Назва книги")

    def test_foreign_key_field(self):
        result = get_fields_verbose_names("Book", "mainapp")

        self.assertIn("author", result)
        self.assertEqual(result["author"], "Ім'я автора")

    def test_reverse_relation_many_to_one(self):
        result = get_fields_verbose_names("Author", "mainapp")

        # reverse FK: books
        self.assertIn("books", result)
        self.assertEqual(result["books"], "Ім'я автора")

    def test_mode_capitalize(self):
        result = get_fields_verbose_names("Book", "mainapp", mode=1)

        self.assertEqual(result["title"], "Назва книги")

    def test_mode_upper(self):
        result = get_fields_verbose_names("Book", "mainapp", mode=2)

        self.assertEqual(result["title"], "НАЗВА КНИГИ")

    def test_mode_lower(self):
        result = get_fields_verbose_names("Book", "mainapp", mode=3)

        self.assertEqual(result["title"], "назва книги")

    def test_invalid_model(self):
        with self.assertRaises(LookupError):
            get_fields_verbose_names("InvalidModel", "mainapp")


# ==========


class GetPersonNameValidatorTests(SimpleTestCase):

    def setUp(self):
        self.validators = get_person_name_validator()

    def test_returns_list_with_validator(self):
        self.assertIsInstance(self.validators, list)
        self.assertEqual(len(self.validators), 1)
        self.assertIsInstance(self.validators[0], RegexValidator)

    def test_valid_names(self):
        validator = self.validators[0]

        valid_names = [
            "Іван",
            "Іван Петренко",
            "О'Браєн",
            "Анна-Марія",
            "Юрій І. Петров",
            "Єва",
            "Петренко Іван Васильович",
            "Петренко І В",
            "Петренко І. В.",
            "Петренко І.В.",
        ]

        for name in valid_names:
            try:
                validator(name)
            except ValidationError:
                self.fail(f"ValidationError raised for valid name: {name}")

    def test_invalid_names(self):
        validator = self.validators[0]

        invalid_names = [
            "John",          # latin
            "123",           # digits
            "Іван123",       # mixed
            "Іван@",         # special char
            "Anna!",         # invalid symbol
        ]

        for name in invalid_names:
            with self.assertRaises(ValidationError):
                validator(name)

    def test_error_message_and_code(self):
        validator = self.validators[0]

        with self.assertRaises(ValidationError) as context:
            validator("John")

        error = context.exception

        self.assertEqual(error.code, "invalid_person_name")
        self.assertEqual(error.message, "Невірне значення")


# ==========


class GetTelNumberValidatorTests(SimpleTestCase):

    def setUp(self):
        self.validators = get_tel_number_validator()

    def test_returns_list_with_validator(self):
        self.assertIsInstance(self.validators, list)
        self.assertEqual(len(self.validators), 1)
        self.assertIsInstance(self.validators[0], RegexValidator)

    def test_valid_phone_numbers(self):
        validator = self.validators[0]

        valid_numbers = [
            "+380501234567",
            "0501234567",
        ]

        for number in valid_numbers:
            try:
                validator(number)
            except ValidationError:
                self.fail(f"ValidationError raised for valid number: {number}")

    def test_invalid_phone_numbers(self):
        validator = self.validators[0]

        invalid_numbers = [
            "1234567890",          # no valid prefix
            "+390501234567",       # wrong country code
            "050123456",          # too short
            "050123456789",       # too long
            "+38 (050) 123-45-67",# unsupported format
            "abc",                # letters
            "",                   # empty
            "+38 050 123 45 67",  # whitespaces
            "+380 50 123 45 67",  # whitespaces
            "050 123 45 67",      # whitespaces
        ]

        for number in invalid_numbers:
            with self.assertRaises(ValidationError):
                validator(number)

    def test_error_message_and_code(self):
        validator = self.validators[0]

        with self.assertRaises(ValidationError) as context:
            validator("123")

        error = context.exception

        self.assertEqual(error.code, "invalid_tel_number")
        self.assertEqual(error.message, "Невірне значення")


# ==========


class GetAddressValidatorTests(SimpleTestCase):

    def setUp(self):
        self.validators = get_address_validator()

    def test_returns_list_with_validator(self):
        self.assertIsInstance(self.validators, list)
        self.assertEqual(len(self.validators), 1)
        self.assertIsInstance(self.validators[0], RegexValidator)

    def test_valid_addresses(self):
        validator = self.validators[0]

        valid_addresses = [
            "Main Street 12",
            "Baker St. 221B",
            "вул. Шевченка 10",
            "вул. Шевченка, 10",
            "вул. Шевченка буд. 10",
            "вул. Шевченка буд.10",
            "вул. Шевченка, буд. 10",
            "вул. Шевченка, буд.10",
            "вул. Тараса Шевченка 10",
            "вул. Тараса Шевченка, 10",
            "вул. Тараса Шевченка буд. 10",
            "вул. Тараса Шевченка, буд. 10",
            "вул. Тараса Шевченка, буд.10",
            "вул. Тараса-Шевченка, буд. 10",
            "Via Roma, 25",
            "Apartment 4B (Entrance 2)",
            "Street-Name 45/2",
        ]

        for address in valid_addresses:
            try:
                validator(address)
            except ValidationError:
                self.fail(f"ValidationError raised for valid address: {address}")

    def test_invalid_addresses(self):
        validator = self.validators[0]

        invalid_addresses = [
            "Address@",       # forbidden symbol
            "Street #12",     # '#' not allowed
            "City!",          # '!' not allowed
            "Name$",          # '$' not allowed
            " вул. Тараса Шевченка буд. 10", # starts from a whitespace
        ]

        for address in invalid_addresses:
            with self.assertRaises(ValidationError):
                validator(address)

    def test_empty_string(self):
        validator = self.validators[0]

        # NOTE: your regex allows empty string if you change '+' to '*'
        # but currently '+' requires at least 1 char → so this should fail
        with self.assertRaises(ValidationError):
            validator("")

    def test_error_message_and_code(self):
        validator = self.validators[0]

        with self.assertRaises(ValidationError) as context:
            validator("Invalid@Address")

        error = context.exception

        self.assertEqual(error.code, "invalid_address")
        self.assertEqual(error.message, "Невірне значення")


# ==========


class GetCarLicensePlateValidatorTests(SimpleTestCase):

    def test_returns_list_with_dummy_validator(self):
        validators = get_car_license_plate_validator()

        self.assertIsInstance(validators, list)
        self.assertEqual(len(validators), 1)
        self.assertIs(validators[0], dummy_validator)

    def test_valid_values(self):
        validator = get_car_license_plate_validator()[0]

        # should not raise anything for any input
        try:
            validator("ANY VALUE")
            validator("")
            validator("!!!@@@###")
            validator(None)
        except Exception as e:
            self.fail(f"dummy_validator raised an exception: {e}")

    def test_invalid_values(self):
        pass
        # validator = get_car_license_plate_validator()[0]

        # # should not raise anything for any input
        # try:
        #     validator("ANY VALUE")
        #     validator("")
        #     validator("!!!@@@###")
        #     validator(None)
        # except Exception as e:
        #     self.fail(f"dummy_validator raised an exception: {e}")

    def test_dummy_validator_returns_none(self):
        validator = get_car_license_plate_validator()[0]

        result = validator("ABC123")

        self.assertIsNone(result)


# ==========


class GetNumericTypesTests(SimpleTestCase):

    def test_returns_tuple(self):
        result = get_numeric_types()

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)

    def test_contains_correct_field_types(self):
        result = get_numeric_types()

        self.assertIn(models.FloatField, result)
        self.assertIn(models.DecimalField, result)
        self.assertIn(models.IntegerField, result)

    def test_exact_order(self):
        result = get_numeric_types()

        expected = (
            models.FloatField,
            models.DecimalField,
            models.IntegerField,
        )

        self.assertEqual(result, expected)

    def test_all_items_are_django_field_classes(self):
        result = get_numeric_types()

        for item in result:
            self.assertTrue(
                issubclass(item, models.Field),
                f"{item} is not a Django model Field"
            )


# ==========


class DummyModel(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = "mainapp"


class DummyAdminSite(admin.AdminSite):
    pass


class IsModelRegisteredInAdminSiteTests(SimpleTestCase):

    def setUp(self):
        self.site = DummyAdminSite()

    def test_returns_false_if_not_admin_site(self):
        result = is_model_registered_in_admin_site("not_admin", "dummymodel")
        self.assertFalse(result)

    def test_returns_false_when_no_models_registered(self):
        result = is_model_registered_in_admin_site(self.site, "dummymodel")
        self.assertFalse(result)

    def test_registered_model_returns_true(self):
        self.site.register(DummyModel)

        result = is_model_registered_in_admin_site(self.site, "dummymodel")
        self.assertTrue(result)

    def test_case_insensitive_match(self):
        self.site.register(DummyModel)

        self.assertTrue(
            is_model_registered_in_admin_site(self.site, "DummyModel")
        )
        self.assertTrue(
            is_model_registered_in_admin_site(self.site, "DUMMYMODEL")
        )
        self.assertTrue(
            is_model_registered_in_admin_site(self.site, "dummyModel")
        )

    def test_unregistered_model_returns_false(self):
        self.site.register(DummyModel)

        self.assertFalse(
            is_model_registered_in_admin_site(self.site, "OtherModel")
        )

    def test_multiple_models(self):
        class AnotherModel(models.Model):
            class Meta:
                app_label = "mainapp"

        self.site.register(DummyModel)
        self.site.register(AnotherModel)

        self.assertTrue(
            is_model_registered_in_admin_site(self.site, "dummymodel")
        )
        self.assertTrue(
            is_model_registered_in_admin_site(self.site, "anothermodel")
        )


# ==========


class SetRelatedModelAttrTests(SimpleTestCase):

    @patch("django.apps.apps.get_model")
    def test_sets_attribute_when_none(self, mock_get_model):
        # --- fake related object (returned from DB)
        rel_obj = Mock()
        rel_obj.pk = 1
        rel_obj.name = None

        # --- mock model manager
        mock_model = Mock()
        mock_model.objects.get.return_value = rel_obj
        mock_get_model.return_value = mock_model

        # --- fake target object
        target = Mock()
        target.rel = Mock(pk=1)

        # --- call function
        set_related_model_attr(
            a_label="mainapp",
            targetObj=target,
            targetObjAttribute="rel",
            model="Model",
            attribute="name",
            value="NEW"
        )

        # --- assertions
        self.assertEqual(rel_obj.name, "NEW")
        rel_obj.save.assert_called_once_with(update_fields=["name"])

    @patch("django.apps.apps.get_model")
    def test_does_not_override_existing(self, mock_get_model):
        rel_obj = Mock()
        rel_obj.pk = 1
        rel_obj.name = "EXISTING"

        mock_model = Mock()
        mock_model.objects.get.return_value = rel_obj
        mock_get_model.return_value = mock_model

        target = Mock()
        target.rel = Mock(pk=1)

        set_related_model_attr(
            "mainapp", target, "rel", "Model", "name", "NEW"
        )

        self.assertEqual(rel_obj.name, "EXISTING")
        rel_obj.save.assert_not_called()

    @patch("django.apps.apps.get_model")
    def test_no_relation(self, mock_get_model):
        target = Mock()
        target.rel = None

        set_related_model_attr(
            "mainapp", target, "rel", "Model", "name", "NEW"
        )

        mock_get_model.assert_not_called()

    @patch("django.apps.apps.get_model")
    def test_get_model_called_correctly(self, mock_get_model):
        rel_obj = Mock(pk=1, name=None)

        mock_model = Mock()
        mock_model.objects.get.return_value = rel_obj
        mock_get_model.return_value = mock_model

        target = Mock()
        target.rel = Mock(pk=1)

        set_related_model_attr(
            "mainapp", target, "rel", "MyModel", "name", "NEW"
        )

        mock_get_model.assert_called_once_with(
            app_label="mainapp",
            model_name="MyModel"
        )


# ==========


class ClearRelatedModelAttrTests(SimpleTestCase):
    @patch("django.apps.apps.get_model")
    def test_clears_attribute_when_present(self, mock_get_model):
        # fake related object
        rel_obj = Mock()
        rel_obj.pk = 1
        rel_obj.name = "VALUE"

        # mock model manager
        mock_model = Mock()
        mock_model.objects.get.return_value = rel_obj
        mock_get_model.return_value = mock_model

        # fake target
        target = Mock()
        target.rel = Mock(pk=1)

        clear_related_model_attr(
            "mainapp", target, "rel", "Model", "name"
        )

        # assertions
        self.assertIsNone(rel_obj.name)
        rel_obj.save.assert_called_once_with(update_fields=["name"])

    @patch("django.apps.apps.get_model")
    def test_does_nothing_if_already_none(self, mock_get_model):
        rel_obj = Mock()
        rel_obj.pk = 1
        rel_obj.name = None

        mock_model = Mock()
        mock_model.objects.get.return_value = rel_obj
        mock_get_model.return_value = mock_model

        target = Mock()
        target.rel = Mock(pk=1)

        clear_related_model_attr(
            "mainapp", target, "rel", "Model", "name"
        )

        rel_obj.save.assert_not_called()

    @patch("django.apps.apps.get_model")
    def test_no_relation(self, mock_get_model):
        target = Mock()
        target.rel = None

        clear_related_model_attr(
            "mainapp", target, "rel", "Model", "name"
        )

        mock_get_model.assert_not_called()

    @patch("django.apps.apps.get_model")
    def test_invalid_attribute_raises(self, mock_get_model):
        rel_obj = Mock(pk=1)
        del rel_obj.name  # simulate missing attribute

        mock_model = Mock()
        mock_model.objects.get.return_value = rel_obj
        mock_get_model.return_value = mock_model

        target = Mock()
        target.rel = Mock(pk=1)

        with self.assertRaises(AttributeError):
            clear_related_model_attr(
                "mainapp", target, "rel", "Model", "name"
            )

    @patch("django.apps.apps.get_model")
    def test_get_model_called_correctly(self, mock_get_model):
        rel_obj = Mock(pk=1, name="X")

        mock_model = Mock()
        mock_model.objects.get.return_value = rel_obj
        mock_get_model.return_value = mock_model

        target = Mock()
        target.rel = Mock(pk=1)

        clear_related_model_attr(
            "mainapp", target, "rel", "MyModel", "name"
        )

        mock_get_model.assert_called_once_with(
            app_label="mainapp",
            model_name="MyModel"
        )


# ==========


class GetModelVerboseNameTests(SimpleTestCase):
    @patch("django.apps.apps.get_model")
    def test_returns_verbose_name(self, mock_get_model):
        # fake model with _meta.verbose_name
        mock_model = Mock()
        mock_model._meta.verbose_name = "Test Model"

        mock_get_model.return_value = mock_model

        result = get_model_verbose_name("mainapp", "Model")

        self.assertEqual(result, "Test Model")

    @patch("django.apps.apps.get_model")
    def test_returns_empty_if_model_none(self, mock_get_model):
        mock_get_model.return_value = None

        result = get_model_verbose_name("mainapp", "Model")

        self.assertEqual(result, "")

    @patch("django.apps.apps.get_model")
    def test_get_model_called_correctly(self, mock_get_model):
        mock_model = Mock()
        mock_model._meta.verbose_name = "X"

        mock_get_model.return_value = mock_model

        get_model_verbose_name("mainapp", "MyModel")

        mock_get_model.assert_called_once_with(
            app_label="mainapp",
            model_name="MyModel"
        )

    @patch("django.apps.apps.get_model")
    def test_missing_meta_raises(self, mock_get_model):
        mock_model = Mock()
        del mock_model._meta  # simulate broken model

        mock_get_model.return_value = mock_model

        with self.assertRaises(AttributeError):
            get_model_verbose_name("mainapp", "Model")


# ==========



