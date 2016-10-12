import  configparser

SETTINGS_PATH = '.setting'
CONFIG_SECTION = 'DEFAULT'
NECESSARY_SETTINGS = ['smtp_server', 'pop3_server', 'pop3_user', 'pop3_pass']

class SettingMissing(Exception):
    """This excepion should used when there is error in setting"""
    def __init__(self, param_name):
        super(SettingMissing, self).__init__()
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

def check_necessary_config(setting, section=CONFIG_SECTION):
    for param in setting[section]:
        missing_param(setting, param)
