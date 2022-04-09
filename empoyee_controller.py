from flask import Blueprint, Response, request, jsonify
from model.models import basic_auth
from marshmallow import ValidationError
import context

employee_controller = Blueprint('employee_controller', __name__)


@employee_controller.route('/api/signup', methods=["POST"])
def signup():
    """
    Регистрация пользователя в системе.
    В контроллере используется Basic Auth
    """
    if context.add_user(request.data):
        return Response("You're successfully registered", status=200)
    return Response("User already existing", status=500)


@employee_controller.route('/api/login', methods=["POST"])
def check_user():
    """
    Проверка наличия пользователя в системе.
    """
    if context.check_user(request.data):
        return Response("User is existing", status=200)
    return Response("User is NOT existing", status=500)


@basic_auth.verify_password
def authenticate(username, password):
    """
    Функция для проверки Basic Auth.
    Если в запросе не будет задан корректный username и password, то на crud запросах будет 401 код ошибки.
    """
    if context.auth(username, password):
        return username


@employee_controller.route('/api', methods=['GET'])
@basic_auth.login_required
def get_employees():
    """
    Возвращает список сотрудников.
    """
    return jsonify(context.get_employees())


@employee_controller.route('/api/add_employee/', methods=['POST'])
@basic_auth.login_required
def add_employee():
    """
    Добавление сотрудника в бд.
    """
    try:
        add_result = context.add_employee(request.data, request.authorization.username)
        if add_result[0]:
            return Response(status=200)
        if isinstance(add_result[1], ValidationError):
            return Response('Wrong data', status=400)
        return Response(status=500)
    except Exception as ex:
        print(ex)
        return Response(status=500)


@employee_controller.route('/api/edit_employees/', methods=['PUT'])
@basic_auth.login_required
def update_employees():
    """
    Изменение уже существующего в бд сотрудника
    """
    update_result = context.update_employees(request.data, request.authorization.username)
    if update_result[0]:
        return Response(status=200)
    if isinstance(update_result[1], ValidationError):
        return Response('Wrong data', status=400)
    return Response(status=500)


@employee_controller.route('/api/rollback/')
@basic_auth.login_required
def rollback_changes():
    """
    Откат изменений в рамках одного запроса.
    Откатывается запрос по username.
    """
    context.rollback_changes(request.authorization.username)
    print('Changes has rollback')
    return Response(status=200)


@employee_controller.route('/api/fill')
def fill():
    """
    Функция для заполнения бд тестовыми данными
    """
    context.fill_tables()
    return Response('Entities are created!', status=200)
