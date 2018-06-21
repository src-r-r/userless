#!/usr/bin/env python3

import unittest
import random

import logging
# import pickle
from time import sleep
# import logging.config

from sqlalchemy.inspection import (
    inspect,
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from faker import Faker

# from userless.io import (
#     process_user_verification,
#     process_password_reset,
# )

from userless.models import (
    User,
    # Group,
)


from userless.extension import (
    celery,
    db,
)
from userless.main import create_app


fake = Faker()

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger(__name__)


app = create_app('../assets/configurations/test.py')
celery.init_app(app)


@celery.task
def verify_user(user_id):
    """ Test task to just set a user to verified.

    :param user_id: ID of the user to set to 'verified'
    """
    log.debug('verifying user id={}'.format(user_id))
    u = db.session.query(User).filter_by(id=user_id).first()
    u.is_verified = True
    db.session.commit()
    return u


class TestUserQueue(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_uq(self):
        # Simulate adding several users
        global verify_userZ
        n_users = random.randint(5, 10)
        log.debug('generating {} users'.format(n_users))
        with app.app_context():
            for i in range(0, n_users):
                user = User(email=fake.email(),
                            password=fake.password())
                db.session.add(user)
                db.session.commit()
                log.debug('verifying {} of {} ({})'.format(i, n_users, user))
                result = verify_user.delay(user.id)
                # Wait a while to let the queue finish
                # result.wait()
                u = result.get()
                if (isinstance(u, User)):
                    self.assertTrue(u.is_verified)
                else:
                    log.debug('result #{} = {}'.format(i, type(result.get()).__name__))
                sleep(random.random() + 0.2)
        with app.app_context():
            verified = db.session.query(User)\
                                 .filter_by(is_verified=True)\
                                 .count()
            self.assertEqual(verified, n_users)
