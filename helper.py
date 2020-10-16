import logging
import pymongo
import pytz
import os
import records
import toml

_CONFIG = {}
_CONFIG.update(toml.load('config/' + os.getenv('ENV', 'local') + '.toml'))

logging.basicConfig(
    format=_CONFIG['default']['log_format'],
    level=getattr(logging, _CONFIG['default']['log_level'].upper())
)

DATABASES = _CONFIG['mysql']
SLAVE_DB = None
TC = None

DATABASE_URL = f'mysql+pymysql://{DATABASES["USER"]}:{DATABASES["PASSWORD"]}@{DATABASES["HOST"]}:' \
               f'{DATABASES["PORT"]}/{DATABASES["NAME"]}?charset={DATABASES["OPTIONS"]["charset"]}'
_database = records.Database(DATABASE_URL, echo=True, pool_recycle=60, pool_timeout=30)

if SLAVE_DB:
    url = f'mysql+pymysql://{SLAVE_DB["USER"]}:{SLAVE_DB["PASSWORD"]}@{SLAVE_DB["HOST"]}:' \
          f'{SLAVE_DB["PORT"]}/{SLAVE_DB["NAME"]}?charset={SLAVE_DB["OPTIONS"]["charset"]}'
    slave_database = records.Database(url, echo=True, pool_recycle=60, pool_timeout=30)
else:
    slave_database = _database


def db_query(sql, *args, **kwargs):
    if TC:
        TC.query(sql, *args, **kwargs)
    elif sql.startswith('SELECT'):
        return slave_database.query(sql, *args, **kwargs)
    else:
        return _database.query(sql, *args, **kwargs)


class Transaction:
    def __init__(self):
        global TC
        if TC:
            raise Exception("不能嵌套事务")
        self.conn = _database.get_connection()
        self.tx = self.conn.transaction()
        TC = self.conn

    def _close(self):
        global TC
        TC = None
        self.conn.close()

    def rollback(self):
        self.tx.rollback()
        self._close()

    def commit(self):
        self.tx.commit()
        self._close()


def get_config():
    return _CONFIG


_connection = pymongo.MongoClient(_CONFIG['mongodb']['url'], tz_aware=True,
                                  read_preference=pymongo.ReadPreference.SECONDARY_PREFERRED,
                                  tzinfo=pytz.timezone('Asia/Shanghai'))
# _connection = pymongo.MongoClient(
#     _CONFIG['mongodb']['url'],
#     replicaSet=_CONFIG['mongodb']['replica_set'],
#     tz_aware=True,
#     connect=False,
#     read_preference=pymongo.ReadPreference.SECONDARY_PREFERRED,
# )

_db = _connection[_CONFIG['mongodb']['database']]
if _CONFIG['mongodb']['auth']:
    _db.authenticate(_CONFIG['mongodb']['user'], _CONFIG['mongodb']['pass'])


def get_mongodb():
    return _db
