
class PluginNameNotFoundError(Exception):
    """Raised when a specific plugin is not found"""


class PluginNameMismatchError(Exception):
    """Raised when a plugin name does not match the 'name' attribute of the object"""


class DuplicatePluginError(Exception):
    """Raised when a specific name has multiple plugins"""


class NoPluginsFoundError(Exception):
    """Raised when no template plugins are found"""


class PluginNoNameAttributeError(Exception):
    """Raised when a plugin has no 'name' attribute"""
