class SimpleException(Exception):
    """
    业务异常信息
    """

    def __init__(self, readable_message, code=1, extra_data=None):
        super(SimpleException, self).__init__(readable_message)
        self.code = code
        self.readable_message = readable_message
        self.extra_data = extra_data

    def __repr__(self):
        return self.readable_message

    def __str__(self):
        return self.__repr__()
