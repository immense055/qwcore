from pretend import stub
import pytest

from qwcore import config, exception


def test_get_config_not_found():
    with pytest.raises(exception.ConfigFileNotFoundError):
        config.get_config('BOGUS')


def test_get_config_parse_error(tmpdir, monkeypatch):
    app_config_dir = tmpdir.mkdir('config')
    app_config_dir.join('config').write('bad content')
    monkeypatch.setattr('qwcore.config.AppDirs', lambda name: stub(user_config_dir=str(app_config_dir)))
    with pytest.raises(exception.ConfigFileParserError):
        config.get_config('app')


def test_get_config(tmpdir, monkeypatch):
    app_config_dir = tmpdir.mkdir('config')
    app_config_dir.join('config').write('key = value')
    monkeypatch.setattr('qwcore.config.AppDirs', lambda name: stub(user_config_dir=str(app_config_dir)))
    assert config.get_config('app').get('key') == 'value'


def test_get_key_config_not_found(monkeypatch):
    def get_config(appname):
        raise exception.ConfigFileNotFoundError()
    monkeypatch.setattr('qwcore.config.get_config', get_config)
    with pytest.raises(exception.ConfigFileNotFoundError):
        config.get_value('app', 'key')


def test_get_key_config_not_found_default(monkeypatch):
    def get_config(appname):
        raise exception.ConfigFileNotFoundError()
    monkeypatch.setattr('qwcore.config.get_config', get_config)
    config.get_value('app', 'key', default='default') == 'default'


def test_get_key_section_not_found(monkeypatch):
    def get_config(appname):
        return {}
    monkeypatch.setattr('qwcore.config.get_config', get_config)
    with pytest.raises(exception.ConfigFileSectionNotFoundError):
        config.get_value('app', 'key', section='section')


def test_get_key_section_not_found_default(monkeypatch):
    def get_config(appname):
        return {}
    monkeypatch.setattr('qwcore.config.get_config', get_config)
    config.get_value('app', 'key', section='section', default='default') == 'default'


def test_get_key_key_not_found(monkeypatch):
    def get_config(appname):
        return {'section': {}}
    monkeypatch.setattr('qwcore.config.get_config', get_config)
    with pytest.raises(exception.ConfigFileKeyNotFoundError):
        config.get_value('app', 'key', section='section')


def test_get_key_key_not_found_default(monkeypatch):
    def get_config(appname):
        return {'section': {}}
    monkeypatch.setattr('qwcore.config.get_config', get_config)
    config.get_value('app', 'key', section='section', default='default') == 'default'


def test_get_key_success(monkeypatch):
    def get_config(appname):
        return {'section': {'key': 'value'}}
    monkeypatch.setattr('qwcore.config.get_config', get_config)
    config.get_value('app', 'key', section='section', default='default') == 'value'
