import redis
import pprint
from operator import itemgetter

redis_host = 'localhost'
skip_keys = ['voters']


if __name__ == '__main__':
    db=redis.Redis(redis_host)
    outl = []
    keys = db.keys()
    for k in keys:
        k=k.decode('utf-8')
        if k in skip_keys:
            continue
        outl.append((k,db.llen(k)))
        outs = sorted(outl, key=itemgetter(1), reverse=False)
    pprint.pprint(outs)
    input()
