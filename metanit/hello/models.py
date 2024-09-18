from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Users(models.Model):
    username = models.CharField(max_length=150, unique=True, blank=False)
    surname = models.CharField(max_length=150, blank=False)  # Поле для фамилии
    email = models.EmailField(unique=True, blank=False)  # Обязательное поле
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        # Хэшируем пароль только при создании нового пользователя
        if self.pk is None or 'password' in kwargs:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def validate_password(self, raw_password):
        raw_password = raw_password.strip()
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username} {self.surname}"
