import os

from appdirs import AppDirs
import configobj

from qwcore.exception import ConfigFileNotFoundError, ConfigFileParserError


def get_config(appname):
    """Return the `configobj` object for an app, assuming it's config file is in the
    XDG compliant path for an app named `appname`, and where the actual config
    file is named 'config'

    :param appname: app name
    :raise ConfigFileNotFoundError: if the config file is not found
    :raise ConfigFileParserError: if the config file is invalid

    """
    config_dir = AppDirs(appname).user_config_dir
    config_file = os.path.join(config_dir, 'config')
    if not os.path.isfile(config_file):
        msg = "Config file not found: {f}".format(f=config_file)
        raise ConfigFileNotFoundError(msg)
    try:
        config = configobj.ConfigObj(config_file)
    except configobj.ConfigObjError as e:
        raise ConfigFileParserError(str(e))
    return config
