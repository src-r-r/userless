#!/usr/bin/env python3

import unittest
import random

import logging
import pickle
from time import sleep
# import logging.config

from faker import Faker

from userless.io import (
    RedisQueue,
    GeneralizedUserQueue,
)

from userless.models import (
    User,
    Group,
)

fake = Faker()

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)

class TestRedisQueue(unittest.TestCase):

    def test_init(self):
        rq = RedisQueue()
        self.assertIsNotNone(rq)

    def test_push(self):
        rq = RedisQueue()
        rq.set('x', '')
        rq.delete('x')
        rq.qpush('x', 4)
        self.assertEqual(pickle.loads(rq.get('x')), [4, ])

    def test_items(self):
        rq = RedisQueue()
        rq.set('x', '')
        rq.delete('x')
        expected = [
            4,
            'magical',
            1.3,
            {'a': 4, 'b': 7, },
        ]
        for e in expected:
            rq.qpush('x', e)
        items = rq.qitems('x')
        expected.reverse()
        self.assertEqual(items, expected)

    def test_pop(self):
        rq = RedisQueue()
        rq.set('x', '')
        rq.delete('x')
        expected = [
            4,
            'magical',
            1.3,
            {'a': 4, 'b': 7, },
        ]
        for e in expected:
            rq.qpush('x', e)
        self.assertEqual(rq.qlength('x'), 4)
        self.assertEqual(rq.qpop('x'), expected[0])
        self.assertEqual(rq.qlength('x'), 3)
        self.assertEqual(rq.qpop('x'), expected[1])
        self.assertEqual(rq.qlength('x'), 2)
        self.assertEqual(rq.qpop('x'), expected[2])
        self.assertEqual(rq.qlength('x'), 1)
        self.assertEqual(rq.qpop('x'), expected[3])
        self.assertEqual(rq.qlength('x'), 0)

from userless.models import db
from userless.main import create_app

class ExampleUserQueue(GeneralizedUserQueue):

    def __init__(self):
        redis_pool_args = dict(
            host='localhost',
            port=6379,
            db=0
        )
        super(ExampleUserQueue, self).__init__(redis_pool_args, User, db)
        self.processed_users = []

    def process(self, user):
        log.debug('processing {}'.format(user))
        self.processed_users.append(user)
        return True


class TestUserQueue(unittest.TestCase):

    def setUp(self):
        self.app = create_app('../assets/configurations/test.py')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        # self.ctx = app.app_context()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_uq(self):
        euq = ExampleUserQueue()
        # Simulate adding several users
        n_users = random.randint(5, 10)
        euq.start()
        log.debug('generating {} users'.format(n_users))
        with self.app.app_context():
            for i in range(0, n_users):
                user = User(email=fake.email(),
                            password=fake.password())
                db.session.add(user)
                db.session.commit()
                euq.add_user(user)
                sleep(random.random())  # wait for at most 1 second
        # Wait a while to let the queue finish
        sleep(1.5)
        self.assertEqual(len(euq.processed_users), n_users)
        euq.stop()
