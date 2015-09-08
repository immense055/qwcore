import pkg_resources

from qwcore.exceptions import (PluginNameNotFoundError, NoPluginsFoundError,
                               DuplicatePluginError, PluginNameMismatchError,
                               PluginNoNameAttributeError)


def get_plugins(group, name=None):
    """Given a plugin group and name, return a dict of plugin classes by name"""
    plugins = {}
    for entry_point in pkg_resources.iter_entry_points(group, name=name):
        plugin = entry_point.load()
        if hasattr(plugin, 'name') and entry_point.name != plugin.name:
            raise PluginNameMismatchError(
                "name %s does not match plugin name %s" % (entry_point.name, plugin.name))
        elif not hasattr(plugin, 'name'):
            raise PluginNoNameAttributeError(
                "plugin %s has no 'name' attribute" % (entry_point.name))
        if plugin.name in plugins:
            raise DuplicatePluginError("duplicate plugin %s found" % name)
        plugins[plugin.name] = plugin
    if name and not plugins:
        raise PluginNameNotFoundError("no %s template found with name %s" % (group, name))
    elif not plugins:
        raise NoPluginsFoundError("no %s plugins found" % group)
    return plugins
