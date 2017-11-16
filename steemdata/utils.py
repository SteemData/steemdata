import json
import re
from json import JSONDecodeError
from typing import Union

from funcy.colls import walk_values
from steem.amount import Amount
from steem.utils import keep_in_dict, parse_time
from toolz import update_in, assoc


def typify(value: Union[dict, list, set, str]):
    """ Enhance block operation with native types.

    Typify takes a blockchain operation or dict/list/value,
    and then it parses and converts string types into native data types where appropriate.
    """
    if type(value) == dict:
        return walk_values(typify, value)

    if type(value) in [list, set]:
        return list(map(typify, value))

    if type(value) == str:
        if re.match('^\d+\.\d+ (STEEM|SBD|VESTS)$', value):
            return keep_in_dict(dict(Amount(value)), ['amount', 'asset'])

        if re.match('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$', value):
            return parse_time(value)

    return value


def safe_json_loads(data: str):
    try:
        return json.loads(data)
    except JSONDecodeError:
        return {}


def json_expand(json_op):
    """ For custom_json ops. """
    if type(json_op) == dict and 'json' in json_op:
        return update_in(json_op, ['json'], safe_json_loads)

    return json_op


def remove_body(op):
    """ Remove Post Body to save disk space"""
    if op['type'] == 'comment' and 'body' in op:
        return assoc(op, 'body', '')
    return op
