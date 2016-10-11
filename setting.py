import  configparser

settings_PATH = '.setting'
CONFIG_SECTION = 'DEFAULT'

def read_section(path=settings_PATH, section=CONFIG_SECTION):
    settings = configparser.ConfigParser()
    settings.read(path)
    return settings[section]

def write(configs, path=settings_PATH, section=CONFIG_SECTION):
    settings = configparser.ConfigParser()
    settings[section] = configs
    with open(path, 'w') as config_file:
        settings.write(config_file)

def read(path=settings_PATH):
    settings = configparser.ConfigParser()
    settings.read(path)
    return settings