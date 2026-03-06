# accounts configurations

from environs import Env
env = Env()
env.read_env()



USER_CONFIG = {
    "is_delete_selected_action": False,
    "fields": ["tel",],
    "list_display": env.list("USER_CONFIG_LIST_DISPLAY"),
}



USER_GROUP_CONFIG = {
    "is_delete_selected_action": False,
    "fields": ["name", "description", "permissions"],
    "list_display": ["name", "description"],
}
