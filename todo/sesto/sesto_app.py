from flask import Flask


class Sesto(Flask):

    def __init__(self, import_name, static_path=None, static_url_path=None,
                 static_folder='static', template_folder='templates',
                 instance_path=None, instance_relative_config=False,
                 blueprints_modules=()):

        super().__init__(import_name, static_path, static_url_path,
                         static_folder, template_folder, instance_path,
                         instance_relative_config)

        self.setting_modules(blueprints_modules)
        self.logger_setting()

    def setting_modules(self, modules):
        """ register Blueprint modules"""
        for module, url_prefix in modules:
            self.register_blueprint(module, url_prefix=url_prefix)

    def logger_setting(self):
        if not self.debug:
            import logging
            from logging import FileHandler, Formatter

            file_handler = FileHandler('log/sesto.log')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'
            ))
            self.logger.addHandler(file_handler)

    def register_api(self, view, endpoint, url, pk='id', pk_type='int'):
        view_func = view.as_view(endpoint)

        self.add_url_rule(url, defaults={pk: None}, view_func=view_func,
                          methods=['GET', ])
        self.add_url_rule(url, view_func=view_func, methods=['POST', ])
        self.add_url_rule(
            '%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
            methods=['GET', 'PUT', 'DELETE'])
