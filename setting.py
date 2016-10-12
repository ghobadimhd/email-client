import  configparser

SETTINGS_PATH = '.setting'
CONFIG_SECTION = 'DEFAULT'
NECESSARY_SETTINGS = ['smtp_server', 'pop3_server', 'pop3_user', 'pop3_pass']
ALL_SETTINGS = ['smtp_server', 'smtp_user', 'smtp_pass', 'pop3_server', 'pop3_user', 'pop3_pass']

class SettingMissing(Exception):
    """This excepion should used when there is error in setting"""
    def __init__(self, param_name):
        super(SettingMissing, self).__init__()
        self.param_name = param_name

class SettingEmpty(Exception):
    """This excepion should used when there is error in setting"""
    def __init__(self, param_name):
        super(SettingEmpty, self).__init__()
        self.param_name = param_name


def read_section(path=SETTINGS_PATH, section=CONFIG_SECTION):
    settings = configparser.ConfigParser()
    settings.read(path)
    return settings[section]

def write(configs, path=SETTINGS_PATH, section=CONFIG_SECTION):
    settings = configparser.ConfigParser()
    settings[section] = configs
    with open(path, 'w') as config_file:
        settings.write(config_file)

def read(path=SETTINGS_PATH):
    settings = configparser.ConfigParser()
    settings.read(path)
    return settings

def missing_param(setting, param_name):
    """Check setting for particular parameter existance

    if parameter did not exist in setting file raise an exception

    Args:
        param_name: name of parameter
    raise:
        SettingMissing:

    """
    if param_name not in setting:
        raise SettingMissing(param_name)

def check_necessary_config(setting):
    for param in NECESSARY_SETTINGS:
        missing_param(setting, param)

def add_missing_param(setting):
    """This fuction read setting and if find out some param is missed
        create it with empty vlaue
    """
    for param in ALL_SETTINGS:
        try:
            missing_param(setting, param)
        except SettingMissing:
            setting[param] = ""

def empty_param(setting, param_name):
    """Check setting for particular parameter empty

    if parameter is empty in setting file raise an exception

    Args:
        param_name: name of parameter
    raise:
        SettingEmpty:

    """
    missing_param(setting, param_name)
    if setting[param_name]:
        raise SettingEmpty(param_name)
