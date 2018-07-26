from typing import List


def format_error_path(path: List[str]) -> str:
    return '.'.join([str(item) for item in path])


def generate_error_string(message: str, path: List[str]) -> str:
    equals_str = ''
    if len(path):
        equals_str = ' = '

    return '{0}{1}{2}'.format(format_error_path(path), equals_str, message)
