from django.apps import apps
from typing import Any, Mapping
from django.db import models
from django.core.validators import RegexValidator



def get_fields_verbose_names(model_name: str, app_name: str, mode: int = 0) -> dict:
    """
    Get verbose names of a model fields 
    model_name: str
        model name
    app_name: str
        app name
    app_name: int
        function mode = 0 - default, verbose name value as is
        function mode = 1 - verbose name value is capitalized
        function mode = 2 - verbose name value is uppercased
        function mode = 3 - verbose name value is lowercased
    """
    result = {}

    if (not model_name) or  model_name == "" or app_name == "" or mode == "":
        return result

    # print(f"get_fields_verbose_names()")
    # print(f"model_name = {model_name}")
    # print(f"app_name = {app_name}")
    model = apps.get_model(app_label=app_name, model_name=model_name)
    if model:
        fields = model._meta.get_fields()
        for field in fields:
            # print(f"field.name = {field.name}")
            # print(f"isinstance(field, models.ForeignKey) = {isinstance(field, models.ForeignKey)}")
            # print(f"isinstance(field, models.OneToOneField) = {isinstance(field, models.OneToOneField)}")
            # print(f"isinstance(field, models.OneToOneRel) = {isinstance(field, models.OneToOneRel)}")
            if isinstance(field, models.OneToOneRel):
                # val ="models.OneToOneRel"
                val = field.field.verbose_name
                # print(f"field = {field}")
                # for f in field:
                #     print(f"f = {f}")
            elif isinstance(field, models.ManyToOneRel):
                # val ="models.ManyToOneRel"
                val = field.field.verbose_name
            elif isinstance(field, models.ManyToManyRel):
                # val ="models.ManyToManyRel"
                val = field.field.verbose_name
            else:
                val = field.verbose_name
            # print(f"val = {val}")
            if mode == 1:
                val = val.capitalize()
            elif mode == 2:
                val = val.upper()
            elif mode == 3:
                val = val.lower()
            result[field.name] = val
    return result



def get_person_name_validator() -> dict:
    """
    Get human person name validator
    """
    return [RegexValidator(
        regex="^[А-ЩЬЮЯЇІЄҐа-щьюяїієґ'\-\s]+$",
        message='Невірне значення',
        code='invalid_person_name',
    )]



def get_tel_number_validator() -> dict:
    """
    Get telephone number validator
    """
    return [RegexValidator(
        regex="^(\+?38)?\s?(0\d{2})\s?\d{3}\s?\d{2}\s?\d{2}$",
        message='Невірне значення',
        code='invalid_tel_number',
    )]



def get_address_validator() -> dict:
    """
    Get address validator
    """
    return [RegexValidator(
        regex="^[\w\s.,\-/\(\)]+$",
        message='Невірне значення',
        code='invalid_address',
    )]



def dummy_validator(value):
    pass



def get_car_license_plate_validator() -> dict:
    """
    Get car's license plate validator
    """
    return [dummy_validator]
    # return [RegexValidator(
    #     regex="^[АВЕКМНОРСТХІ]{2}\d{4}[АВЕКМНОРСТХІ]{2}$", #cyrillic
    #     # regex="^[ABEKMHOPCTXI]{2}\d{4}[ABEKMHOPCTXI]{2}$", # latin
    #     message='Невірне значення. ',
    #     code='invalid_car_license_plate',
    # )]   



def get_numeric_types():
    return (models.FloatField, models.DecimalField, models.IntegerField)
    
    
