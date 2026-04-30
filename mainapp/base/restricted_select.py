from django.forms import Media, widgets
from django import forms


class RestrictedSelect(widgets.Select):
    @property
    def media(self):
        media = super().media
        media += Media(js=["js/forms/restricted_select_loader.js"])
        return media



class BoundRestrictedModelChoiceField(forms.BoundField):
    def build_widget_attrs(self, attrs, widget=None):
        attrs = super().build_widget_attrs(attrs, widget)

        bound_restrict_on_form_field = self.form[self.field.restrict_on_form_field]
        # Parent select name. By its event child select will be loaded
        attrs["restrict_on_form_field"] = bound_restrict_on_form_field.html_name
        # Field name of a model attrs["restricted_select_model_name"] on which filtering is done
        # If comma separated then more than one fields names
        attrs["restrict_on_relation"] = self.field.restrict_on_relation
        # Model name of a child select
        # If comma separated then more than one child model
        attrs["restricted_select_model_name"] = self.field.restricted_select_model_name
        # Application label
        # If comma separated then more than one application label
        attrs["restricted_select_model_app_label"] = self.field.restricted_select_model_app_label
        # Child select name
        # If comma separated then more than one child 
        attrs["restricted_select_name"] = self.field.restricted_select_name
        # Comma separated list of names of child selects which will be cleared on event of the parent select 
        attrs["clear_restricted_selects_onevent"] = self.field.clear_restricted_selects_onevent
        # Select name with parameter for loading current select if current select options is empty
        # If comma separated then more than one param select
        attrs["select_name_with_param_for_curr_select_load"] = self.field.select_name_with_param_for_curr_select_load

        # IMPORTANT!!!
        # if attrs["restricted_select_name"] has comma separated value then 
        # attrs["restrict_on_relation"], attrs["restricted_select_model_name"], attrs["restricted_select_model_app_label"] 
        # also must have comma separated values. 
        # The order of comma separated values must be appropriate
        # Processing of comma separated values is going from left to right 

        return attrs


 
class RestrictedModelChoiceField(forms.ModelChoiceField):
    widget = RestrictedSelect

    def __init__(self, *args, restrict_on_form_field: str = None, restrict_on_relation: str = None, 
                restricted_select_model_name: str = None, restricted_select_model_app_label: str = None, 
                restricted_select_name: str = None, clear_restricted_selects_onevent: str = None,
                select_name_with_param_for_curr_select_load: str = None, **kwargs):
        super().__init__(*args, **kwargs)

        if not restrict_on_form_field:
            restrict_on_form_field = ""
            #raise ValueError("restrict_on_form_field is required")
        self.restrict_on_form_field = restrict_on_form_field

        if not restrict_on_relation:
            restrict_on_relation = ""
            #raise ValueError("restrict_on_relation is required")
        self.restrict_on_relation = restrict_on_relation

        if not restricted_select_model_name:
            restricted_select_model_name = ""
            #raise ValueError("restricted_select_model_name is required")
        self.restricted_select_model_name = restricted_select_model_name

        if not restricted_select_model_app_label:
            restricted_select_model_app_label = ""
            #raise ValueError("restricted_select_model_app_label is required")
        self.restricted_select_model_app_label = restricted_select_model_app_label

        if not restricted_select_name:
            restricted_select_name = ""
            #raise ValueError("restricted_select_name is required")
        self.restricted_select_name = restricted_select_name

        if not clear_restricted_selects_onevent:
            clear_restricted_selects_onevent = ""
        self.clear_restricted_selects_onevent = clear_restricted_selects_onevent
        
        if not select_name_with_param_for_curr_select_load:
            select_name_with_param_for_curr_select_load = ""
        self.select_name_with_param_for_curr_select_load = select_name_with_param_for_curr_select_load

    def get_bound_field(self, form, field_name):
        return BoundRestrictedModelChoiceField(form, self, field_name)
    


# # BoundRestrictedModelChoiceField for a CemeteryPlace with free status
# class BoundRestrictedModelChoiceFieldFreeCemeteryPlace(BoundRestrictedModelChoiceField):
#     def build_widget_attrs(self, attrs, widget=None):
#         attrs = super().build_widget_attrs(attrs, widget)
#         # Flag that current select contains only rows of CemeteryPlaces with free status
#         attrs["is_select_free_cemetery_place"] = self.field.is_select_free_cemetery_place
#         return attrs



# # RestrictedModelChoiceField for a CemeteryPlace with free status
# class RestrictedModelChoiceFieldFreeCemeteryPlace(RestrictedModelChoiceField):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.is_select_free_cemetery_place = True

#     def get_bound_field(self, form, field_name):
#         return BoundRestrictedModelChoiceFieldFreeCemeteryPlace(form, self, field_name)
    
    

# # Helpful methods for form restricted selects
# class Helper():

#     def is_form_init_instance(obj):
#         """
#         Check out if there is an instance in form's __init__ method
#         obj : form's self
#             form's __init__ self param
#         """
#         return obj.instance.pk
    
#     def is_form_init_after_save(args):
#         """
#         Check out if form's __init__ method is in after save state
#         args : tuple
#             form's __init__ args param
#         """
#         return len(args) != 0
    
#     def is_form_init_before_save(args):
#         """
#         Check out if form's __init__ method is in before save state
#         args : tuple
#             form's __init__ args param
#         """
#         #print(f"len(args) = {len(args)}")
#         #print(f"args = {args}")
#         return len(args) == 0