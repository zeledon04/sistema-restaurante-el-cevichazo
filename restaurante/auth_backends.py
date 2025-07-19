from django.contrib.auth.backends import BaseBackend
from .models import Usuarios

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Usuarios.objects.get(usuario=username)
            if user.contrasena == password:
                return user
        except Usuarios.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist:
            return None
