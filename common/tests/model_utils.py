from django.test import TestCase
from ..model_utils import *
from mainapp.apps import MainappConfig
from mainapp.models import CemeteryPlace, DeadPerson



class ModelUtilsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_get_fields_verbose_names(self):
        verboses = get_fields_verbose_names("CemeteryPlace", MainappConfig.name)
        # print(f"verboses = {verboses}")
        self.assertEqual(verboses.get("cemetery_name"), CemeteryPlace._meta.get_field("cemetery_name").verbose_name)
        self.assertEqual(verboses.get("cemetery_sector"), CemeteryPlace._meta.get_field("cemetery_sector").verbose_name)
        self.assertEqual(verboses.get("cemetery_area"), CemeteryPlace._meta.get_field("cemetery_area").verbose_name)
        self.assertEqual(verboses.get("cemetery_row"), CemeteryPlace._meta.get_field("cemetery_row").verbose_name)
        self.assertEqual(verboses.get("location"), CemeteryPlace._meta.get_field("location").verbose_name)
        self.assertEqual(verboses.get("dead_person"), CemeteryPlace._meta.get_field("dead_person").verbose_name)
        self.assertEqual(verboses.get("status"), CemeteryPlace._meta.get_field("status").verbose_name)
        self.assertEqual(verboses.get("booking_info"), CemeteryPlace._meta.get_field("booking_info").verbose_name)
        self.assertEqual(verboses.get("note"), CemeteryPlace._meta.get_field("note").verbose_name)
        self.assertEqual(verboses.get("picture"), CemeteryPlace._meta.get_field("picture").verbose_name)
        self.assertEqual(verboses.get("picture2"), CemeteryPlace._meta.get_field("picture2").verbose_name)
        self.assertEqual(verboses.get("picture3"), CemeteryPlace._meta.get_field("picture3").verbose_name)

        verboses = get_fields_verbose_names("CemeteryPlace", MainappConfig.name, 0)
        # print(f"verboses = {verboses}")
        self.assertEqual(verboses.get("cemetery_name"), CemeteryPlace._meta.get_field("cemetery_name").verbose_name)
        self.assertEqual(verboses.get("cemetery_sector"), CemeteryPlace._meta.get_field("cemetery_sector").verbose_name)
        self.assertEqual(verboses.get("cemetery_area"), CemeteryPlace._meta.get_field("cemetery_area").verbose_name)
        self.assertEqual(verboses.get("cemetery_row"), CemeteryPlace._meta.get_field("cemetery_row").verbose_name)
        self.assertEqual(verboses.get("location"), CemeteryPlace._meta.get_field("location").verbose_name)
        self.assertEqual(verboses.get("dead_person"), CemeteryPlace._meta.get_field("dead_person").verbose_name)
        self.assertEqual(verboses.get("status"), CemeteryPlace._meta.get_field("status").verbose_name)
        self.assertEqual(verboses.get("booking_info"), CemeteryPlace._meta.get_field("booking_info").verbose_name)
        self.assertEqual(verboses.get("note"), CemeteryPlace._meta.get_field("note").verbose_name)
        self.assertEqual(verboses.get("picture"), CemeteryPlace._meta.get_field("picture").verbose_name)
        self.assertEqual(verboses.get("picture2"), CemeteryPlace._meta.get_field("picture2").verbose_name)
        self.assertEqual(verboses.get("picture3"), CemeteryPlace._meta.get_field("picture3").verbose_name)

        verboses = get_fields_verbose_names("CemeteryPlace", MainappConfig.name, 1)
        # print(f"verboses = {verboses}")
        self.assertEqual(verboses.get("cemetery_name"), CemeteryPlace._meta.get_field("cemetery_name").verbose_name.capitalize())
        self.assertEqual(verboses.get("cemetery_sector"), CemeteryPlace._meta.get_field("cemetery_sector").verbose_name.capitalize())
        self.assertEqual(verboses.get("cemetery_area"), CemeteryPlace._meta.get_field("cemetery_area").verbose_name.capitalize())
        self.assertEqual(verboses.get("cemetery_row"), CemeteryPlace._meta.get_field("cemetery_row").verbose_name.capitalize())
        self.assertEqual(verboses.get("location"), CemeteryPlace._meta.get_field("location").verbose_name.capitalize())
        self.assertEqual(verboses.get("dead_person"), CemeteryPlace._meta.get_field("dead_person").verbose_name.capitalize())
        self.assertEqual(verboses.get("status"), CemeteryPlace._meta.get_field("status").verbose_name.capitalize())
        self.assertEqual(verboses.get("booking_info"), CemeteryPlace._meta.get_field("booking_info").verbose_name.capitalize())
        self.assertEqual(verboses.get("note"), CemeteryPlace._meta.get_field("note").verbose_name.capitalize())
        self.assertEqual(verboses.get("picture"), CemeteryPlace._meta.get_field("picture").verbose_name.capitalize())
        self.assertEqual(verboses.get("picture2"), CemeteryPlace._meta.get_field("picture2").verbose_name.capitalize())
        self.assertEqual(verboses.get("picture3"), CemeteryPlace._meta.get_field("picture3").verbose_name.capitalize())

        verboses = get_fields_verbose_names("CemeteryPlace", MainappConfig.name, 2)
        # print(f"verboses = {verboses}")
        self.assertEqual(verboses.get("cemetery_name"), CemeteryPlace._meta.get_field("cemetery_name").verbose_name.upper())
        self.assertEqual(verboses.get("cemetery_sector"), CemeteryPlace._meta.get_field("cemetery_sector").verbose_name.upper())
        self.assertEqual(verboses.get("cemetery_area"), CemeteryPlace._meta.get_field("cemetery_area").verbose_name.upper())
        self.assertEqual(verboses.get("cemetery_row"), CemeteryPlace._meta.get_field("cemetery_row").verbose_name.upper())
        self.assertEqual(verboses.get("location"), CemeteryPlace._meta.get_field("location").verbose_name.upper())
        self.assertEqual(verboses.get("dead_person"), CemeteryPlace._meta.get_field("dead_person").verbose_name.upper())
        self.assertEqual(verboses.get("status"), CemeteryPlace._meta.get_field("status").verbose_name.upper())
        self.assertEqual(verboses.get("booking_info"), CemeteryPlace._meta.get_field("booking_info").verbose_name.upper())
        self.assertEqual(verboses.get("note"), CemeteryPlace._meta.get_field("note").verbose_name.upper())
        self.assertEqual(verboses.get("picture"), CemeteryPlace._meta.get_field("picture").verbose_name.upper())
        self.assertEqual(verboses.get("picture2"), CemeteryPlace._meta.get_field("picture2").verbose_name.upper())
        self.assertEqual(verboses.get("picture3"), CemeteryPlace._meta.get_field("picture3").verbose_name.upper())

        verboses = get_fields_verbose_names("CemeteryPlace", MainappConfig.name, 3)
        # print(f"verboses = {verboses}")
        self.assertEqual(verboses.get("cemetery_name"), CemeteryPlace._meta.get_field("cemetery_name").verbose_name.lower())
        self.assertEqual(verboses.get("cemetery_sector"), CemeteryPlace._meta.get_field("cemetery_sector").verbose_name.lower())
        self.assertEqual(verboses.get("cemetery_area"), CemeteryPlace._meta.get_field("cemetery_area").verbose_name.lower())
        self.assertEqual(verboses.get("cemetery_row"), CemeteryPlace._meta.get_field("cemetery_row").verbose_name.lower())
        self.assertEqual(verboses.get("location"), CemeteryPlace._meta.get_field("location").verbose_name.lower())
        self.assertEqual(verboses.get("dead_person"), CemeteryPlace._meta.get_field("dead_person").verbose_name.lower())
        self.assertEqual(verboses.get("status"), CemeteryPlace._meta.get_field("status").verbose_name)
        self.assertEqual(verboses.get("booking_info"), CemeteryPlace._meta.get_field("booking_info").verbose_name.lower())
        self.assertEqual(verboses.get("note"), CemeteryPlace._meta.get_field("note").verbose_name.lower())
        self.assertEqual(verboses.get("picture"), CemeteryPlace._meta.get_field("picture").verbose_name.lower())
        self.assertEqual(verboses.get("picture2"), CemeteryPlace._meta.get_field("picture2").verbose_name.lower())
        self.assertEqual(verboses.get("picture3"), CemeteryPlace._meta.get_field("picture3").verbose_name.lower())

        verboses = get_fields_verbose_names("DeadPerson", MainappConfig.name, 1)
        # print(f"verboses = {verboses}")
        self.assertEqual(verboses.get("surname"), DeadPerson._meta.get_field("surname").verbose_name.capitalize())
        self.assertEqual(verboses.get("name"), DeadPerson._meta.get_field("name").verbose_name.capitalize())
        self.assertEqual(verboses.get("patronymic"), DeadPerson._meta.get_field("patronymic").verbose_name.capitalize())
        self.assertEqual(verboses.get("birth_date"), DeadPerson._meta.get_field("birth_date").verbose_name.capitalize())
        self.assertEqual(verboses.get("death_date"), DeadPerson._meta.get_field("death_date").verbose_name.capitalize())
        self.assertEqual(verboses.get("burial_date"), DeadPerson._meta.get_field("burial_date").verbose_name.capitalize())
        self.assertEqual(verboses.get("age"), DeadPerson._meta.get_field("age").verbose_name.capitalize())
        self.assertEqual(verboses.get("death_certificate"), DeadPerson._meta.get_field("death_certificate").verbose_name.capitalize())
        self.assertEqual(verboses.get("relatives_info"), DeadPerson._meta.get_field("relatives_info").verbose_name.capitalize())
        self.assertEqual(verboses.get("person_name_who_will_bury"), DeadPerson._meta.get_field("person_name_who_will_bury").verbose_name.capitalize())
        self.assertEqual(verboses.get("person_address_who_will_bury"), DeadPerson._meta.get_field("person_address_who_will_bury").verbose_name.capitalize())
        self.assertEqual(verboses.get("person_name_family_burial"), DeadPerson._meta.get_field("person_name_family_burial").verbose_name.capitalize())
        self.assertEqual(verboses.get("person_address_family_burial"), DeadPerson._meta.get_field("person_address_family_burial").verbose_name.capitalize())
        self.assertEqual(verboses.get("who_did_burial"), DeadPerson._meta.get_field("who_did_burial").verbose_name.capitalize())
        self.assertEqual(verboses.get("note"), DeadPerson._meta.get_field("note").verbose_name.capitalize())
        self.assertEqual(verboses.get("ident"), DeadPerson._meta.get_field("ident").verbose_name.capitalize())

    def test_get_fields_verbose_names_with_bad_params(self):
        verboses = get_fields_verbose_names("", MainappConfig.name, 1)
        self.assertEqual(verboses, {})

        verboses = get_fields_verbose_names("CemeteryPlace", "", 1)
        self.assertEqual(verboses, {})

        verboses = get_fields_verbose_names("CemeteryPlace", MainappConfig.name, "")
        self.assertEqual(verboses, {})

    def test_get_person_name_validator(self):
        # TODO
        pass

    def test_get_tel_number_validator(self):
        # TODO
        pass

    def test_get_address_validator(self):
        # TODO
        pass