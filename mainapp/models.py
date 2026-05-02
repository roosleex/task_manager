from django.db import models
from .base.models import BaseModel
from accounts.models import User


class Task(BaseModel):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=1000, null=True, blank=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    

class Profile(BaseModel):
    profile_img = models.ImageField(null=True, blank=True, default="user-default-ava.jpg")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)