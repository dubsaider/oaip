class AbstractHandler:
    def __init__(self, parser=None, type_parser=None):
        self.parser = parser(type_parser)

    def __call__(self, *args, **kwds):
        pass

    