import json
import os.path
from unittest import TestCase
from config import Config, ConfigException
from test_utils import generate_string, generate_non_existent_file


class TestConfig(TestCase):
    _config_file = generate_non_existent_file()
    _non_existent_config_file = generate_non_existent_file()

    _env_section = generate_string()
    _env_option = generate_string()
    _env_name = f"{_env_section}_{_env_option}"
    _env_value = generate_string()

    _section = generate_string()
    _option = generate_string()
    _test_dict = {
        _section: {
            _option: generate_string(),
        },
        _env_section: {
            _env_option: _env_value + generate_string(),
        }
    }

    def setUp(self) -> None:
        with open(self._config_file, 'w') as c:
            json.dump(self._test_dict, c)
        os.environ[self._env_name] = self._env_value
        self._config = Config(self._config_file)
        self._config.open()

    def tearDown(self) -> None:
        os.remove(self._config_file)
        os.unsetenv(self._env_name)

    def test_open(self):
        _conf_dict = self._config.copy()
        self.assertDictEqual(_conf_dict, self._test_dict)
        with self.assertRaises(ConfigException):
            self._config.open(self._non_existent_config_file)

    def test_get_section(self):
        self.assertDictEqual(self._config.get_section(self._section), self._test_dict[self._section])

    def test_has_section(self):
        self.assertTrue(self._config.has_section(self._section))
        self.assertFalse(self._config.has_section(self._section + "_"))

    def test_get(self):
        self.assertEqual(
            self._config.get(self._section, self._option),
            self._test_dict[self._section][self._option])
        _default_value = generate_string()
        self.assertEqual(
            self._config.get(self._section, self._option + '_', _default_value),
            _default_value)
        self.assertEqual(
            self._config.get(self._env_section, self._env_option),
            self._env_value)

    def test_has(self):
        self.assertTrue(self._config.has(self._section, self._option))
        self.assertFalse(self._config.has(self._section + '_', self._option))
        self.assertFalse(self._config.has(self._section, self._option + '_'))

    def test_get_env_var(self):
        self.assertEqual(
            self._config.get_env_var(self._env_section, self._env_option),
            self._env_value)

        _default_value = generate_string()
        self.assertEqual(
            self._config.get_env_var(self._env_section, self._env_option + '_', _default_value),
            _default_value)

    def test_get_full_option_name(self):
        self.assertEqual(
            Config.get_full_option_name(self._section, self._option),
            f"{self._section}_{self._option}")
