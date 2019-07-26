import os

from flask import Flask

CONFIG_NAME_MAPPER = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig'
}


def create_app(flask_config_name=None, **kwargs):
    import threading
    threading.stack_size(2 * 1024 * 1024)

    flask_app = Flask(__name__, **kwargs)
    flask_app.url_map.strict_slashes = False
    env_flask_config_name = os.getenv('FLASK_CONFIG')
    if not env_flask_config_name and flask_config_name is None:
        flask_config_name = 'development'
    elif flask_config_name is None:
        flask_config_name = env_flask_config_name
    else:
        if env_flask_config_name:
            assert env_flask_config_name == flask_config_name, (
                    "FLASK_CONFIG environment variable (\"%s\") and flask_config_name argument "
                    "(\"%s\") are both set and are not the same." % (
                        env_flask_config_name,
                        flask_config_name
                    )
            )

    try:
        flask_app.config.from_object(CONFIG_NAME_MAPPER[flask_config_name])
    except ImportError:
        raise

    from app import extenstions
    extenstions.init_app(flask_app)

    from app import short_url
    short_url.init_app(flask_app)

    return flask_app


app = create_app()
