from IPython.core.history import HistoryManager

from xeus_python_shell import XPythonShell, XPythonShellApp
from xeus_python_shell.compiler import XCachingCompiler
from xeus_python_shell.display import XDisplayPublisher, XDisplayHook


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
        self.shell = LiteXPythonShell.instance(
            display_pub_class=XDisplayPublisher,
            displayhook_class=XDisplayHook,
            compiler_class=XCachingCompiler,
            user_ns=self.user_ns
        )
