from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or not password:
            return None

        users = UserModel._default_manager.filter(
            Q(**{f"{UserModel.USERNAME_FIELD}__iexact": username}) | Q(username__iexact=username)
        )

        for user in users:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
