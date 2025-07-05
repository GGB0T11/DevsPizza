from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.warning(self.request, "Antes de continuar efetue o Login")
        return super().handle_no_permission()


class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.role == "admin" or request.user.is_staff):
            messages.error(request, "Somente admins podem acessar essa área!")
            return redirect(reverse("home"))

        return super().dispatch(request, *args, **kwargs)
