from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.models import User


class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return
        try:
            user = User.objects.get(email=username)
        except UserModel.DoesNotExist:
            return
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
