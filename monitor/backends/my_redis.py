#_*_coding:utf-8_*_
# Author:Topaz

import redis
def redis_conn(redis_settings):
    pool = redis.ConnectionPool(host=redis_settings.REDIS_CONN['HOST'],
                                port=redis_settings.REDIS_CONN['PORT'],
                                db=redis_settings.REDIS_CONN['DB']
                                )
    r = redis.Redis(connection_pool=pool)
    return r