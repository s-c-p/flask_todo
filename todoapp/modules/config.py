class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
