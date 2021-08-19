import sys

from IPython.core.displaypub import DisplayPublisher
from IPython.core.displayhook import DisplayHook


class XDisplayPublisher(DisplayPublisher):
    def __init__(self, shell=None, *args, **kwargs):
        super(XDisplayPublisher, self).__init__(shell, *args, **kwargs)

        self.publish_display_data = None
        self.clear_output = None

    def publish(
            self, data, metadata=None, source=None, *,
            transient=None, update=False, **kwargs
            ) -> None:
        if self.publish_display_data is not None:
            self.publish_display_data(data, metadata, transient, update)


class XDisplayHook(DisplayHook):
    def __init__(self, *args, **kwargs):
        super(XDisplayHook, self).__init__(*args, **kwargs)

        self.publish_execution_result = None

    def start_displayhook(self):
        self.data = {}
        self.metadata = {}

    def write_output_prompt(self):
        pass

    def write_format_data(self, format_dict, md_dict=None):
        self.data = format_dict
        self.metadata = md_dict

    def finish_displayhook(self):
        sys.stdout.flush()
        sys.stderr.flush()

        if self.publish_execution_result is not None:
            self.publish_execution_result(
                self.prompt_count, self.data, self.metadata
            )

        self.data = {}
        self.metadata = {}
