from marshmallow import Schema, fields


class DepartmentSchema(Schema):
    DepartmentId = fields.Integer()
    DepartmentName = fields.String()


class EmployeeSchema(Schema):
    EmployeeId = fields.Integer()
    LastName = fields.String()
    MiddleName = fields.String()
    FirstName = fields.String()
    Birthday = fields.DateTime()
    EmploymentDate = fields.DateTime()
    Department = fields.Nested(DepartmentSchema, required=True)


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    password_hash = fields.String()
    created_on = fields.DateTime()
    updated_on = fields.DateTime()
