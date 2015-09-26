import logging
import textwrap

import click
import six

from qwcore.plugin import get_plugins


def build_command(name, description, version, command_group, project_name=None):
    """Build a click command with subcommands

    :param name: command name
    :description: command description
    :version: command version
    :command_group: the entry point group for the subcommand extensions
    """

    if not project_name:
        project_name = name

    subcommands = get_plugins(command_group)

    class MyGroup(click.Group):

        # override to set the project name for the command
        def get_command(self, ctx, cmd_name):
            ctx.meta['qwcore.project_name'] = project_name
            return super(MyGroup, self).get_command(ctx, cmd_name)

    def show_version(ctx, param, value):
        if value:
            click.echo(version)
            ctx.exit()

    def set_debug(ctx, param, value):
        if value:
            log = logging.getLogger(name)
            log.setLevel(getattr(logging, 'DEBUG'))

    version_flag = click.Option(['--version'], is_flag=True, expose_value=False,
                                callback=show_version, is_eager=True, help='Show the version and exit.')
    debug_flag = click.Option(['--debug'], is_flag=True, callback=set_debug,
                              expose_value=False, help='Turn on debug logging.')

    description = "{description}".format(description=description)
    command = MyGroup(command_group, help=description, params=[version_flag, debug_flag])
    for plugin_name, cls in six.iteritems(subcommands):
        subcommand = click.Command(
            cls.name,
            short_help=cls.help,
            help=textwrap.dedent(' '*4 + cls.__doc__),
            params=cls.params,
            callback=cls().run
        )
        command.add_command(subcommand)

    return command
