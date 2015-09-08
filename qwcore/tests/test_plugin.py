
import pkg_resources
import pytest

from qwcore.plugin import get_plugins
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
            ep = pkg_resources.EntryPoint.parse("testname = qwcore.tests.test_plugin:%s" % ext_class, dist=dist)
            ep.load()

            def iter_entry_points(group, name=None):
                yield ep
                if dupe:
                    yield ep
        monkeypatch.setattr('qwcore.plugin.pkg_resources.iter_entry_points', iter_entry_points)

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
