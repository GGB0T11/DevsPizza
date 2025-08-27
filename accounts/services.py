from django.core.exceptions import ValidationError

from .models import CustomUser


def validate_password(password: str, confirm_password: str) -> None:
    if password != confirm_password:
        raise ValidationError("As senhas devem ser iguais!")
    if len(password) < 8:
        raise ValidationError("A senha deve ter no mínimo 8 caracteres!")


def create_account(data: dict) -> CustomUser:
    if CustomUser.objects.filter(email=data["email"]).exists():
        raise ValidationError("Já existe um usuário cadastrado com esse email, insira outro")

    validate_password(data["password"], data["confirm_password"])

    account = CustomUser.objects.create_user(
        username=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        role=data["role"],
        password=data["password"],
    )

    return account


def update_account(account: CustomUser, data: dict):
    if CustomUser.objects.filter(email=account.email).exclude(id=account.id).exists():
        raise ValidationError("O novo email que deseja inserir já está associado a uma conta!")

    account.first_name = data["first_name"]
    account.last_name = data["last_name"]
    account.email = data["email"]
    account.role = data["role"]

    password, confirm_password = data["password"], data["confirm_password"]

    if password and confirm_password:
        validate_password(password, confirm_password)

    return account
