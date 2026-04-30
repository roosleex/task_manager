from django.apps import apps
from typing import Any, Mapping
from django.db import models
from django.core.validators import RegexValidator
from django.contrib import admin


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
        regex="^[А-ЩЬЮЯЇІЄҐа-щьюяїієґ'\-\s.]+$",
        message='Невірне значення',
        code='invalid_person_name',
    )]



def get_tel_number_validator() -> dict:
    """
    Get telephone number validator
    """
    return [RegexValidator(
        # regex="^(\+?38)?\s?(0\d{2})\s?\d{3}\s?\d{2}\s?\d{2}$",
        # without whitespaces
        regex="^(\+?38)?(0\d{2})\d{3}\d{2}\d{2}$",
        message='Невірне значення',
        code='invalid_tel_number',
    )]



def get_address_validator() -> dict:
    """
    Get address validator
    """
    return [RegexValidator(
        regex="^[\w]{1,}[\w\s.,\-/\(\)]+$",
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


def is_model_registered_in_admin_site(admin_site, model_name):
    """
    Check out if a model registered in the admin site
    admin_site : admin.AdminSite
        instance of admin.AdminSite
    model_name : str
    """
    if not isinstance(admin_site, admin.AdminSite):
        return False
    reg_models = admin_site._registry.items()
    for model, model_admin in reg_models:
        if model._meta.model_name.lower() == model_name.lower():
            return True
    return False


def set_related_model_attr(a_label, targetObj, targetObjAttribute, model, attribute, value):
    """
    Set related model attribute
    a_label: str
        application label
    targetObj: models.Model
        target object in which related model is
    targetObjAttribute: str
        attribute name in targetObj which keeps related model
    model : str
        related model name
    attribute : str
        related model attribute name to assing
    value : str
        value for assinging to related model attribute 
    """
    selfAttr = getattr(targetObj, targetObjAttribute)
    if selfAttr:
        relModel = apps.get_model(app_label=a_label, model_name=model)
        relModelObj = relModel.objects.get(pk=selfAttr.pk)
        if relModelObj and getattr(relModelObj, attribute) is None:
            setattr(relModelObj, attribute, value)
            relModelObj.save(update_fields=[attribute])
    """
    Example on the real model (self == CemeteryPlace)
    if self.location:
        location = PlaceLocation.objects.get(pk=self.location.pk)
        if location and location.cemetery_place is None:
            location.cemetery_place = self
            location.save(update_fields=["cemetery_place"])
    """


def clear_related_model_attr(a_label, targetObj, targetObjAttribute, model, attribute):
    """
    Clear related model attribute
    a_label: str
        application label
    targetObj: models.Model
        target object in which related model is
    targetObjAttribute: str
        attribute name in targetObj which keeps related model
    model : str
        related model name
    attribute : str
        related model attribute name to assing
    value : str
        value for assinging to related model attribute 
    """
    selfAttr = getattr(targetObj, targetObjAttribute)
    if selfAttr:
        relModel = apps.get_model(app_label=a_label, model_name=model)
        relModelObj = relModel.objects.get(pk=selfAttr.pk)
        if relModelObj and getattr(relModelObj, attribute):
            setattr(relModelObj, attribute, None)
            relModelObj.save(update_fields=[attribute])
    """
    Example on the real model (self == CemeteryPlace)
    if self.location:
        location = PlaceLocation.objects.get(pk=self.location.pk)
        if location and location.cemetery_place:
            location.cemetery_place = None
            location.save(update_fields=["cemetery_place"])
    """


def get_model_verbose_name(a_label, m_name):
    """
    Get model verbose_name
    a_label: str
        application label
    m_name: str
        model name
    """
    model = apps.get_model(app_label=a_label, model_name=m_name)
    if model:
        return model._meta.verbose_name
    return ''




    
