
class ConfigBaseException(Exception):
    pass


class ConfigException(ConfigBaseException):
    section = None
    configuration_id = None

    def __init__(self, message, section, configuration_id):
        self.message = message
        self.section = section
        self.configuration_id = configuration_id
        super(ConfigException, self).__init__(message)


class ConfigDecryptException(ConfigException):
    pass


class ConfigValidationException(ConfigException):
    pass
