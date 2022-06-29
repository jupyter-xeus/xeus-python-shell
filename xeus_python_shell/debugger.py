import re

from IPython.core.getipython import get_ipython

# This import is required to have the next ones working...
from debugpy.server import api  # noqa
from _pydevd_bundle import pydevd_frame_utils
from _pydevd_bundle.pydevd_suspended_frames import (
    SuspendedFramesManager,
    _FramesTracker,
)


class _FakeCode:
    def __init__(self, co_filename, co_name):
        self.co_filename = co_filename
        self.co_name = co_name


class _FakeFrame:
    def __init__(self, f_code, f_globals, f_locals):
        self.f_code = f_code
        self.f_globals = f_globals
        self.f_locals = f_locals
        self.f_back = None


class _DummyPyDB:
    def __init__(self):
        from _pydevd_bundle.pydevd_api import PyDevdAPI

        self.variable_presentation = PyDevdAPI.VariablePresentation()


class VariableExplorer:
    def __init__(self):
        self.suspended_frame_manager = SuspendedFramesManager()
        self.py_db = _DummyPyDB()
        self.tracker = _FramesTracker(self.suspended_frame_manager, self.py_db)
        self.frame = None

    def track(self):
        ip = get_ipython()
        var = ip.user_ns
        self.frame = _FakeFrame(
            _FakeCode("<module>", ip.compile.get_filename("sys._getframe()")), var, var
        )
        self.tracker.track(
            "thread1", pydevd_frame_utils.create_frames_list_from_frame(self.frame)
        )

    def untrack_all(self):
        self.tracker.untrack_all()

    def get_children_variables(self, variable_ref=None):
        var_ref = variable_ref
        if not var_ref:
            var_ref = id(self.frame)
        variables = self.suspended_frame_manager.get_variable(var_ref)
        return [x.get_var_data() for x in variables.get_children_variables()]


class XDebugger:
    def __init__(self):
        self.variable_explorer = VariableExplorer()

    def _accept_variable(self, variable_name):
        forbid_list = [
            "__name__",
            "__doc__",
            "__package__",
            "__loader__",
            "__spec__",
            "__annotations__",
            "__builtins__",
            "__builtin__",
            "__display__",
            "get_ipython",
            "debugpy",
            "exit",
            "quit",
            "In",
            "Out",
            "_oh",
            "_dh",
            "_",
            "__",
            "___",
        ]
        cond = variable_name not in forbid_list
        cond = cond and not bool(re.search(r"^_\d", variable_name))
        cond = cond and variable_name[0:2] != "_i"
        return cond

    def build_variables_response(self, request, variables):
        var_list = [var for var in variables if self._accept_variable(var["name"])]
        reply = {
            "seq": request["seq"],
            "type": "response",
            "request_seq": request["seq"],
            "success": True,
            "command": request["command"],
            "body": {"variables": var_list},
        }
        return reply

    def inspect_variables(self, message):
        self.variable_explorer.untrack_all()
        # looks like the implementation of untrack_all in ptvsd
        # destroys objects we nee din track. We have no choice but
        # reinstantiate the object
        self.variable_explorer = VariableExplorer()
        self.variable_explorer.track()
        variables = self.variable_explorer.get_children_variables()
        return self.build_variables_response(message, variables)

    def variables(self, message):
        # This intentionnaly handles only the case where the code
        # did not hit a breakpoint
        variables = self.variable_explorer.get_children_variables(
            message["arguments"]["variablesReference"]
        )
        return self.build_variables_response(message, variables)
