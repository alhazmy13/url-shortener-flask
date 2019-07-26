class BaseConfig(object):
    SECRET_KEY = 'this-really-needs-to-be-changed'

    SITE_URL = 'http://alhazmy13.net/'
    KEY_LENGTH = 8

    REDIS_URL = 'redis://127.0.0.1:6379'
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass
