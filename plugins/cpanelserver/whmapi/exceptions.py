
class WHMException(Exception):
    pass


class WHMCredentialsRequired(WHMException):
    pass


class WHMCredentialsInvalid(WHMException):
    pass


class WHMAPIException(WHMException):
    pass
