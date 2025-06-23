from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(
        max_length=20,
        choices=[("employee", "Employee"), ("admin", "Admin")],
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} | {self.role}"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
