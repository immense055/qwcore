
import click
import pkg_resources
from mock import Mock, call
import pytest

from qwcore.utils import get_plugins, build_command
from qwcore.exceptions import (PluginNameNotFound, NoPluginsFound,
                               DuplicatePlugin, PluginNameMismatch,
                               PluginNoNameAttribute)


class PluginClass(object):
    name = 'testname'


class PluginClassMismatch(object):
    name = 'mismatch'


class PluginClassNoName(object):
    pass


class TestLoadPlugins(object):

    def patch_iter_ep(self, monkeypatch, ext_class, no_ep=False, dupe=False):
        dist = pkg_resources.get_distribution('qwcore')
        if no_ep:
            def iter_entry_points(group, name=None):
                return iter([])
        else:
            ep = pkg_resources.EntryPoint.parse("testname = qwcore.tests.test_utils:%s" % ext_class, dist=dist)
            ep.load()

            def iter_entry_points(group, name=None):
                yield ep
                if dupe:
                    yield ep
        monkeypatch.setattr('qwcore.utils.pkg_resources.iter_entry_points', iter_entry_points)

    def test_load_success(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClass')
        exts = get_plugins('foo', name='testname')
        assert len(exts) == 1
        assert 'testname' in exts

    def test_load_mismatch(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClassMismatch')
        with pytest.raises(PluginNameMismatch):
            get_plugins('foo', name='testname')

    def test_load_no_name_attr(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClassNoName')
        with pytest.raises(PluginNoNameAttribute):
            get_plugins('foo', name='testname')

    def test_load_name_not_found(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClass', no_ep=True)
        with pytest.raises(PluginNameNotFound):
            get_plugins('foo', name='testname')

    def test_load_duplicates(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClass', dupe=True)
        with pytest.raises(DuplicatePlugin):
            get_plugins('foo', name='testname')

    def test_load_no_plugins(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClass', no_ep=True)
        with pytest.raises(NoPluginsFound):
            get_plugins('foo')


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

    monkeypatch.setattr('qwcore.utils.get_plugins', get_plugins)

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
