# Predefined form controls

from django import forms
# from mainapp.apps import MainappConfig
from django.apps import apps
from datetime import date



def get_choices_empty_default():
    return [('','---------')]



class FullDate(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        kwargs.setdefault("widget", forms.TextInput(attrs={'type':'date'}))
        super().__init__(*args, **kwargs)



class FullDateMin(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", "Дата початкова")
        kwargs.setdefault("required", False)
        kwargs.setdefault("widget", forms.TextInput(attrs={'type':'date'}))
        super().__init__(*args, **kwargs)



class FullDateMax(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label", "Дата кінцева")
        kwargs.setdefault("required", False)
        kwargs.setdefault("widget", forms.TextInput(attrs={'type':'date'}))
        super().__init__(*args, **kwargs)



class AllModelsNames(forms.ChoiceField):
    def __init__(self, app_label, *args, **kwargs):
        kwargs.setdefault("label", "Довідник")
        choices = self.get_model_choices(app_label)
        super().__init__(choices=choices, *args, **kwargs)

    def get_model_choices(self, app_label):
        choices = []
        for model in apps.get_app_config(app_label).get_models():
            model_name = model.__name__
            if 'Historical' in model_name:
                continue
            try:
                if model.objects.exists():  # Only include if model has at least one record
                    verbose = model._meta.verbose_name.title()
                    choices.append((model_name, verbose))
            except Exception:
                # Some models (e.g., unmanaged, abstract) may throw here
                continue
        return choices

    # def get_model_choices(self, app_label):
    #     models = apps.get_app_config(app_label).get_models()
    #     return [(model.__name__, model._meta.verbose_name.title()) for model in models]



class MonthInput(forms.TextInput):
    input_type = "month"

    def format_value(self, value):
        """
        Convert Python date -> YYYY-MM string for HTML <input type="month">.
        """
        if isinstance(value, date):
            return value.strftime("%Y-%m")
        return super().format_value(value)
    


class MonthDate(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        kwargs.setdefault("label", "Місяць")
        kwargs.setdefault("widget", MonthInput())
        # kwargs.setdefault(
        #     "widget",
        #     forms.TextInput(attrs={"type": "month"})  # HTML5 month picker
        # )
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """
        Convert YYYY-MM string into a Python date (use first day of month).
        """
        if not value:
            return None
        try:
            year, month = map(int, value.split("-"))
            return forms.DateField().to_python(f"{year}-{month:02d}-01")
        except Exception:
            raise forms.ValidationError("Введіть коректний місяць та рік.")
        


class CustomSelect(forms.ChoiceField):
    def __init__(self, label: str, required: bool, choices: list, *args, **kwargs):
        kwargs.setdefault("label", label)
        kwargs.setdefault("required", required)
        # Choices must be provided, at least an empty list
        choices1 = get_choices_empty_default() + choices
        kwargs.setdefault("choices", choices1)
        # kwargs.setdefault("choices", [
        #     ("", "---------"),  # default empty option
        #     ("ivanov", "Іванов Іван"),
        #     ("petrov", "Петров Петро"),
        #     ("sydorenko", "Сидоренко Сергій"),
        # ])
        super().__init__(*args, **kwargs)



class FullDateTimeInput(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None):
        super().__init__(
            date_attrs={'type': 'date', 'class': 'form-control'},
            time_attrs={'type': 'time', 'class': 'form-control', 'step': 1},
            attrs=attrs
        )



class FullDateTime(forms.SplitDateTimeField):
    def __init__(self, label, required, *args, **kwargs):
        kwargs.setdefault("label", label)
        kwargs.setdefault("required", required)
        kwargs.setdefault("widget", FullDateTimeInput())
        super().__init__(*args, **kwargs)
        




