# Utilities for numbers



def get_report_title_from_app_list(app_list: list, name: str) -> str:
    """
    Get a report title from an app list
    app_list : list
        app_list
    name: str
        report's object name
    """
    result = ""
    for app in app_list:
        for model in app["models"]:
            if model["object_name"] == name:
                result = model["name"]
                break
        if result:
            break
    return result















