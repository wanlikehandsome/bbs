import time
import json
from models import Model
from models.user import User
from models.mongua import Mongua
import logging
import os
import time
ogger = logging.getLogger("bbs")


class Cache(object):
    def get(self, key):
        pass

    def set(self, key, value):
        pass


class MemoryCache(Cache):
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache[key]

    def set(self, key, value):
        self.cache[key] = value


class RedisCache(Cache):
    import redis
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set(self, key, value):
        return RedisCache.redis_db.set(key, value)

    def get(self, key):
        return RedisCache.redis_db.get(key)


class Topic(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('content', str, ''),
        ('title', str, -1),
        ('user_id', int, -1),
        ('board_id', int, -1),
        ('views', int, 0)
    ]

    should_update_all = True
    # 1. memory cache
    cache = MemoryCache()
    # 2. redis cahce
    redis_cache = RedisCache()
    def to_json(self):
        """
         将从MongoDB中查询到的对象转化为json格式
        :return: json str
        """
        d = dict()
        for k in Topic.__fields__:
            key = k[0]
            if not key.startswith('_'):
                # 过滤 _id
                d[key] = getattr(self,key)
        return json.dumps(d)

    @classmethod
    def from_json(cls, j):
        """
        根据json格式的数据, 返回一个topic对象
        :param j: josn
        :return: topic object
        """
        d = json.loads(j)

        instance = cls()
        for k, v in d.items():
            setattr(instance, k, v)
        return instance

    @classmethod
    def all_delay(cls):
        return Topic.all()

    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def save(self):
        super(Topic, self).save()
        should_update_all = True

    @classmethod
    def cache_all(cls):
        """数据更新一次, 缓存更新一次
        :return: topic list
        """
        if Topic.should_update_all:
            Topic.redis_cache.set('topic_all', json.dumps([i.to_json() for i in cls.all_delay()]))
            Topic.should_update_all = False
        j = json.loads(Topic.redis_cache.get('topic_all').decode('utf-8'))
        j = [Topic.from_json(i) for i in j]
        return j

    @classmethod
    def cache_find(cls, board_id):
        """数据更新一次, 缓存更新一次
        :return: topic list
        """
        j = json.loads(Topic.redis_cache.get('topic_all').decode('utf-8'))
        j = [Topic.from_json(i) for i in j]
        topics_in_board = []
        for topic_object in j:
            if topic_object.board_id == board_id:
                topics_in_board.append(topic_object)
        return topics_in_board



    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def board(self):
        from .board import Board
        m = Board.find(self.board_id)
        return m

    def user(self):
        u = User.find(id=self.user_id)
        return u
