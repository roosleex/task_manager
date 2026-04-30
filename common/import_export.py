from import_export import resources
from import_export.admin import ExportMixin
from import_export.fields import Field
from import_export.widgets import FloatWidget, IntegerWidget
from django.utils import timezone
from django.utils.encoding import iri_to_uri
from django.utils.timezone import is_aware, localtime, is_naive, make_aware, get_current_timezone
from datetime import datetime



def unique_column_name(obj):
    init_values = {}
    for field in obj.fields.values():
        init_values[field.column_name] = 0
    # print(f"init_values = {init_values}")
    seen = {}
    for field in obj.fields.values():
        original = field.column_name
        if original in seen:
            seen[original] += 1
            tmp_val = f"{original}_{seen[original]}"
            if tmp_val in init_values:
                init_values[tmp_val] += 1
                tmp_val = f"{original}_{seen[original]}_{init_values[tmp_val]}"
            field.column_name = tmp_val
        else:
            seen[original] = 1



def modify_widgets(obj, **kwargs):
    """
    Modify widget properties before export.
    """
    file_format = kwargs.get("file_format")
    if not file_format or (file_format == ""):
        export_form = kwargs.get('export_form')
        if export_form:
            format_id = export_form.cleaned_data.get("format")
            format_text = dict(export_form.fields["format"].choices).get(str(format_id))
            # print(f"get_export_resource_kwargs format_text = {format_text}")
            if format_text:
                file_format = format_text
    # print(f"modify_widgets file_format = {file_format}")
    # print(f"modify_widgets obj_file_format = {obj_file_format}")
    # print(f"kwargs = {kwargs}")
    # print(f"obj.fields = {obj}")
    coerce = False
    if file_format == "pdf":
        coerce = True
    for field in obj.fields.values():
        # print(f"field = {field}")
        if isinstance(field.widget, (FloatWidget, IntegerWidget)):
            field.widget.coerce_to_string = coerce



def append_totals(obj, queryset, dataset, **kwargs):
    """
    Add an extra row at the end of the exported file.
    For example: totals.
    """
    from reports.base.report import complete_totals_data

    file_format = kwargs.get("file_format")
    # print(f"file_format = {file_format}")
    # print(f"########## queryset = {queryset}")
    cols_data = []
    for q in queryset:
        col_data = q.__dict__
        if '_meta' in col_data:
            del col_data['_meta']
        col_data['nn'] = ""
        cols_data.append(col_data)
    # print(f"########## cols_data = {cols_data}")
    totals_data = complete_totals_data(obj.totals_info, obj.cols_info, cols_data)
    # print(f"totals_data = {totals_data}")
    if totals_data and totals_data[0]:
        n = -1
        totals_data_str = []
        for tt in totals_data[0]:
            tt_val = tt
            if tt_val == 0:
                tt_val = ""
            n += 1
            if n == 0:
                totals_data_str.append("Всього:")
                continue 
            if file_format == "pdf":
                tt_val = str(tt_val).replace(".", ",")
            totals_data_str.append(tt_val)
        dataset.append(totals_data_str)



def export_resource_data(data):
        # Iterate over all values (works for list or dict)
        if isinstance(data, dict):
            items = data.items()
        elif isinstance(data, list):
            items = enumerate(data)
        else:
            return data  # unexpected type
        for key, value in items:
            dt = None

            # If value is already datetime
            if hasattr(value, 'tzinfo'):
                dt = value

            # If value is a string like "2025-10-08 21:31:06+00:00"
            elif isinstance(value, str):
                try:
                    dt = datetime.fromisoformat(value)
                except ValueError:
                    dt = None
            if dt:
                if is_naive(dt):
                    # Make it aware using the current Django timezone
                    dt = make_aware(dt, get_current_timezone())
                # Convert to local time
                dt_local = localtime(dt)
                # Convert back to string
                formatted = dt_local.strftime("%d.%m.%Y %H:%M:%S")
                # Update data
                if isinstance(data, dict):
                    data[key] = formatted
                else:
                    data[key] = formatted
        return data



