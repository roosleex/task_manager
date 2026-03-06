# common configurations

from environs import Env
env = Env()
env.read_env()



COMMON_CONFIG = {
    "prog_name": "Task manager",
    "prog_name_verbose": "Task manager",
    "prog_version": "1.0.0",
    "prog_copyright": "\xA9 roosleex | All rights reserved",
    #
    "is_delete_selected_action": False,
    "is_btn_save_and_continue_editing": env.bool("COMMON_IS_BTN_SAVE_AND_CONTINUE_EDITING", default=True),
    "is_btn_save_as_new": env.bool("COMMON_IS_BTN_SAVE_AS_NEW", default=False),
    #
    "main_app_config_verbose_name": env.str("COMMON_CONFIG_MAIN_APP_CONFIG_VERBOSE_NAME"),
    "main_app_config_verbose_name_plural": env.str("COMMON_CONFIG_MAIN_APP_CONFIG_VERBOSE_NAME_PLURAL"),
    "accounts_config_verbose_name": "User",
    "accounts_config_verbose_name_plural": "Users",
    "reports_config_verbose_name": "Report",
    "reports_config_verbose_name_plural": "Reports",
    "user_guide_config_verbose_name": "User manual",
    "user_guide_config_verbose_name_plural": "User manuals",
    #
}
