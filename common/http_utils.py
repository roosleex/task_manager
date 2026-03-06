# Utilities for http

import urllib.parse



def is_ajax_header(request) -> bool:
    """
    Check if headers have ajax header
    request : 
        request data
    """
    target_header = request.headers.get('X-Requested-With')
    if target_header:
        if target_header == 'XMLHttpRequest':
            return True
    return False



def is_method_get(request) -> bool:
    """
    Check if request method is GET
    request : 
        request data
    """
    if request.method:
        if request.method == 'GET':
            return True
    return False



def is_method_post(request) -> bool:
    """
    Check if request method is POST
    request : 
        request data
    """
    if request.method:
        if request.method == 'POST':
            return True
    return False



def get_valid_int(value: int, default: int = 0) -> int:
    """
    Get valid int param
    value : int
        value for validating
    default : int
        default value in case of exception
    """
    try:
        result = int(value)
    except:
        if not default:
            default = 0
        result = default
    return result



def get_valid_str(value: str, default: str = "") -> str:
    """
    Get valid str param
    value : str
        value for validating
    default : str
        default value in case of exception
    """
    try:
        if value:
            result = str(value)
        else:
            raise Exception("not valid str")  
        # TODO other validations
    except:
        if not default:
            default = ""
        result = default
    return result



def is_int_valid(value: int, exclude: list = []) -> bool:
    """
    Check if int value is valid
    value : int
        value for validating
    exclude : list
        list of invalid values
    """
    result = True
    if not isinstance(value, int) or isinstance(value, bool):
        result = False
    else:
        for val in exclude:
            if val == value:
                result = False
                break
    return result



def clean_val(value, replace_vals_old: list = [], replace_vals_new: list = []):
    """
    Clean parameter value. If no matches were found return original value.
    value :
        value of a parameter
    replace_vals_old : list
        list of values to be replaced
    replace_vals_new : list
        list of new values after replacing
    """
    result = value
    i = 0
    for val in replace_vals_old:
        if val == value:
            if i < len(replace_vals_new):
                result = replace_vals_new[i]
            break
        i += 1
    return result



def get_valid_float(value: float, default: float = 0) -> float:
    """
    Get valid float param
    value : float
        value for validating
    default : float
        default value in case of exception
    """
    try:
        result = float(value)
    except:
        if not default:
            default = 0
        result = default
    return result



def get_params_dict_from_query(qs: str):
    """
    Get dict params data from a query string
    qs: str
        a query string
    """   
    # Step 1: Remove the leading "?"
    qs1 = qs.lstrip("?")
    # Step 2: Parse it into a dict
    parsed = urllib.parse.parse_qs(qs1, keep_blank_values=True)
    # Step 3: Flatten values from list to string (optional)
    flattened = {k: v[0] if v else "" for k, v in parsed.items()}
    return flattened



def set_GET_item(request, key, value):
    """
    Set item of request.GET
    """
    request.GET._mutable = True
    request.GET[key] = value
    request.GET._mutable = False
    return True










