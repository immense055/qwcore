import pkg_resources

from qwcore.exceptions import (PluginNameNotFoundError, NoPluginsFoundError,
                               DuplicatePluginError, PluginNameMismatchError,
                               PluginNoNameAttributeError)


def _get_plugins(group, name=None):
    """Return a dict of plugins by name from a certain group, filtered by name if
    given.

    :param group: plugin group
    :param name: plugin name
    """
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


def get_plugin(group, name):
    """Return a single plugin

    :param group: plugin group
    :param name: plugin name
    """
    return _get_plugins(group, name)[name]


def get_plugins(group):
    """Return a dict of plugins by name from a certain group

    :param group: plugin group
    """
    return _get_plugins(group)
