import logging
import os

from appdirs import AppDirs
import configobj

from qwcore import exception

LOG = logging.getLogger(__name__)


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
        raise exception.ConfigFileNotFoundError(msg)
    try:
        config = configobj.ConfigObj(config_file)
    except configobj.ConfigObjError as e:
        raise exception.ConfigFileParserError(str(e))
    return config


def get_value(appname, key, section=None, default=None):
    """Return a config value

    :param appname: app name
    :param key: config key
    :param section: config section
    :param default: default value if config file not present or key/section not present
    """
    try:
        config = get_config(appname)
    except exception.ConfigFileNotFoundError as e:
        if default:
            LOG.info("Config file not found, using default value: {d}".format(d=default))
            return default
        else:
            raise e
    if section:
        try:
            config = config[section]
        except KeyError as e:
            if default:
                LOG.info("section '{s}' not found in config file, using default: {d}".format(s=section, d=default))
                return default
            else:
                raise exception.ConfigFileSectionNotFoundError(
                    "section '{s}' not found in config file".format(s=section))
    try:
        return config[key]
    except KeyError as e:
        if default:
            LOG.info("'{k}' key not found in config file, using default: {d}".format(k=key, d=default))
            return default
        else:
            raise exception.ConfigFileKeyNotFoundError(
                "key '{s}' not found in config file".format(s=section))
