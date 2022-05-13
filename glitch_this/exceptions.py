class BaseCustomException(Exception):
    pass


class WrongImageFormatException(BaseCustomException):
    pass


class ValidGIFNotFoundException(BaseCustomException):
    pass
