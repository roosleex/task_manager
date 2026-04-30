from django.apps import apps
from ast import literal_eval
from typing import Any, Mapping
import locale


def list_get(l, index, default=""):
    """
    Safe method for getting a list element
    l: list
        iinstance of a list
    index: int
        index of an element
    default: any
        default value if the index out of bound
    """
    if not isinstance(index, int):
        return default
    if index < 0 or index >= len(l):
        return default
    return l[index] if index < len(l) else default


def eval_str(
    code: str,
    globals: dict[str, Any] | None = None,
    locals: Mapping[str, object] | None = None,
) -> Any:
    """
    Evaluate a string of code
    code : str
        a string containing code expression
    globals: dict
        provides a global namespace to eval()
    locals: dict
        contains the variables that eval() uses as local names when evaluating expression
    """
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Code must be a non-empty string")

    # ❌ Basic blacklist (not perfect, but adds protection)
    forbidden = [
        "__import__",
        "exec",
        "eval",
        "open",
        "os",
        "sys",
        "subprocess",
        "shutil",
        "input",
        "globals",
        "locals",
        "__",
    ]

    for word in forbidden:
        if word in code:
            raise ValueError(f"Unsafe expression: {word} is not allowed")

    # ✅ Restrict builtins
    safe_globals = {
        "__builtins__": {}
    }

    # allow user-provided globals (merge safely)
    if globals:
        safe_globals.update(globals)

    try:
        return eval(code, safe_globals, locals)
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {e}") from e



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



def latin_to_ukrainian(val: str) -> str:
    translit_map = {
        'A': 'А', 'B': 'В', 'C': 'С', 'E': 'Е', 'H': 'Н',
        'I': 'І', 'K': 'К', 'M': 'М', 'O': 'О', 'P': 'Р',
        'T': 'Т', 'X': 'Х', 'Y': 'У'
    }
    return ''.join(translit_map.get(char, char) for char in val)



def sort_dict_by_uk_ua(data: dict):
    """
    Sort dict keys by uk_UA.UTF-8 locale
    """
    old_locale = locale.setlocale(locale.LC_ALL)  # save current
    sorted_data = {}
    try:
        locale.setlocale(locale.LC_ALL, "uk_UA.UTF-8")
        sorted_data = dict(
            sorted(data.items(), key=lambda x: locale.strxfrm(x[0]))
        )
    finally:
        locale.setlocale(locale.LC_ALL, old_locale) # restore
    return sorted_data


def is_trusted_user(user) -> bool:
    """
    Check if a current user is trusted
    user : 
        user
    """
    try:
        if user and user.is_staff==True and user.is_active==True and user.is_authenticated:
            return True
    except Exception as e:
        pass
    return False