class BaseModelResource(resources.ModelResource):
    """
    For a resource which has a specific model class.
    Resource, який гарантує унікальність column_name.
    Якщо виявляється дублікат, додає суфікс _2, _3 і т.д.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_column_name(self)

    def before_export(self, queryset, **kwargs):
        modify_widgets(self, **kwargs)

    def export_resource(self, obj, *args, **kwargs):
        data = super().export_resource(obj, *args, **kwargs)
        return export_resource_data(data)



class BaseModelReportResource(BaseModelResource):
    """
    For a resource which has a specific model class and using in a reports.
    """

    def __init__(self, cols_info, totals_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cols_info = cols_info
        self.totals_info = totals_info

    def before_export(self, queryset, **kwargs):
        super().before_export(queryset, **kwargs)

    def after_export(self, queryset, dataset, **kwargs):
        append_totals(self, queryset, dataset, **kwargs)



class BaseResource(resources.Resource):
    """
    For a resource which has no specific model class.
    Resource, який гарантує унікальність column_name.
    Якщо виявляється дублікат, додає суфікс _2, _3 і т.д.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_column_name(self)

    def export_resource(self, obj, *args, **kwargs):
        data = super().export_resource(obj, *args, **kwargs)
        return export_resource_data(data)



class BaseReportResource(BaseResource):
    """
    For a resource which based on a report.
    """

    def form(self):
        """
        Form a resource based on report's cols_info 
        """
        for col_info in self.cols_info:
            field_name = col_info.col_name
            field_verbose = col_info.header
            if col_info.is_float_type():
                resource_field = Field(attribute=field_name, column_name=field_verbose, widget=FloatWidget(coerce_to_string=False))
            elif col_info.is_int_type():
                resource_field = Field(attribute=field_name, column_name=field_verbose, widget=IntegerWidget(coerce_to_string=False))
            else:
                resource_field = Field(attribute=field_name, column_name=field_verbose)
            self.fields[field_name] = resource_field
        # print(f"resource.fields = {resource.fields}")
        if self.fields:
            self.export_order = list(self.fields.keys())

    def __init__(self, cols_info, totals_info, *args, **kwargs):
        self.cols_info = cols_info
        self.totals_info = totals_info
        self.form()
        super().__init__(*args, **kwargs)

    def before_export(self, queryset, **kwargs):
        modify_widgets(self, **kwargs)

    def after_export(self, queryset, dataset, **kwargs):
        append_totals(self, queryset, dataset, **kwargs)



class BaseExportMixin(ExportMixin):
    def get_export_filename(self, request, queryset, file_format):
        """
        Global custom export filename for all resources.
        """
        date_str = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
        model_name = self.model._meta.verbose_name_plural
        export_file_name = f"{model_name}_{date_str}.{file_format.get_extension()}"
        # print(f"export_file_name = {export_file_name}")
        return iri_to_uri(export_file_name)
    
    def get_export_formats(self):
        """Add PDF format to the default export formats"""
        from mainapp.base.formats import PDF, XLSX
        # formats = super().get_export_formats()
        formats = [XLSX]
        return formats + [PDF]
    
    # def get_export_data(self, file_format, request, queryset, **kwargs):
    #     print(f"get_export_data file_format = {file_format}")
    #     super().get_export_data(file_format, request, queryset, **kwargs)
        
    
    # def get_export_resource_kwargs(self, request, **kwargs):
    #     """
    #     Ensure file_format is passed into Resource methods (before_export, etc.).
    #     """
    #     # print(f"get_export_resource_kwargs kwargs = {kwargs.get('export_form')}")
    #     resource_kwargs = super().get_export_resource_kwargs(request, **kwargs)
    #     export_form = kwargs.get('export_form')
    #     if export_form:
    #         format_id = export_form.cleaned_data.get("format")
    #         format_text = dict(export_form.fields["format"].choices).get(str(format_id))
    #         print(f"get_export_resource_kwargs format_text = {format_text}")
    #         if format_text:
    #             resource_kwargs["file_format"] = format_text
    #     return resource_kwargs



def dehydrate_date_time(value) -> str:
    """
    dehydrate models.DateTimeField value
    value: models.DateTimeField value
        e.g. 2025-07-29 09:53:27.251029+00:00
    """
    if value:
        return value.strftime("%d.%m.%Y %H:%M:%S")
    return ""



def is_report_resource(resource):
    """
    Chech if resource is a report resource
    resource: 
        instance of resources.Resource
    """
    if (isinstance(resource, BaseModelReportResource) or isinstance(resource, BaseReportResource)):
        return True
    return False