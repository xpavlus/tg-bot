import json
import os


class ConfigException(Exception):
    pass


class ConfigFileMissing(ConfigException):
    pass


class ConfigSectionMissing(ConfigException):
    pass


class Config:
    default_section = "telegram"
    default_config_path = "./config.json"

    def __init__(self, path: str = None):
        self.path = path if path else self.default_config_path
        self._dict = {}

    @staticmethod
    def get_full_option_name(section: str, option: str) -> str:
        return f"{section}_{option}"

    @staticmethod
    def get_env_var(section: str, option: str = None, fallback=None):
        _var_name = Config.get_full_option_name(section, option)
        return os.getenv(_var_name, fallback)

    def open(self, config_path: str = None) -> {str: str}:
        if config_path:
            self.path = config_path
        if os.path.isfile(self.path):
            with open(self.path) as c:
                self._dict = json.loads(c.read())
        else:
            raise ConfigFileMissing("Config file does not exists")

    def copy(self):
        return self._dict

    def get_section(self, section: str) -> {str: str}:
        if section in self._dict.keys():
            return self._dict[section]
        else:
            raise ConfigSectionMissing("Section does not exists")

    def has_section(self, section: str) -> bool:
        try:
            return section in self._dict.keys()
        except KeyError:
            return False

    def get(self, section: str, option: str = None, fallback=None):
        if option is None:
            option = section
            section = Config.default_section
        if self.get_env_var(section, option):
            return self.get_env_var(section, option)
        else:
            if option in self._dict[section].keys():
                return self._dict[section][option]
            else:
                return fallback

    def has(self, section: str, option: str = None) -> bool:
        if option is None:
            option = section
            section = self.default_section
        try:
            return bool(self.get_env_var(section, option)) or option in self._dict[section].keys()
        except KeyError:
            return False
