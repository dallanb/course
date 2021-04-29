from functools import wraps

from src.notifications import course_created, course_approved


class course_notification:
    def __init__(self, operation):
        self.operation = operation

    def __call__(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            prev_instance = {**kwargs.get('instance').__dict__} if kwargs.get('instance') else None
            new_instance = f(*args, **kwargs)

            if self.operation == 'create':
                self.create(new_instance=new_instance)
            if self.operation == 'update':
                self.update(prev_instance=prev_instance, new_instance=new_instance, args=kwargs)

            return new_instance

        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        return wrap

    @staticmethod
    def create(new_instance):
        course_created.from_data(course=new_instance).notify()

    @staticmethod
    def update(prev_instance, new_instance, args):
        if prev_instance and prev_instance.get('status') and prev_instance['status'].name == 'pending' \
                and new_instance.status.name == 'active':
            course_approved.from_data(course=new_instance).notify()
