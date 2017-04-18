import warnings

from steem.blog import Blog as SteemBlog


class Blog(SteemBlog):
    """ Obtain a list of blog posts of an account

        :param str account_name: Name of the account
        :param Steemd steemd_instance: Steemd() instance to use when accessing a RPC

    """

    def __init__(self, account_name, steemd_instance=None):
        warnings.warn('steemdata.Blog is deprecated. Use steem.Blog instead!')
        super(Blog, self).__init__(account_name, steemd_instance)
