from django.db import models
from abc import abstractmethod



class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


# Base class for all models
class BaseModel(models.Model):
    # Set in child classes
    # Ordinal number of a class in the admin menu
    ADMIN_MENU_ORDER = 0

    # For soft deleting
    deleted = models.BooleanField(default=False)

    objects = BaseModelManager()

    class Meta:
        abstract = True

    def delete(self):
        """
        Delete softly
        """
        self.deleted = True
        self.save()

    @classmethod
    @abstractmethod
    def get_settings(cls):
        """
        Get model settings
        """
        return None
    
    
