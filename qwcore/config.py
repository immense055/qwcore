import os

from appdirs import AppDirs
import configobj

from qwcore import exceptions


def get_config(appname):
    """Return the config object for an app

    :param appname: app name
    """
    config_dir = AppDirs(appname).user_config_dir
    config_file = os.path.join(config_dir, 'config')
    if not os.path.isfile(config_file):
        msg = "Config file not found: {f}".format(f=config_file)
        raise exceptions.ConfigFileNotFoundError(msg)
    try:
        config = configobj.ConfigObj(config_file)
    except configobj.ConfigObjError as e:
        raise exceptions.ConfigFileParserError(str(e))
    return Config(config)


class Config(object):

    def __init__(self, configobj):
        self.configobj = configobj

    def get(self, key, section=None):
        """Return a config value by key and section"""
        config = self.configobj
        try:
            if section:
                config = config[section]
            return config[key]
        except (KeyError, configobj.ConfigObjError) as e:
            raise exceptions.ConfigFileKeyError(str(e))
