class PluginNameNotFound(Exception):
    """Raised when a specific plugin is not found"""


class PluginNameMismatch(Exception):
    """Raised when a plugin name does not match the 'name' attribute of the object"""


class DuplicatePlugin(Exception):
    """Raised when a specific name has multiple plugins"""


class NoPluginsFound(Exception):
    """Raised when no template plugins are found"""


class PluginNoNameAttribute(Exception):
    """Raised when a plugin has no 'name' attribute"""
