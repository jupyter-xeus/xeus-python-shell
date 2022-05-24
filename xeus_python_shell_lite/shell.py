import time

from IPython.core.history import HistoryManager

from xeus_python_shell import XPythonShell, XPythonShellApp
from xeus_python_shell.compiler import XCachingCompiler
from xeus_python_shell.display import XDisplayPublisher, XDisplayHook


def sleep(seconds):
    """Delay execution for a given number of seconds.  The argument may be
    a floating point number for subsecond precision.
    """
    start = now = time.time()
    while now - start < seconds:
        now = time.time()


class CustomHistoryManager(HistoryManager):

    def __init__(self, shell=None, config=None, **traits):
        self.enabled = False
        super(CustomHistoryManager, self).__init__(shell=shell, config=config, **traits)


class LiteXPythonShell(XPythonShell):

    def init_history(self, *args, **kwargs):
        self.history_manager = CustomHistoryManager(shell=self, parent=self)
        self.configurables.append(self.history_manager)


class LiteXPythonShellApp(XPythonShellApp):

    def init_shell(self):
        # Blocking time.sleep
        # TODO Find another way to do this (using service workers in JupyterLite?)
        time.sleep = sleep

        self.shell = LiteXPythonShell.instance(
            display_pub_class=XDisplayPublisher,
            displayhook_class=XDisplayHook,
            compiler_class=XCachingCompiler,
            user_ns=self.user_ns
        )
