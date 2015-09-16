
class QwcoreError(Exception):
    """Qwcore base exception"""


class PluginNameNotFoundError(QwcoreError):
    """Raised when a specific plugin is not found"""


class PluginNameMismatchError(QwcoreError):
    """Raised when a plugin name does not match the 'name' attribute of the object"""


class DuplicatePluginError(QwcoreError):
    """Raised when a specific name has multiple plugins"""


class NoPluginsFoundError(QwcoreError):
    """Raised when no template plugins are found"""


class PluginNoNameAttributeError(QwcoreError):
    """Raised when a plugin has no 'name' attribute"""


class ConfigFileNotFoundError(QwcoreError):
    """Raised when the config file for an app is not found"""


class ConfigFileParserError(QwcoreError):
    """Raised when the config file can't be parsed"""
