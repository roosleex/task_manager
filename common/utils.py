from django.contrib import admin
from django.apps import apps
from ast import literal_eval
from typing import Any, Mapping


#Check out if a model registered in the admin site
def is_model_registered_in_admin_site(admin_site, model_name):
    """
    admin_site : admin.AdminSite
        instance of admin.AdminSite
    model_name : str
    """
    if not isinstance(admin_site, admin.AdminSite):
        return False
    reg_models = admin_site._registry.items()
    for model, model_admin in reg_models:
        if (model == model_name):
            return True
    return False



#Safe method for getting a list element
def list_get(l, index, default):
    """
    l: list
        iinstance of a list
    index: int
        index of an element
    default: any
        default value if the index out of bound
    """
    return l[index] if index < len(l) else default



#Set related model attribute
def set_related_model_attr(a_label, targetObj, targetObjAttribute, model, attribute, value):
    """
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



#Clear related model attribute
def clear_related_model_attr(a_label, targetObj, targetObjAttribute, model, attribute):
    """
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



# Get model verbose_name
def get_model_verbose_name(a_label, m_name):
    """
    a_label: str
        application label
    m_name: str
        model name
    """
    model = apps.get_model(app_label=a_label, model_name=m_name)
    if model:
        return model._meta.verbose_name
    return ''


def eval_str(code, globals: dict[str, Any] | None = None, locals: Mapping[str, object] | None = None):
    """
    Evaluate a string of code
    code : str
        a string containing code expression
    globals: dict
        provides a global namespace to eval()
    locals: dict
        contains the variables that eval() uses as local names when evaluating expression
    """
    #TODO: check code param on vulnerabilities
    result = eval(code, globals, locals)
    return result



def is_first_val_greater_than_second_val(val1, val2, custom_message: str = ""):
    """
    Check if the first value greater than the second value
    Return bool result and user message
    val1: 
        the first value
    val2:
        the second value
    custom_message: str
        custom user's message
    """
    result = False
    message = ""
    if val1 and val2:
        if val1 > val2:
            result = True
            if custom_message == "":
                message = f"{val1} > {val2}"
            else:
                message = custom_message
    # print(f"result = {result}")
    # print(f"message = {message}")
    return (result, message)


