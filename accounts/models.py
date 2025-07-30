from django.contrib.auth.models import AbstractUser
from django.db import models


# Customizando o Model do user
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(
        max_length=20,
        choices=[("employee", "Funcionário"), ("admin", "Administrador")],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # Autenticação via email e não via username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "role"]
