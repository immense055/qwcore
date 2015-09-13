
class QwcoreException(Exception):
    """Qwcore base exception"""


class PluginNameNotFoundError(QwcoreException):
    """Raised when a specific plugin is not found"""


class PluginNameMismatchError(QwcoreException):
    """Raised when a plugin name does not match the 'name' attribute of the object"""


class DuplicatePluginError(QwcoreException):
    """Raised when a specific name has multiple plugins"""


class NoPluginsFoundError(QwcoreException):
    """Raised when no template plugins are found"""


class PluginNoNameAttributeError(QwcoreException):
    """Raised when a plugin has no 'name' attribute"""


class ConfigFileNotFoundError(QwcoreException):
    """Raised when the config file for an app is not found"""


class ConfigFileParserError(QwcoreException):
    """Raised when the config file can't be parsed"""


class ConfigFileKeyError(QwcoreException):
    """Raised when a key can't be found"""
