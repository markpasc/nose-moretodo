from nose.plugins.errorclass import ErrorClass, ErrorClassPlugin
from nose.tools import make_decorator


class Todo(Exception):

    """The `Exception` raised when a to-do test fails as expected.

    These results are not counted as errors in the test suite results.

    """

    pass


class MoreTodo(ErrorClassPlugin):

    """A nose plugin adding "to-do" tests in the style of Perl's Test::More.

    There are several nose plugins for adding to-do tests (including the
    `ErrorClassPlugin` example in the nose documentation). Unlike most of them,
    `MoreTodo` also treats the *unexpected success* of a to-do test as a
    failure. That is, tests that are marked to-do *must* fail.

    To use the plugin, mark your to-do tests with the included
    `moretodo.todo()` decorator::

        from moretodo import todo

        class MyTests(unittest.TestCase):

            @todo
            def test_something_broken(self):
                raise NotImplementedError

    When such a test fails by raising any exception (including `AssertionError`
    exceptions from the `TestCase.assert*` methods), it will be counted as a
    non-error ``TODO`` test in the test suite results. If, however, your test
    succeeds, the `todo` decorator will raise a real `AssertionError`, counting
    your test among the suite's failed tests.

    """

    enabled = True
    todo = ErrorClass(Todo, label='TODO', isfailure=False)

    def options(self, parser, env):
        """Configures this nose plugin's options.

        This implementation adds a ``--do-all`` parameter that, when specified,
        disables the to-do plugin. A true value in the environment variable
        ``NOSE_WITHOUT_TODO`` also disables the plugin.

        """
        env_opt = 'NOSE_WITHOUT_TODO'
        parser.add_option('--do-all', action='store_true',
            dest='no_todo', default=env.get(env_opt, False),
            help='Run all to-do tests as normal tests instead. '
            '[NOSE_WITHOUT_TODO]')

    def configure(self, options, conf):
        """Configures this nose plugin per the specified options.

        If the `no_todo` option was specified (either through the ``--do-all``
        command line argument or the ``NOSE_WITHOUT_TODO`` environment
        variable), to-do behavior will be disabled and tests will run normally.

        """
        if not self.can_configure:
            return
        self.conf = conf
        disable = getattr(options, 'no_todo', False)
        if disable:
            # Set it on the class, so our class method will know.
            type(self).enabled = False

    @classmethod
    def run_test(cls, fn, args, kwargs):
        """Runs the given test `fn` with the given positional and keyword
        arguments.

        If to-do tests are enabled, failures will be transmuted into
        expected-failure successes, while real successes will become
        unexpected-success failures.

        """
        if not cls.enabled:
            return fn(*args, **kwargs)

        try:
            fn(*args, **kwargs)
        except Exception, exc:
            raise Todo('Caught expected failure %s: %s' % (type(exc).__name__, str(exc)))
        else:
            raise AssertionError('Test unexpectedly passed')


def todo(fn):
    """Marks a test as a to-do test.

    To-do tests are expected to fail. If a test marked with this decorator
    fails, it will be marked as an expected failure in the test results;
    contrariwise, if the test succeeds, it will be reported as a fatal
    "unexpected success" failure.

    """
    @make_decorator(fn)
    def run_test(*args, **kwargs):
        return MoreTodo.run_test(fn, args, kwargs)
    return run_test

