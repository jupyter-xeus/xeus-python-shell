import sys

from IPython.core.interactiveshell import InteractiveShell
from IPython.core.shellapp import InteractiveShellApp
from IPython.core.application import BaseIPythonApplication
from IPython.core import page, payloadpage
from IPython.core.completer import provisionalcompleter, rectify_completions

from .compiler import XCachingCompiler
from .display import XDisplayPublisher, XDisplayHook


class XPythonShell(InteractiveShell):
    def __init__(self, *args, **kwargs):
        super(XPythonShell, self).__init__(*args, **kwargs)

        self.kernel = None

    def enable_gui(self, gui=None):
        """Not implemented yet."""
        pass

    def init_hooks(self):
        super(XPythonShell, self).init_hooks()
        self.set_hook('show_in_pager', page.as_hook(payloadpage.page), 99)

    # Workaround for preventing IPython to show error traceback
    # in the console, we catch it and will display it later
    def _showtraceback(self, etype, evalue, stb):
        self.last_error = [str(etype), str(evalue), stb]

    def complete_code(self, code, cursor_pos):
        with provisionalcompleter():
            raw_completions = self.Completer.completions(code, cursor_pos)
            completions = list(rectify_completions(code, raw_completions))

            comps = []
            for comp in completions:
                comps.append(dict(
                    start=comp.start,
                    end=comp.end,
                    text=comp.text,
                    type=comp.type,
                ))

        if completions:
            cursor_start = completions[0].start
            cursor_end = completions[0].end
            matches = [c.text for c in completions]
        else:
            cursor_start = cursor_pos
            cursor_end = cursor_pos
            matches = []

        return matches, cursor_start, cursor_end


class XPythonShellApp(BaseIPythonApplication, InteractiveShellApp):
    def initialize(self, argv=None):
        super(XPythonShellApp, self).initialize(argv)

        self.user_ns = {}

        # self.init_io() ?

        self.init_path()
        self.init_shell()

        self.init_extensions()
        self.init_code()

        sys.stdout.flush()
        sys.stderr.flush()

    def init_shell(self):
        self.shell = XPythonShell.instance(
            display_pub_class=XDisplayPublisher,
            displayhook_class=XDisplayHook,
            compiler_class=XCachingCompiler,
            user_ns=self.user_ns
        )

    # Overwrite exit logic, this is not part of the kernel protocol
    def exit(self, exit_status=0):
        pass
