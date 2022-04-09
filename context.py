import json

from marshmallow import ValidationError

from model.models import Employee, Department, db, User, EntityRequest, EmployeeRequest, DepartmentRequest
from model.schemas.schemas import EmployeeSchema, DepartmentSchema, UserSchema


def get_employees():
    """
    Возвращает список сотрудников.
    Type - list
    """
    return get_data_with_schema(Employee, EmployeeSchema())


def get_departments():
    """
    Возвращает список отделов, в котором работают сотрудники.
    Type - list
    """
    return get_data_with_schema(Department, DepartmentSchema())


def get_data_with_schema(model, schema):
    """
    Функция для получения данных по модели.
    """
    try:
        entities = model.query.all()
        data = [schema.dump(entity) for entity in entities]
        return data
    except Exception as ex:
        print(ex)
        raise ex


def add_employee(request_data, username):
    """
    Добавление сотрудника.
    Если названия отдела отличается от тех, что в бд - создается новый отдел
    :param request_data: тело HTTP-запроса в формате строки json
    :param username: никнейм пользователя
    """
    try:
        request_id = add_request(User.query.filter(User.username == username).first().id)
        # Валидация схемы, если отправлены неправильные данные, то сработает ValidationError
        employee_dict = EmployeeSchema(many=False).loads(request_data)
        if 'DepartmentName' in employee_dict['Department'] and 'DepartmentId' not in employee_dict['Department']:
            department_id = add_department_by_name(employee_dict['Department']['DepartmentName'], request_id)
            employee_dict['Department']['DepartmentId'] = department_id
        employee = Employee(employee_dict['LastName'], employee_dict['MiddleName'], employee_dict['FirstName'],
                            employee_dict['Birthday'], employee_dict['EmploymentDate'],
                            employee_dict['Department']['DepartmentId'])
        db.session.add(employee)
        db.session.commit()
        logging_operation(employee, EmployeeRequest(), request_id)
        return True, None
    except ValidationError as v:
        return False, v
    except Exception as ex:
        return False, ex


def add_department_by_name(department_name, request_id):
    """
    Добавление отдела.
    :param department_name: название отдела
    :param request_id: ID запроса для логирования
    """
    d = Department(department_name)
    db.session.add(d)
    db.session.commit()
    logging_operation(d, DepartmentRequest(), request_id)
    return d.DepartmentId


def update_employees(request_json_array, username):
    """
    Обновление записей сотрудников в бд
    Если названия отдела отличается от тех, что в бд - создается новый отдел
    :param request_json_array: тело HTTP-запроса в формате строки json
    :param username: никнейм пользователя
    """
    try:
        array = json.loads(request_json_array.decode('utf-8'))
        #Валидация схемы, если отправлены неправильные данные, то сработает ValidationError
        employees = EmployeeSchema(many=True).load(array)
        request_id = add_request(User.query.filter(User.username == username).first().id)
        for employee_json in employees:
            employee = Employee.query.get(employee_json['EmployeeId'])
            logging_operation(employee, EmployeeRequest(), request_id, "UPDATE")
            employee.LastName = employee_json['LastName']
            employee.MiddleName = employee_json['MiddleName']
            employee.FirstName = employee_json['FirstName']
            employee.Birthday = employee_json['Birthday']
            employee.EmploymentDate = employee_json['EmploymentDate']
            if ('DepartmentId' not in employee_json['Department']):
                department = Department.query.filter(
                    Department.DepartmentName == employee_json['Department']['DepartmentName']).first()
                if (department is None):
                    department_id = add_department_by_name(employee_json['Department']['DepartmentName'], request_id)
                    employee_json['Department']['DepartmentId'] = department_id
                else:
                    employee_json['Department']['DepartmentId'] = department.DepartmentId
            employee.DepartmentId = employee_json['Department']['DepartmentId']
            db.session().commit()
        return True, None
    except ValidationError as v:
        print(v)
        return False, v
    except Exception as ex:
        print(ex)
        return False, ex


def auth(username, password):
    """
    Функция проверки пользователя. Используется для аутентификации.
    :param username: никнейм пользователя
    :param password: пароль пользователя, используется для проверки путем хеширования
    """
    user = User.query.filter(User.username == username).first()
    if user and user.check_password(password):
        return True
    return False


def check_user(request_json):
    """
    Проверка наличия пользователя в бд
    :param request_json: тело HTTP-запроса в формате строки json
    """
    user_json = request_json.decode('utf-8')
    user = User.query.filter(User.username == user_json["username"]).first()
    if user and user.check_password(user_json["password"]):
        return True
    return False


def add_user(request_json):
    """
    Добавление пользователя в бд
    :param request_json_array: тело HTTP-запроса в формате строки json
    """
    user = UserSchema().loads(request_json)
    db.session.add(user)
    db.session.commit()
    return True


def fill_tables():
    """
    Добавление тестовых данных в бд
    """
    db.create_all()
    db.session.commit()
    user = User("test", "test@mail.ru", "P@ss")
    db.session.add(user)
    print(f"Пользователь username: {user.username} добавлен")
    department = Department("Test department")
    db.session.add(department)
    print(f"Департамент '{department.DepartmentName}' добавлен")
    db.session.commit()
    employee = Employee("Test", "Test", "Test", "2000-01-02", "2020-08-07", department.DepartmentId)
    db.session.add(employee)
    print(f"Сотрудник {employee.LastName} {employee.FirstName} {employee.MiddleName} добавлен")
    db.session.commit()


def add_request(user_id):
    """
    Добавление записи о запросе в бд
    :param user_id: ID пользователя в бд
    """
    request = EntityRequest(user_id)
    db.session.add(request)
    db.session.commit()
    return request.id


def logging_operation(model, model_request, request_id, operation='INSERT'):
    """
    Функция для логирования операции вставки или обновления в бд
    :param model: экземпляр класса модели сущности (в данном примере это Department или Employee)
    :param model_request: экземпляр класса модели сущности логирования (в данном примере это DepartmentRequest или EmployeeRequest)
    """
    model_request.get_entity(model)
    model_request.Operation = operation
    model_request.RequestId = request_id
    db.session.add(model_request)
    db.session.commit()


def model_rollback(Model, Model_logging, request_id):
    """
    В данной функции происходи откат изменений входной модели.
    :param Model: класс модели сущности (в данном примере это Department или Employee)
    :param Model_logging: класс модели сущности логирования (в данном примере это DepartmentRequest или EmployeeRequest)
    :param request_id: ID запроса в бд
    """
    model_requests = Model_logging.query.filter(Model_logging.RequestId == request_id).all()
    for model_request in model_requests:
        if model_request.Operation == "INSERT":
            m = Model.query.get(model_request.EntityId)
            db.session.delete(m)
        if model_request.Operation == "UPDATE":
            m = Model.query.get(model_request.EntityId)
            m.update_from_model_logging(model_request)
    db.session.commit()


def rollback_changes(username):
    """
    В данной функции происходи откат ВСЕХ изменений пользователя.
    :param username: никнейм пользователя
    """
    user_id = User.query.filter(User.username == username).first().id
    request = EntityRequest.query.filter(EntityRequest.UserId == user_id).order_by(EntityRequest.id.desc()).first()
    if not request.rollback_status:
        model_rollback(Employee, EmployeeRequest, request.id)
        model_rollback(Department, DepartmentRequest, request.id)
        request.rollback_status = True
        db.session.commit()

    return True
