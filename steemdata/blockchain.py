import warnings

from steem.blockchain import Blockchain as SteemBlockchain


class Blockchain(SteemBlockchain):
    """ Access the blockchain and read data from it.

    Args:
        steem_instance (Steemd): Steemd() instance to use when accessing a RPC
        mode (str): `irreversible` or `head`. `irreversible` is default.
    """

    def __init__(self, steem_instance=None, mode="irreversible"):
        warnings.warn('steemdata.Blockchain is deprecated. Use steem.Blockchain instead!')
        super(Blockchain, self).__init__(steem_instance, mode)
