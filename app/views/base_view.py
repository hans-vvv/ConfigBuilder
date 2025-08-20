from app.printers import write_configs

class BaseView: # inject common dependencies
    def __init__(self, write_configs, *args, **kwargs):
        self.write_configs = write_configs

