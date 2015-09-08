
import pkg_resources
import pytest

from qwcore.plugin import _get_plugins, get_plugins, get_plugin
from qwcore.exceptions import (PluginNameNotFoundError, NoPluginsFoundError,
                               DuplicatePluginError, PluginNameMismatchError,
                               PluginNoNameAttributeError)


class PluginClass(object):
    name = 'testname'


class PluginClassMismatch(object):
    name = 'mismatch'


class PluginClassNoName(object):
    pass


class TestGetPlugins(object):

    def patch_iter_ep(self, monkeypatch, plugin_class, no_ep=False, dupe=False):
        dist = pkg_resources.get_distribution('qwcore')
        if no_ep:
            def iter_entry_points(group, name=None):
                return iter([])
        else:
            ep = pkg_resources.EntryPoint.parse("testname = qwcore.tests.test_plugin:%s" % plugin_class, dist=dist)
            ep.load()

            def iter_entry_points(group, name=None):
                yield ep
                if dupe:
                    yield ep
        monkeypatch.setattr('qwcore.plugin.pkg_resources.iter_entry_points', iter_entry_points)

    def test_get_plugin(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClass')
        p = get_plugin('foo', 'testname')
        assert p.name == 'testname'

    def test_get_plugins(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClass')
        plugins = get_plugins('foo')
        assert len(plugins) == 1
        assert 'testname' in plugins
        assert plugins['testname'].name == 'testname'

    def test_mismatch(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClassMismatch')
        with pytest.raises(PluginNameMismatchError):
            _get_plugins('foo', name='testname')

    def test_no_name_attr(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClassNoName')
        with pytest.raises(PluginNoNameAttributeError):
            _get_plugins('foo', name='testname')

    def test_name_not_found(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClass', no_ep=True)
        with pytest.raises(PluginNameNotFoundError):
            _get_plugins('foo', name='testname')

    def test_duplicates(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClass', dupe=True)
        with pytest.raises(DuplicatePluginError):
            _get_plugins('foo', name='testname')

    def test_no_plugins(self, monkeypatch):
        self.patch_iter_ep(monkeypatch, 'PluginClass', no_ep=True)
        with pytest.raises(NoPluginsFoundError):
            _get_plugins('foo')
