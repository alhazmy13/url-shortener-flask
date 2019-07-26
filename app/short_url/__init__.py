def init_app(app, **kwargs):
    from app.short_url import route  # pylint: disable=unused-variable
    app.register_blueprint(route.api)
