"""Utility functions for when xeus-python is embedded in JupyterLite"""
import sys
import time
import types

import xeus_python_shell.lite_webbrowser


def mock_time_sleep():
    def sleep(seconds):
        """Delay execution for a given number of seconds.  The argument may be
        a floating point number for subsecond precision.
        """
        start = now = time.time()
        while now - start < seconds:
            now = time.time()

    time.sleep = sleep


def mock_fcntl():
    sys.modules["fcntl"] = types.ModuleType("fcntl")


def mock_pexpect():
    pexpect_mock = types.ModuleType("pexpect")
    sys.modules["pexpect"] = pexpect_mock


def mock_resource():
    sys.modules["resource"] = types.ModuleType("resource")


def mock_termios():
    termios_mock = types.ModuleType("termios")
    termios_mock.TCSAFLUSH = 2

    sys.modules["termios"] = termios_mock


def mock_tornado():
    """This is needed for some Matplotlib backends (webagg, ipympl) and plotly"""

    # Appease plotly -> tenacity -> tornado.gen usage
    gen = sys.modules["tornado.gen"] = types.ModuleType("gen")
    gen.coroutine = lambda *args, **kwargs: args[0]
    gen.sleep = lambda *args, **kwargs: None
    gen.is_coroutine_function = lambda *args: False

    tornado = sys.modules["tornado"] = types.ModuleType("tornado")
    tornado.gen = gen


def mock_webbrowser():
    sys.modules["webbrowser"] = xeus_python_shell.lite_webbrowser


ALL_MOCKS = [
    mock_time_sleep,
    mock_fcntl,
    mock_pexpect,
    mock_resource,
    mock_termios,
    mock_tornado,
    mock_webbrowser,
]


def apply_mocks():
    """Apply all of the mocks needed for mainstream packages to work, if possible"""
    import warnings

    for mock in ALL_MOCKS:
        try:
            mock()
        except Exception as err:
            warnings.warn("failed to apply mock", mock, err)
