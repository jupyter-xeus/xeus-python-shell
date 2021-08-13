from IPython.core.compilerop import CachingCompiler


def default_get_filename(raw_code):
    return '<string>'


class XCachingCompiler(CachingCompiler):
    get_filename = default_get_filename

    def __init__(self, *args, **kwargs):
        super(XCachingCompiler, self).__init__(*args, **kwargs)

        self.filename_mapper = None

    def get_code_name(self, raw_code, code, number):
        filename = XCachingCompiler.get_filename(raw_code)

        if self.filename_mapper is not None:
            self.filename_mapper(filename, number)

        return filename

    @classmethod
    def set_filename_getter(cls, get_filename):
        cls.get_filename = get_filename
