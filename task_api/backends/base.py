from importlib import import_module


class TaskBackend(object):
    def resolve_class(self, class_str):
        try:
            module_name, class_name = class_str.rsplit('.', 1)
            module = import_module(module_name)
            cls = getattr(module, class_name)
        except (ImportError, ValueError, AttributeError):
            raise ImportError('Cannot load class: ' + class_str)
        return cls

    def run_task(self, info, class_str):
        raise NotImplemented
