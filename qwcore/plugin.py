import pkg_resources

from qwcore.exceptions import (PluginNameNotFound, NoPluginsFound,
                               DuplicatePlugin, PluginNameMismatch,
                               PluginNoNameAttribute)


def get_plugins(group, name=None):
    """Given a plugin group and name, return a dict of plugin classes by name"""
    plugins = {}
    for entry_point in pkg_resources.iter_entry_points(group, name=name):
        plugin = entry_point.load()
        if hasattr(plugin, 'name') and entry_point.name != plugin.name:
            raise PluginNameMismatch(
                "name %s does not match plugin name %s" % (entry_point.name, plugin.name))
        elif not hasattr(plugin, 'name'):
            raise PluginNoNameAttribute(
                "plugin %s has no 'name' attribute" % (entry_point.name))
        if plugin.name in plugins:
            raise DuplicatePlugin("duplicate plugin %s found" % name)
        plugins[plugin.name] = plugin
    if name and not plugins:
        raise PluginNameNotFound("no %s template found with name %s" % (group, name))
    elif not plugins:
        raise NoPluginsFound("no %s plugins found" % group)
    return plugins
