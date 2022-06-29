from IPython.core.compilerop import CachingCompiler


class XCachingCompiler(CachingCompiler):
    def __init__(self, *args, **kwargs):
        super(XCachingCompiler, self).__init__(*args, **kwargs)

        self.filename_mapper = None
        self.get_filename = None

    def get_code_name(self, raw_code, code, number):
        if self.get_filename is not None:
            filename = self.get_filename(raw_code)
        else:
            filename = "<string>"

        if self.filename_mapper is not None:
            self.filename_mapper(filename, number)

        return filename
