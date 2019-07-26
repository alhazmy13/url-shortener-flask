from app.extenstions.redis import FlaskRedis
from app.extenstions.logging import Logging

redis = FlaskRedis()
logging = Logging()


def init_app(app):
    """
    Application extensions initialization.
    """
    for extension in (
            logging,
            redis,
    ):
        extension.init_app(app)
