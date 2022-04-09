class Config(object):
    """Базовый конфиг"""
    DB_SERVER = '192.168.1.34'
    USERNAME = 'YAKOV'
    PASSWORD = 'Passw0rd!'
    DB_NAME = 'flask-database'
    SECRET_KEY = 'My Secret Key'
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"mssql+pymssql://{self.USERNAME}:{self.PASSWORD}@{self.DB_SERVER}/{self.DB_NAME}"


class ProductionConfig(Config):
    """Переменные, используемые в продакшене"""
    DB_SERVER = '192.168.1.34'


class DevelopmentConfig(Config):
    """Переменные, используемые при разработке"""
    DB_SERVER = 'db'
