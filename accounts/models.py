# from simple_history.models import HistoricalRecords
from .base.models import BaseUser, BaseUserGroup



class User(BaseUser):
    # history = HistoricalRecords()

    class Meta(BaseUser.Meta):
        # add custom permissions
        # permissions = [
        #     ("cemactions_add_occupied_place", 'Can add зайняте місце'),
        #     ('cemactions_add_free_place', 'Can add вільне місце'),
        #     # 
        #     ('reports_view_burials', 'Can view звіт поховань'),
        #     ('reports_view_booked_places', 'Can view звіт бронювань'),
        #     ('reports_view_free_places', 'Can view звіт вільних місць'),
        #     #
        #     ('reports_export_burials', 'Can export звіт поховань'),
        #     ('reports_export_booked_places', 'Can export звіт бронювань'),
        #     ('reports_export_free_places', 'Can export звіт вільних місць'),
        # ]
        pass



class UserGroup(BaseUserGroup):
    # history = HistoricalRecords()
    pass
