import datetime

from steemdata.utils import typify


def test_typify():
    untyped = {'amount_to_sell': '0.784 SBD',
               'block_num': 8926306,
               'expiration': '2017-02-06T10:01:46',
               'fill_or_kill': False,
               'min_to_receive': '4.868 STEEM',
               'proof': {'inputs': [{'foo': {'bar': '4.868 STEEM'}},
                                    3055534,
                                    16227194]}
               }
    typed = {'amount_to_sell': {'amount': 0.784, 'asset': 'SBD'},
             'block_num': 8926306,
             'expiration': datetime.datetime(2017, 2, 6, 10, 1, 46),
             'fill_or_kill': False,
             'min_to_receive': {'amount': 4.868, 'asset': 'STEEM'},
             'proof': {'inputs': [{'foo': {'bar': {'amount': 4.868, 'asset': 'STEEM'}}},
                                  3055534,
                                  16227194]}}

    assert typify(untyped) == typed
