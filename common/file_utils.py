# Utilities for files

from django.http import HttpResponse, HttpResponseBadRequest
from datetime import date
from uuid import uuid4



def get_file_export_response(format: str, file_data, file_name: str) -> bool:
    """
    Get response for a file export
    format : str
        file format
    file_data :
        file_data
    file_name: str
        file name without an extension
    """
    if format == 'xlsx':
        # response = HttpResponse(file_data.xlsx, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response = HttpResponse(file_data, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="' + file_name + '.xlsx"'
        print(f"response = {response}")
        print(f'response["Content-Disposition"] = {response["Content-Disposition"]}')
        return response
    return HttpResponseBadRequest('Invalid request')



def get_image_path(path_prefix, mode: int, date=date.today()):
    """
    Get directory path of an image
    path_prefix
        path prefix
    mode : int
       if 0 then return value for a field models.ImageField parameter
       if 1 then return value with calculated today's date
       if 2 then return value with date defined in the second parameter
    date : date
        date for mode=2
    """
    if (mode==0):
        return path_prefix + "%Y/%m/%d/"
    if (mode==1):
        d = date.today()
    if (mode==2):
        d = date
    return path_prefix + str(d.year) + "/" + '{:02d}'.format(d.month) + "/" + '{:02d}'.format(d.day) + "/"



def get_file_uniq_name(file_extension: str):
    """
    Get unique name for a file
    file_extension:
        extension of a file, without a dot!, e.g. "txt", "jpg" and so on
    """
    return str(uuid4()) + "." + file_extension













