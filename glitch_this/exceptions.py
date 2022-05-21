class BaseCustomException(Exception):
    pass


class WrongImageFormatException(BaseCustomException):
    pass


class ValidGIFNotFoundException(BaseCustomException):
    pass


class BaseCLICustomException(Exception):
    pass


class OutFileNotFoundException(BaseCLICustomException):
    pass


class CanNotOverwriteUntilForceIsProvided(BaseCLICustomException):
    pass
