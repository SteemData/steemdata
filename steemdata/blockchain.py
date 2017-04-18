import re
import warnings
from typing import Union

from funcy.colls import walk_values
from steem.amount import Amount
from steem.blockchain import Blockchain as SteemBlockchain
from steem.utils import parse_time, keep_in_dict


class Blockchain(SteemBlockchain):
    """ Access the blockchain and read data from it.

    Args:
        steem_instance (Steemd): Steemd() instance to use when accessing a RPC
        mode (str): `irreversible` or `head`. `irreversible` is default.
    """

    def __init__(self, steem_instance=None, mode="irreversible"):
        warnings.warn('steemdata.Blockchain is deprecated. Use steem.Blockchain instead!')
        super(Blockchain, self).__init__(steem_instance, mode)


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


if __name__ == '__main__':
    b = Blockchain()
    print(len(list(b.stream(start=9563511, stop=9563511))))
    quit(0)
    for event in b.stream(start=9563511, full_blocks=True):
        if event['trx_id'] == '0000000000000000000000000000000000000000':
            print(event)
