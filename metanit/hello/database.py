from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from  .models import Users

from .forms import UserForm

class auth:


    def authenticate_user(self, email, password):  # Добавьте self
        try:
            user = Users.objects.get(email=email)
            # Проверяем пароль
            if check_password(password, user.password):  # Используйте check_password для проверки
                return True  # Пароль верный
            else:
                return False  # Неверный пароль
        except Users.DoesNotExist:  # Исправлено здесь
            return False  # Пользователь не найден
