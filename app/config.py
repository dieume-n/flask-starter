import os


class Config(object):
    DEBUG = False
    ENV = "production"
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USER = os.environ.get("DB_USER")
    DB_SERVER = os.environ.get("DB_SERVER")
    DB_NAME = os.environ.get("DB_NAME")

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"mysql+pymysql://{self.DB_USER}@{self.DB_SERVER}/{self.DB_NAME}"  # pragma: no cover

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    RESET_PASSWORD_TOKEN_EXPIRY = os.environ.get("RESET_PASSWORD_TOKEN_EXPIRY", 3600)


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///app-dev.sqlite3"
    SECRET_KEY = os.environ.get("SECRET_KEY", "mysupersecretkey")
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PROFILER_ENABLED = True

    # Flask-Mail
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.mailtrap.io")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEBUG = True


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///app-test.sqlite3"
    SECRET_KEY = os.environ.get("SECRET_KEY", "mysupersecretkey")


class ProdConfig(Config):
    pass


configurations = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
