import click
from mock import Mock, call

from qwcore.cli import build_command


def test_build_command(monkeypatch):

    yo_option = click.Option(['--yo'], is_flag=True,  help='Yo')

    class Cmd1:
        """Cmd1 doc"""
        name = 'Cmd1'
        help = 'help'
        params = [yo_option]

    Cmd1.run = Mock()

    class Cmd2():
        """Cmd2 doc"""
        name = 'Cmd2'
        help = 'help'
        params = []

    Cmd2.run = Mock()

    subcommands = {'Cmd1': Cmd1, 'Cmd2': Cmd2}

    def get_plugins(group, name=None):
        return subcommands

    monkeypatch.setattr('qwcore.cli.get_plugins', get_plugins)

    cmd = build_command('testname', 'description', '1.0', 'group')
    ctx = click.Context(click.Group)
    assert sorted(cmd.commands.keys()) == ['Cmd1', 'Cmd2']
    assert 'Cmd1 doc' in cmd.commands['Cmd1'].get_help(ctx)
    assert 'Cmd2 doc' in cmd.commands['Cmd2'].get_help(ctx)
    assert 'Cmd1  help' in cmd.get_help(ctx)
    assert 'Cmd2  help' in cmd.get_help(ctx)
    assert cmd.commands['Cmd1'].params == [yo_option]
    assert cmd.commands['Cmd2'].params == []
    try:
        cmd.main(['Cmd1'])
    except SystemExit:
        pass
    assert Cmd1.run.mock_calls == [call(yo=False)]
    assert Cmd2.run.mock_calls == []
