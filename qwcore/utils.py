import click
import logging
import os
import sys
import pkg_resources
import subprocess
import textwrap

from qwcore.exceptions import (PluginNameNotFound, NoPluginsFound,
                               DuplicatePlugin, PluginNameMismatch,
                               PluginNoNameAttribute)

COLOR_LOG = dict(color=True)

try:
    import colorama
except Exception:
    colorama = None


class ColoredStreamHandler(logging.StreamHandler):

    def __init__(self, stream=None):
        logging.StreamHandler.__init__(self, stream)

        self.colors = [
            (logging.ERROR, colorama.Fore.RED),
            (logging.WARNING, colorama.Fore.YELLOW),
            (logging.INFO, colorama.Fore.GREEN)
        ]

    def should_color(self):
        if not colorama:
            return False
        if hasattr(self.stream, "isatty") and self.stream.isatty():
            return True
        if os.environ.get("TERM") == "ANSI":
            return True
        return False

    def format(self, record):
        msg = logging.StreamHandler.format(self, record)
        if hasattr(record, 'color') and record.color and self.should_color():
            for level, color in self.colors:
                if record.levelno >= level:
                    msg = "".join([color] + [msg, colorama.Fore.RESET])
                    break
        return msg


def run(cmd, logger, cwd=None, env=None):
    """Run a subprocess"""

    environ = os.environ.copy()
    if env:
        environ.update(env)

    proc = subprocess.Popen(cmd,
                            stderr=subprocess.STDOUT,
                            stdout=subprocess.PIPE,
                            cwd=cwd,
                            env=env)

    # real time logging unless the subprocess itself is buffering
    # http://stackoverflow.com/a/17698359
    for line in iter(proc.stdout.readline, b''):
        logger.info(line.rstrip())
    proc.communicate()


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


def configure_logging(namespace, log_format='%(message)s', log_level='INFO', color=False):
    """Setup logging"""
    logger = logging.getLogger(namespace)
    formatter = logging.Formatter(log_format)
    if color:
        handler = ColoredStreamHandler(sys.stdout)
    else:
        handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.setLevel(getattr(logging, log_level))
    logger.addHandler(handler)


def build_command(name, description, version, command_group):
    """Build a command to instantiate and run"""

    subcommands = get_plugins(command_group)

    def version(ctx, param, value):
        if value:
            click.echo(version)
            ctx.exit()

    def debug(ctx, param, value):
        if value:
            log = logging.getLogger(name)
            log.setLevel(getattr(logging, 'DEBUG'))

    version_flag = click.Option(['--version'], is_flag=True, expose_value=False,
                                callback=version, is_eager=True, help='Show the version and exit.')
    debug_flag = click.Option(['--debug'], is_flag=True, callback=debug,
                              expose_value=False, help='Turn on debug logging.')

    description = "{description}".format(description=description)
    command = click.Group(command_group, help=description, params=[version_flag, debug_flag])
    for plugin_name, cls in subcommands.iteritems():
        subcommand = click.Command(
            cls.name,
            short_help=cls.help,
            help=textwrap.dedent(' '*4 + cls.__doc__),
            params=cls.params,
            callback=cls().run
        )
        command.add_command(subcommand)

    return command
