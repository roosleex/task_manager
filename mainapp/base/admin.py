from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django.conf import settings
from mainapp.apps import MainappConfig
from accounts.apps import AccountsConfig
from reports.apps import ReportsConfig
from reports.admin import get_reports_app_list
from django.apps import apps



def get_app_list_item(name, object_name, app_url):
    from mainapp.admin.sites import MainappAdminSite
    return [{
        #"model": "",
        "name": name, 
        "object_name": object_name,
        "perms": {
            "add": True, 
            "change": True, 
            "delete": True, 
            "view": True
        },	
        "admin_url": app_url + object_name + "/",
        #"add_url": app_url + object_name + "/add/", 	
        "view_only": True,
    }]



class BaseModelAdmin(SimpleHistoryAdmin):
    """
    Base class for all admin models
    """
    list_per_page = 20
    save_as = settings.COMMON_CONFIG["is_btn_save_as_new"]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not settings.COMMON_CONFIG["is_delete_selected_action"]:
            if "delete_selected" in actions:
                del actions["delete_selected"]
        return actions

    class Meta:
        abstract = True
        
    class Media(object):
        js = (
            "js/doubleScroll.js",
        )

    def get_exclude(self, request, obj=None):
        exclude = super().get_exclude(request, obj)
        if exclude:
            exclude += ["deleted"]
        else:
            exclude = ["deleted"]
        return exclude
    


