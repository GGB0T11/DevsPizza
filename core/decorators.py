from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def admin_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.role == "admin" or request.user.is_staff:
            return func(request, *args, **kwargs)
        else:
            messages.error(request, "Acesso restrito a Adiministradores")
            return redirect("home")

    return wrapper
