from django.contrib.auth.models import AbstractUser
from django.db import models


# Customizando o Model do user
class CustomUser(AbstractUser):
    """Representa um usuário.

    Atributes:
        first_name (str): Nome.
        last_name (str): Sobrenome.
        email (str): Email.
        role (str): Cargo (employee/admin).
        created_at (timestamp): Data de criação.
        updated_at (timestamp): Data de atualização.

    """

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
