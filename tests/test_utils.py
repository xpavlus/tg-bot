import os
import random


def generate_non_existent_file(path_base: str = None, file_name_base: str = None):
    if path_base is None:
        path_base = os.path.curdir
    if file_name_base is None:
        _filename = generate_string(5)
    else:
        _filename = file_name_base + generate_string(5)
    for _ in range(5):
        _file = os.path.join(path_base, _filename)
        if not os.path.isfile(_file):
            return _file
    else:
        raise FileExistsError("All attempts to create a config files have failed")


def generate_string(length: int = None, symbol_sets: [str] = None):
    if length is None:
        length = random.randint(0, 10)
    _symbol_sets = {
        'letters': 'abcdefghijklmnopqrstuvwxyz',
        'numbers': '0123456789',
        'spec': '_-+#$@'
    }
    if symbol_sets is None:
        symbol_sets = ['letters', 'numbers']
    alphabet = ''.join([_symbol_sets[s] for s in symbol_sets])
    contents = [random.choice(alphabet) for _ in range(length)]
    return ''.join(contents)


def generate_int(max_num: int = 10000, positive_only: bool = False):
    if positive_only:
        return random.randint(0, max_num)
    else:
        return random.randint(-max_num, max_num)