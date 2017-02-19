import logging

import pymongo
from pymongo.errors import ConnectionFailure

log = logging.Logger('steemdata-lib')


class SteemData(object):
    def __init__(self,
                 db_name='SteemData',
                 host='steemit:steemit@mongo1.steemdata.com',
                 port=27017):
        try:
            self.mongo_url = 'mongodb://%s:%s/%s' % (host, port, db_name)
            client = pymongo.MongoClient(self.mongo_url)
            self.db = client[db_name]

        except ConnectionFailure as e:
            log.error('Can not connect to MongoDB server: %s' % e)
            raise
        else:
            self.load_collections()

    def list_collections(self):
        return self.db.collection_names()

    def load_collections(self):
        for coll in self.list_collections():
            setattr(self, coll, self.db[coll])

    def info(self):
        print(self.mongo_url)


if __name__ == '__main__':
    s = SteemData()
    s.info()
