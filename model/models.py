from datetime import datetime

from flask_httpauth import HTTPBasicAuth
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
basic_auth = HTTPBasicAuth()


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(500), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Department(db.Model):
    __tablename__ = 'Department'
    DepartmentId = db.Column(db.Integer, primary_key=True)
    DepartmentName = db.Column(db.String(500), nullable=False)
    CreateDate = db.Column(db.DateTime(), default=datetime.now)
    UpdateDate = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    def __init__(self, name):
        self.DepartmentName = name

    def update_from_model_logging(self, model_logging):
        self.DepartmentName = model_logging.DepartmentName


class Employee(db.Model):
    __tablename__ = 'Employee'
    EmployeeId = db.Column(db.Integer, primary_key=True)
    LastName = db.Column(db.String(100), nullable=False)
    MiddleName = db.Column(db.String(100), nullable=True)
    FirstName = db.Column(db.String(100), nullable=False)
    Birthday = db.Column(db.DATETIME, nullable=False)
    EmploymentDate = db.Column(db.DATETIME, nullable=False)
    CreateDate = db.Column(db.DateTime(), default=datetime.now)
    UpdateDate = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    DepartmentId = db.Column(db.Integer, db.ForeignKey('Department.DepartmentId'))
    Department = db.relationship('Department', foreign_keys='Employee.DepartmentId')
    db.ForeignKeyConstraint(['DepartmentId'], ['Department.DepartmentId'], name='fk_employee_department')

    def __init__(self, lastname, middlename, firstname, birthday, employmentdate, departmentid):
        self.LastName = lastname
        self.MiddleName = middlename
        self.FirstName = firstname
        self.Birthday = birthday
        self.EmploymentDate = employmentdate
        self.DepartmentId = departmentid

    def update_from_model_logging(self, model_logging):
        self.LastName = model_logging.LastName
        self.MiddleName = model_logging.MiddleName
        self.FirstName = model_logging.FirstName
        self.Birthday = model_logging.Birthday
        self.EmploymentDate = model_logging.EmploymentDate
        self.DepartmentId = model_logging.DepartmentId


class EntityRequest(db.Model):
    __tablename__ = 'EntityRequest'
    id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.id'))
    User = db.relationship('User', foreign_keys='EntityRequest.UserId')
    rollback_status = db.Column(db.Boolean, default=False)

    def __init__(self, user_id):
        self.UserId = user_id


class EmployeeRequest(db.Model):
    __tablename__ = 'EmployeeRequest'
    id = db.Column(db.Integer, primary_key=True)
    EntityId = db.Column(db.Integer)
    LastName = db.Column(db.String(100), nullable=False)
    MiddleName = db.Column(db.String(100), nullable=True)
    FirstName = db.Column(db.String(100), nullable=False)
    Birthday = db.Column(db.DATETIME, nullable=False)
    EmploymentDate = db.Column(db.DATETIME, nullable=False)
    CreateDate = db.Column(db.DateTime())
    UpdateDate = db.Column(db.DateTime())
    DepartmentId = db.Column(db.Integer)
    Operation = db.Column(db.String(100), nullable=False)
    OperationDate = db.Column(db.DateTime(), default=datetime.now)
    RequestId = db.Column(db.Integer, db.ForeignKey('EntityRequest.id'))
    Request = db.relationship('EntityRequest', foreign_keys='EmployeeRequest.RequestId')

    def get_entity(self, employee):
        self.EntityId = employee.EmployeeId
        self.LastName = employee.LastName
        self.MiddleName = employee.MiddleName
        self.FirstName = employee.FirstName
        self.Birthday = employee.Birthday
        self.EmploymentDate = employee.EmploymentDate
        self.CreateDate = employee.CreateDate
        self.UpdateDate = employee.UpdateDate
        self.DepartmentId = employee.DepartmentId


class DepartmentRequest(db.Model):
    __tablename__ = 'DepartmentRequest'
    id = db.Column(db.Integer, primary_key=True)
    EntityId = db.Column(db.Integer)
    DepartmentName = db.Column(db.String(500), nullable=False)
    CreateDate = db.Column(db.DateTime())
    UpdateDate = db.Column(db.DateTime())
    Operation = db.Column(db.String(100), nullable=False)
    OperationDate = db.Column(db.DateTime(), default=datetime.now)
    RequestId = db.Column(db.Integer, db.ForeignKey('EntityRequest.id'))
    Request = db.relationship('EntityRequest', foreign_keys='DepartmentRequest.RequestId')

    def get_entity(self, department):
        self.EntityId = department.DepartmentId
        self.DepartmentName = department.DepartmentName
