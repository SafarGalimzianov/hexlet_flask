import os # Импорт модуля os для работы с переменными окружения
import psycopg2 # Импорт модуля psycopg2 для работы с БД PostgreSQL
from flask import ( # Импорт модуля flask
    get_flashed_messages, # Получение информационных сообщений пользователю
    flash, # Отображение информационных сообщений пользователю
    Flask, # Импорт класса Flask
    redirect, # Перенаправление
    render_template, # Отображение шаблона
    request, # Получение данных ответа
    url_for, # Получение URL по названию обработчика запроса
)

from email_validator import validate_email, EmailNotValidError # Импорт функции валидации email

# Класс UserRepositry с методами обращения к базе данных
from user_repository import UserRepository
from dotenv import load_dotenv # Импорт функции для загрузки переменных окружения из файла .env
'''
Инстанцируем класс Flask с именем приложения
Имя приложения - это имя модуля, в котором оно находится
В данном случае это main
Это необходимо для того, чтобы Flask мог найти
по относительным путям шаблоны и статические файлы
'''
app = Flask(__name__)

# Настраиваем секретный ключ для подписи данных сессии
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# Настраиваем URL базы данных для подключения
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

# Создаем связь с баззой данных
conn = psycopg2.connect(app.config['DATABASE_URL'])

# Создаем таблицу в базе данных
repo = UserRepository(conn)


# Валидация пользователя
def validate(user: dict) -> dict:
    errors = {} # Пустой словарь с длиной 0, равен False
    if not user.get('name'): # Если нет имени пользователя
        errors['name'] = 'Cannot be blank'
    try:
        validate_email(user['email']) # Проверка email на валидность
    except KeyError:
        errors['email'] = 'Cannot be blank'
    except EmailNotValidError:
        errors['email'] = 'Email is not valid'
    except Exception as e:
        errors['email'] = 'Something went wrong'
    return errors


# Декоратор для обработки запроса GET на URL /
@app.route('/')
def home(): # Обработчик запроса. Название функции не имеет значения
    return render_template('users/home.html') #Отображение на странице текста без обработки


# Декоратор для обработки запроса GET на URL /users
# Отображение списка пользователей
@app.get('/users')
def users_get(): # Имена обработчиков принято называть по URL и методу или результату
    # Получение flash сообщений и указание их категорий
    messages = get_flashed_messages(with_categories=True)

    # Получение параметра поиска из строки запроса
    term = request.args.get('term')

    # Получение пользователей из базы данных по поисковому запросу
    # Фильтрация реализована в методе get_users класса UserRepository
    # так как БД умеют фильтровать данные быстрее и эффективнее, чем Python
    if term:
        users=repo.get_by_term(term)
    else:
        users=repo.get_content()

    # Отображение шаблона с пользователями
    return render_template(
        'users/index.html', #Путь к шаблону
        # Передача переменных в шаблон. Принято передавать словарь с одинаковыми именами переменных
        users=users,
        search=term,
        messages=messages,
    )


# Декоратор для обработки запроса POST на URL /users
# Форма в users/index.html содержит action={{ url_for('users_post') }} и method='post'
@app.post('/users')
def users_post():
    # Получение данных из формы запроса
    user = request.form.to_dict()
    
    errors = validate(user)
    if errors: # Если errors не пустой словарь {}
        return render_template(
            'users/new.html',
            user=user,
            errors=errors,
        )

    # Добавление пользователя в базу данных
    repo.save(user)

    # Отправка flash сообщения
    flash('User added successfully', 'info')

    # Перенаправление на страницу с пользователями
    return redirect(url_for('users_get'), code=302)


# Декоратор для обработки запроса GET на URL /users/new
# Отображение формы добавления нового пользователя
@app.get('/users/new')
def users_new():
    user = {'name':'', 'email': ''} # Передача пользователя с пустыми значениями в шаблон
    errors = {} # Передача пустого словаря с ошибками в шаблон

    return render_template(
        'users/new.html',
        user=user,
        errors=errors,
    )


# Декоратор длоя обработки запроса GET на URl /users/<id>/edit
# Отображение формы редактирования пользователя
@app.get('/users/<int:id>/edit')
def users_edit(id):
    user = repo.find(id)
    errors = {}

    return render_template(
        'users/edit.html',
        user=user,
        errors=errors,
    )


# Декоратор для обработки запроса POST на URL /users/<id>/patch
# Обновление пользователя
# Форма в users/edit.html содержит action={{ url_for('users_patch') }} и method='post'
@app.post('/users/<int:id>/patch')
def users_patch(id):
    user_to_update = repo.find(id) # Получение пользователя из базы данных
    user = request.form.to_dict() # Получение пользователя из формы

    errors = validate(user)
    if errors:
        return render_template(
            'users/edit.html',
            user=user_to_update,
            errors=errors,
        ), 422
    
    user['id'] = id
    repo.save(user)
    flash('Пользователь успешно обновлен', 'success')

    return redirect(url_for('users_get'), code=302)
    

# Декоратор для обработки запроса POST на URL /users/<id>/delete
# Удаление пользователя
# Форма в users/edit.html содержит action={{ url_for('users_delete')}} и method='post'
@app.post('/users/<int:id>/delete')
def users_delete(id):
    repo.delete(id)
    flash('User deleted successfully', 'success')

    return redirect(url_for('users_get'), code=302)


# Декоратор для обработки запроса GET на URL /users/<id>
# Отображение информации о пользователе
@app.route('/users/<int:id>')
def users_show(id):
    user = repo.find(id) # Получение пользователя из базы данных

    return render_template(
        'users/show.html',
        user=user,
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404