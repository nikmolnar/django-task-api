from task_api.utils import resolve_class


class TaskBackend(object):
    def resolve_class(self, class_str):
        cls = resolve_class(class_str)
        if cls is None:
            raise ImportError('Cannot load class: ' + class_str)
        return cls

    def run_task(self, info, class_str):
        raise NotImplemented
