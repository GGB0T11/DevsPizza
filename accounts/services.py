from django.core.exceptions import ValidationError

from .models import CustomUser


def validate_email(email: str, account_id=None) -> list:
    """Valida email único"""
    errors = []
    if account_id:
        exists = CustomUser.objects.filter(email=email).exclude(id=account_id).exists()
    else:
        exists = CustomUser.objects.filter(email=email).exists()
    if exists:
        errors.append("Já existe uma conta com esse email.")
    return errors


def validate_password(password: str, confirm_password: str) -> list:
    """Valida senha e confirmação"""
    errors = []
    if password != confirm_password:
        errors.append("As senhas devem ser iguais!")
    if len(password) < 8:
        errors.append("A senha deve ter no mínimo 8 caracteres!")
    return errors


def create_account(data: dict) -> CustomUser:
    """Cria a conta"""
    errors = []

    errors.extend(validate_email(data["email"]))
    errors.extend(validate_password(data["password"], data["confirm_password"]))

    if errors:
        raise ValidationError(errors)

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
    """Atualiza as informações de uma conta"""
    error = []

    password, confirm_password = data["password"], data["confirm_password"]
    if password and confirm_password:
        error = validate_password(password, confirm_password)

    if error:
        raise ValidationError(error)

    account.first_name = data["first_name"]
    account.last_name = data["last_name"]
    account.email = data["email"]
    account.role = data["role"]

    return account
