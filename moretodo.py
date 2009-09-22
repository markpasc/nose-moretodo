from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin
from nose.tools import make_decorator


class Todo(Exception):
    pass


class MoreTodo(ErrorClassPlugin):

    enabled = True
    todo = ErrorClass(Todo, label='TODO', isfailure=False)

    def options(self, parser, env):
        env_opt = 'NOSE_WITHOUT_TODO'
        parser.add_option('--do-all', action='store_true',
            dest='no_todo', default=env.get(env_opt, False),
            help='Run all to-do tests as normal tests instead. '
            '[NOSE_WITHOUT_TODO]')

    def configure(self, options, conf):
        if not self.can_configure:
            return
        self.conf = conf
        disable = getattr(options, 'no_todo', False)
        if disable:
            # Set it on the class, so our class method will know.
            type(self).enabled = False

    @classmethod
    def run_test(cls, fn, args, kwargs):
        if not cls.enabled:
            return fn(*args, **kwargs)

        try:
            fn(*args, **kwargs)
        except Exception, exc:
            raise Todo('Caught expected failure %s: %s' % (type(exc).__name__, str(exc)))
        else:
            raise AssertionError('Test unexpectedly passed')


def todo(fn):
    @make_decorator(fn)
    def run_test(*args, **kwargs):
        return MoreTodo.run_test(fn, args, kwargs)
    return run_test
