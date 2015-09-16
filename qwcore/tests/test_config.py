from pretend import stub
import pytest

from qwcore import config, exceptions


def test_get_config_not_found():
    with pytest.raises(exceptions.ConfigFileNotFoundError):
        config.get_config('BOGUS')


def test_get_config_parse_error(tmpdir, monkeypatch):
    app_config_dir = tmpdir.mkdir('config')
    app_config_dir.join('config').write('bad content')
    monkeypatch.setattr('qwcore.config.AppDirs', lambda name: stub(user_config_dir=str(app_config_dir)))
    with pytest.raises(exceptions.ConfigFileParserError):
        config.get_config('app')


def test_get_config(tmpdir, monkeypatch):
    app_config_dir = tmpdir.mkdir('config')
    app_config_dir.join('config').write('key = value')
    monkeypatch.setattr('qwcore.config.AppDirs', lambda name: stub(user_config_dir=str(app_config_dir)))
    assert config.get_config('app').get('key') == 'value'