class BaseMainappAdminSite(admin.AdminSite):
    """
    Base class for mainapp admin site
    """
    site_header = settings.ADMIN_SITE_CONFIG["site_header"]
    site_title = settings.ADMIN_SITE_CONFIG["site_title"]
    index_title = settings.ADMIN_SITE_CONFIG["index_title"]
    admin_url1 = settings.ADMIN_URL1
    custom_actions_label = "custactions" # label for custom actions

    def each_context(self, request):
        context = super().each_context(request)

        context.update({
            "COMPANY_DEFAULT_GEO_LOCATION": settings.COMPANY_DEFAULT_GEO_LOCATION,
            "admin_url1": self.admin_url1,
            "JQUERY_PATH_FILE": settings.JQUERY_PATH_FILE,
            "show_save_and_continue": settings.COMMON_CONFIG["is_btn_save_and_continue_editing"],
        })

        return context
    
    def get_active_app_name(self, request):
        path = request.get_full_path()
        path_app_name = path.split("/")[2]
        print(f"path={path}")
        print(f"path_app_name={path_app_name}")
        return path_app_name

    def is_app_active(self, request, app_name):
        """
        Define what app is current active
        app_name : str
        """
        path_app_name = self.get_active_app_name(request) 
        return path_app_name == app_name

    def is_index_page_active(self, request):
        return self.is_app_active(request, "")
    
    def is_mainapp_active(self, request):
        return self.is_app_active(request, MainappConfig.name)
    
    def is_accounts_active(self, request):
        return self.is_app_active(request, AccountsConfig.name)
    
    def is_reports_active(self, request):
        return self.is_app_active(request, ReportsConfig.name)

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        custactions_app_list = self.get_custactions_app_list(request)
        if len(custactions_app_list) > 0:
            app_list += custactions_app_list
        reports_app_list = get_reports_app_list(request)
        if len(reports_app_list) > 0:
            app_list += reports_app_list
        # Sort the models alphabetically within each app.
        # print(f"app_list = {app_list}")
        for app in app_list:
            if app['app_label'] == 'mainapp':
                app["models"].sort(key=lambda x: apps.get_model(app_label=app['app_label'], model_name=x["object_name"]).ADMIN_MENU_ORDER)
            else:
                app["models"].sort(key=lambda x: x["name"])
        app_list = self.get_positioned_app_list(request, app_list)
        # print(f"app_list = {app_list}")
        # print(f"app_list[2]={app_list[2]}")
        #print(app_list)
        return app_list

    def get_positioned_app_list(self, request, app_list):
        # print(f"is_app_active={self.is_app_active(request, MainappConfig.name)}")
    
        positions = {
            MainappConfig.name: {
                MainappConfig.name: 0,
                ReportsConfig.name: 1,
                self.custom_actions_label: 2,
                AccountsConfig.name: 3,
            }, 
            ReportsConfig.name: {
                ReportsConfig.name: 0,
                MainappConfig.name: 1,
                self.custom_actions_label: 2,
                AccountsConfig.name: 3,
            },
            self.custom_actions_label: {
                self.custom_actions_label: 0,
                MainappConfig.name: 1,
                ReportsConfig.name: 2,
                AccountsConfig.name: 3,
            },
            AccountsConfig.name: {
                AccountsConfig.name: 0,
                MainappConfig.name: 1,
                ReportsConfig.name: 2,
                self.custom_actions_label: 3,  
            },   
        }
            
        app_name = self.get_active_app_name(request)
        if app_name == "":
            app_name = MainappConfig.name
        
        # active_pos = positions.get(app_name)
        active_pos = positions.get(MainappConfig.name)
        # print(f"active_pos={active_pos}")
        if not active_pos:
            return

        new_app_list = [None] * len(active_pos)
        for app in app_list:
            # print(active_pos.get(app['app_label']))
            # print(f"app['app_label']={app['app_label']}")
            # print(f"pos={active_pos.get(app['app_label'])}")
            # new_app_list.insert(active_pos.get(app['app_label']), app)
            new_app_list[active_pos.get(app['app_label'])] = app

        # clear None items
        # item is None when user has no permissions on it
        new_app_list2 = []
        for app in new_app_list:
            if app != None:
                new_app_list2.append(app)

        # print(f"new_app_list[2]={new_app_list[2]}")    
        return new_app_list2
        # print(f"new_app_list={new_app_list}")
        app_list = new_app_list
        # print(f"app_list={app_list}")

        # other_pos = 2
        # new_app_list = []
        # for app in app_list:
        #     if self.is_index_page_active(request):
        #         if app['app_label'] == MainappConfig.name:
        #             new_app_list.insert(0, app)
        #         elif app['app_label'] == AccountsConfig.name:
        #             new_app_list.insert(1, app)
        #         else:
        #             new_app_list.insert(other_pos, app)
        #             other_pos +=1
        #     elif self.is_mainapp_active(request):
        #         if app['app_label'] == MainappConfig.name:
        #             new_app_list.insert(0, app)
        #     elif self.is_accounts_active(request):
        #         if app['app_label'] == AccountsConfig.name:
        #             new_app_list.insert(0, app)
        #     elif self.is_reports_active(request):
        #         if app['app_label'] == ReportsConfig.name:
        #             new_app_list.insert(0, app)
        # return new_app_list

    def get_custactions_app_list(self, request, menu_items = None):
        app_url = "/" + self.admin_url1 + "/" + self.custom_actions_label + "/"
        # print(f"user_permissions.all() = {request.user.user_permissions.all()}")
        # perms = request.user.user_permissions.all()
        # print(f"perms = {perms}")
        # for perm in perms:
        #     print(f"perm = {perm}")
        # print(f"request.user.get_user_permissions() = {request.user.get_user_permissions()}")
        # for perm in request.user.get_user_permissions():
        #     print(f"perm = {perm}")
        # print(f"request.user.has_perm('accounts.cemactions_add_occupied_place') = {request.user.has_perm('accounts.cemactions_add_free_place')}")
        items = []
        for item in menu_items:
            perm = item["perm"]
            name = item["name"]
            object_name = item["object_name"]
            if request.user.has_perm(perm):
                items += get_app_list_item(name, object_name, app_url)
        
        app_list = []
        if len(items) > 0:
            app_list = [{
                "name": settings.ADMIN_SITE_CONFIG["app_list_custom_actions_app_name"], 
                "app_label": self.custom_actions_label, 
                "app_url": app_url, 
                "has_module_perms": True, 
                "models": items,
            }]

        return app_list

    def get_common_context(self, request):
        """
        Get common context
        request
            request
        """
        app_list = self.get_app_list(request)
        context = {}
        context["has_delete_permission"] = True
        context["has_add_permission"] = True
        context["has_change_permission"] = True
        context["has_view_permission"] = True
        context["has_permission"] = True
        context["site_url"] = "/"
        context["site_header"] = self.site_header
        context["site_title"] = self.site_title
        context["index_title"] = self.index_title
        context["app_list"] = app_list
        context["available_apps"] = app_list
        context["is_nav_sidebar_enabled"] = True
        context["user"] = request.user
        return context
            
    """def has_permission(self, request):
        has_permis = super().has_permission(request)
        #if not request.user.is_superuser:
        #    if is_model_registered_in_admin_site(self, 'django.contrib.auth.models.Group'):
        #        self.unregister(Group)
        #    if is_model_registered_in_admin_site(self, 'django.contrib.auth.models.User'):
        #        self.unregister(User)
        print(f'request.user.is_active = {request.user.is_active}')
        print(f'request.user.is_staff = {request.user.is_staff}')
        return has_permis"""
    



    
    