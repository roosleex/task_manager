from django.test import SimpleTestCase
from ..report_utils import *



class ReportUtilsTests(SimpleTestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_get_report_title_from_app_list(self):
        app_list = [
            {
                'name': 'Звіти',
                'app_label': 'reports', 
                'app_url': '/garbadm/reports/', 
                'has_module_perms': True, 
                'models': [
                    {
                        'name': 'Звіт розпізнаних номерних знаків', 
                        'object_name': 'license_plate_recognition', 
                        'admin_url': '/garbadm/reports/form/license_plate_recognition/', 
                        'view_only': True
                    }
                ]
            }
        ]
        actual = get_report_title_from_app_list(app_list, "license_plate_recognition")
        expected = "Звіт розпізнаних номерних знаків"
        self.assertEqual(actual, expected)


        app_list = [
            {
                'name': 'Звіти777',
                'app_label': 'reports', 
                'app_url': '/garbadm/reports/', 
                'has_module_perms': True, 
                'models': [
                    {
                        'name': 'Звіт розпізнаних номерних знаків777', 
                        'object_name': 'license_plate_recognition777', 
                        'admin_url': '/garbadm/reports/form/license_plate_recognition/', 
                        'view_only': True
                    }
                ]
            },
            {
                'name': 'Звіти',
                'app_label': 'reports', 
                'app_url': '/garbadm/reports/', 
                'has_module_perms': True, 
                'models': [
                    {
                        'name': 'Звіт розпізнаних номерних знаків', 
                        'object_name': 'license_plate_recognition', 
                        'admin_url': '/garbadm/reports/form/license_plate_recognition/', 
                        'view_only': True
                    }
                ]
            }
        ]
        actual = get_report_title_from_app_list(app_list, "license_plate_recognition")
        expected = "Звіт розпізнаних номерних знаків"
        self.assertEqual(actual, expected)


        app_list = [
            {
                'name': 'Звіти',
                'app_label': 'reports', 
                'app_url': '/garbadm/reports/', 
                'has_module_perms': True, 
                'models': [
                    {
                        'name': 'Звіт розпізнаних номерних знаків1', 
                        'object_name': 'license_plate_recognition1', 
                        'admin_url': '/garbadm/reports/form/license_plate_recognition/', 
                        'view_only': True
                    },
                    {
                        'name': 'Звіт розпізнаних номерних знаків2', 
                        'object_name': 'license_plate_recognition2', 
                        'admin_url': '/garbadm/reports/form/license_plate_recognition/', 
                        'view_only': True
                    },
                    {
                        'name': 'Звіт розпізнаних номерних знаків3', 
                        'object_name': 'license_plate_recognition3', 
                        'admin_url': '/garbadm/reports/form/license_plate_recognition/', 
                        'view_only': True
                    }
                ]
            }
        ]
        actual = get_report_title_from_app_list(app_list, "license_plate_recognition")
        expected = ""
        self.assertEqual(actual, expected)


        app_list = [
            {
                'name': 'Звіти',
                'app_label': 'reports', 
                'app_url': '/garbadm/reports/', 
                'has_module_perms': True, 
                'models': [
                    {
                        'name': 'Звіт розпізнаних номерних знаків1', 
                        'object_name': 'license_plate_recognition1', 
                        'admin_url': '/garbadm/reports/form/license_plate_recognition/', 
                        'view_only': True
                    },
                    {
                        'name': 'Звіт розпізнаних номерних знаків2', 
                        'object_name': 'license_plate_recognition2', 
                        'admin_url': '/garbadm/reports/form/license_plate_recognition/', 
                        'view_only': True
                    },
                    {
                        'name': 'Звіт розпізнаних номерних знаків3', 
                        'object_name': 'license_plate_recognition3', 
                        'admin_url': '/garbadm/reports/form/license_plate_recognition/', 
                        'view_only': True
                    }
                ]
            }
        ]
        actual = get_report_title_from_app_list(app_list, "license_plate_recognition3")
        expected = "Звіт розпізнаних номерних знаків3"
        self.assertEqual(actual, expected)

        
        
       



    