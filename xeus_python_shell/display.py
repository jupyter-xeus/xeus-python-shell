import sys

from IPython.core.displaypub import DisplayPublisher
from IPython.core.displayhook import DisplayHook


class XDisplayPublisher(DisplayPublisher):
    def publish(
            self, data, metadata=None, source=None, *,
            transient=None, update=False, **kwargs
            ) -> None:
        publish_display_data(data, metadata, transient, update)

    def clear_output(self, wait=False):
        clear_output(wait)


class XDisplayHook(DisplayHook):
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

        publish_execution_result(self.prompt_count, self.data, self.metadata)

        self.data = {}
        self.metadata = {}
