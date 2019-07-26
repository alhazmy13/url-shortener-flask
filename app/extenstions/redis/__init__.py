import os

try:
    from urlparse import urlsplit
except ImportError:
    from urllib.parse import urlsplit

from redis import Redis


def parse_url(url):
    """Parses the supplied Redis URL and returns a dict with the parsed/split data.
    For ambiguous URLs like redis://localhost and redis://my_socket_file
    """
    # Parse URL, make sure string is valid.
    try:
        split = urlsplit(url.rstrip('/'))
    except (AttributeError, TypeError) as e:
        raise ValueError('Malformed URL specified: {0}'.format(e))
    if split.scheme not in ['redis+socket', 'redis', 'file']:
        raise ValueError('Malformed URL specified.')
    scheme = split.scheme
    netloc = split.netloc
    hostname = split.hostname
    path = split.path
    password = split.password
    try:
        port = split.port
    except ValueError:
        port = None  # Stupid urlsplit bug on Windows.

    # Handle non-socket URLs.
    if scheme == 'redis' and netloc and not netloc.endswith('.') and not netloc.endswith('@'):
        result = dict(host=hostname)
        if password:
            result['password'] = password
        if port:
            result['port'] = port
        if path:
            if not path[1:].isdigit():
                raise ValueError('Network URL path has non-digit characters: {0}'.format(path[1:]))
            result['db'] = int(path[1:])
        return result

    # Handle socket URLs.
    if port:
        raise ValueError('Socket URL looks like non-socket URL.')
    if not password:
        socket_path = '{0}{1}'.format(netloc, path)
    elif netloc.endswith('.'):
        socket_path = '{0}{1}'.format(netloc.split('@')[1], path)
    elif not path:
        socket_path = netloc.split('@')[1]
    else:
        socket_path = path

    # Catch bad paths.
    parent_dir = os.path.split(socket_path)[0]
    if parent_dir and not os.path.isdir(parent_dir):
        raise ValueError("Unix socket path's parent not a dir: {0}".format(parent_dir))

    # Finish up.
    result = dict(unix_socket_path=socket_path)
    if password:
        result['password'] = password
    return result


def read_config(config, prefix):
    """Return a StrictRedis.__init__() compatible dictionary from data in the Flask config.
    """
    # Get all relevant config values from Flask application.
    suffixes = ('URL', 'SOCKET', 'HOST', 'PORT', 'PASSWORD', 'DB')
    config_url, config_socket, config_host, config_port, config_password, config_db = [
        config.get('{0}_{1}'.format(prefix, suffix)) for suffix in suffixes
    ]
    result = dict()
    # Get more values from URL if provided.
    if config_url:
        result.update(parse_url(config_url))
    # Apply other config values.
    if config_socket:
        result['unix_socket_path'] = config_socket
    else:
        if config_host:
            result['host'] = config_host
        if config_port is not None:
            result['port'] = int(config_port)
    if config_password is not None:
        result['password'] = config_password
    if config_db is not None:
        result['db'] = int(config_db)

    result['charset'] = 'utf-8'
    # result['decode_responses'] = True
    return result


class FlaskRedis(Redis):

    def __init__(self, app=None, config_prefix=None):
        super(FlaskRedis, self).__init__()
        if app is not None:
            self.init_app(app, config_prefix)

    def init_app(self, app, config_prefix=None):
        # Normalize the prefix and add this instance to app.extensions.
        config_prefix = (config_prefix or 'REDIS').rstrip('_').upper()
        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        if config_prefix.lower() in app.extensions:
            raise ValueError('Already registered config prefix {0!r}.'.format(config_prefix))

        # Read config.
        args = read_config(app.config, config_prefix)

        # Instantiate StrictRedis.
        super(FlaskRedis, self).__init__(**args)  # Initialize fully.
