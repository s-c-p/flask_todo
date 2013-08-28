from flask import Flask
from todo.sesto import log_config


class Sesto(Flask):

    def __init__(self, import_name, static_path=None, static_url_path=None,
                 static_folder='static', template_folder='templates',
                 instance_path=None, instance_relative_config=False,
                 blueprints_modules=()):

        super().__init__(import_name, static_path, static_url_path,
                         static_folder, template_folder, instance_path,
                         instance_relative_config)

        self.setting_modules(blueprints_modules)

    def setting_modules(self, modules):
        """ register Blueprint modules"""
        for module, url_prefix in modules:
            self.register_blueprint(module, url_prefix=url_prefix)

    def init_logger(self):

        self.logger.addHandler(log_config.create_log_file_handler(
                               self.config.get('LOG_PATH')))

    def register_api(self, view, endpoint, url, pk='id', pk_type='int'):
        view_func = view.as_view(endpoint)

        self.add_url_rule(url, defaults={pk: None}, view_func=view_func,
                          methods=['GET', ])
        self.add_url_rule(url, view_func=view_func, methods=['POST', ])
        self.add_url_rule(
            '%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
            methods=['GET', 'PUT', 'DELETE'])
