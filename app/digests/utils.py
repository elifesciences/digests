import json
import os
import re
from typing import Dict


from elife_api_validator import SCHEMA_DIRECTORY


def get_schema(schema_name: str) -> Dict:
    with open(os.path.join(SCHEMA_DIRECTORY, schema_name)) as schema:
        val = json.loads(schema.read())
        return val


def get_schema_name(content_type, file_type='json') -> str:
    """Returns a formatted content type string.
    >>> get_schema_name('application/vnd.elife.disgest+json; version=1')
    'digest.v1.json'
    :return: str
    """
    schema_name = ''
    version = '1'

    name_result = re.search(r'(?<=\.)[a-z-]*?(?=\+)', content_type)
    if name_result:
        schema_name = name_result.group()

    version_result = re.search(r'(?<=)[0-9]+', content_type)
    if version_result:
        version = version_result.group()

    return f'{schema_name}.v{version}.{file_type}'
