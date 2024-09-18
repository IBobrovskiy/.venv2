from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages
from .forms import LoginForm
from .models import Users
import logging
from django.contrib.auth.hashers import check_password

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')


def register(request):
    print("Функция register вызвана")

    if request.method == 'POST':
        form = UserForm(request.POST)
        print("Метод POST")
        if form.is_valid():
            print("Форма валидна")
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  # Хэшируем пароль
            user.save()  # Сохраняем пользователя в БД
            print('Успешно зарегистрировались!')
            return redirect('success')  # Перенаправление на страницу успеха
        else:
            form = UserForm(request.POST)
            print("Форма не валидна")
            print(form.errors)
            form = UserForm()  # Создаем новый экземпляр формы для GET-запроса
    else:
        form = UserForm()

    return render(request, 'login.html', {'form2': form})  # Возвращаем форму обратно на страницу


def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password'].strip()
            logger.debug(f"Попытка входа для email: {email}")

            try:
                user = Users.objects.get(email=email)
                logger.debug(f"Пользователь найден: {user.username}")

                if user.validate_password(password):
                    request.session['user_id'] = user.id
                    logger.info(f"Пользователь {user.username} успешно вошел в систему.")
                    return redirect('success')
                else:
                    logger.warning(f"Неверный пароль для пользователя: {user.username}")
                    messages.error(request, 'Неверный пароль.')
            except Users.DoesNotExist:
                logger.error(f"Пользователь с email {email} не существует.")
                messages.error(request, 'Пользователь с таким email не существует')

    return render(request, 'login.html', {'form': form})


def success(request):
    return render(request, 'success.html')
