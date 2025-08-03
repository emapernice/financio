from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass  # Por ahora no agregamos campos extra

    def __str__(self):
        return self.username
