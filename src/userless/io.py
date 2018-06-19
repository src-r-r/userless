#!/usr/bin/env python3

# from queue import Queue
from threading import (
    Thread,
    Semaphore,
)
import pickle
from time import sleep
from redis import (
    Redis,
    ConnectionPool,
)

import logging

log = logging.getLogger(__name__)

QUEUE_INTERVAL = 0.1


class RedisQueue(Redis):

    def __init__(self, *args, **kwargs):
        self._s = kwargs.pop('seperator', ';')
        super(RedisQueue, self).__init__(*args, **kwargs)

    def qitems(self, key):
        val = self.get(key)
        if not (val and len(val)):
            return []
        return pickle.loads(val)

    def qlength(self, key):
        return len(self.qitems(key))

    def _qset(self, key, items):
        self.set(key, pickle.dumps(items))

    def qpush(self, key, item):
        if not self.exists(key):
            items = []
        else:
            try:
                items = self.qitems(key)
            except pickle.UnpicklingError as ue:
                # occurs if data is something other than a list.
                items = []
        items.insert(0, item)
        self._qset(key, items)

    def qpop(self, key):
        items = self.qitems(key)
        if not (len(items)):
            return None
        item = items.pop(-1)
        self._qset(key, items)
        return item


class GeneralizedUserQueue(Thread):
    """ Queue for email verification. """

    SLEEP_TIME = 10
    REDIS_KEY = 'users'

    def __init__(self, redis_pool_args, UserClass, db, flask_context, *args,
                 **kwargs):
        """ Construct a new email verification queue.

        :param user_function: Function to call during queue processing.

        :param args: Args for the thread.

        :param kwargs: keyword args for the thread.

        :parm escargo_server: `(host, port)` of escargo server.
        Default is ('127.0.0.1', 5000)
        :optional escargo_server: True
        """
        self._lock = Semaphore()
        self._running = False
        self.flask_context = flask_context
        self.redis_pool = ConnectionPool(**redis_pool_args)
        self.User = UserClass
        self.db = db
        super(GeneralizedUserQueue, self).__init__(*args, **kwargs)

    def process(self, user):
        """ Process a user. """
        raise NotImplementedError()

    def run(self):
        """ Run the email verification queue. """
        self._running = True
        while self._running:
            self._lock.acquire()  # !! BEGIN CRITICAL SECTION
            redis = RedisQueue(connection_pool=self.redis_pool)
            uid = redis.qpop(self.REDIS_KEY)
            if uid is None:
                log.debug('no user found in queue...waiting')
                sleep(QUEUE_INTERVAL)
                self._lock.release()
                # redis.release()
                continue
            uid = int(uid)
            with self.flask_context:
                user = self.db.query(self.User).filter_by(id=uid).first()

            if user:
                self.process(user)
                # !! END REGIION !!
                self._lock.release()
                sleep(QUEUE_INTERVAL)
                continue

            log.warning('User with id=`{}` does not exist'.format(uid))
            self._lock.release()
            sleep(QUEUE_INTERVAL)

    def stop(self):
        self._running = False

    def add_user(self, user):
        """ Add a user to the queue.

        :param user: User to be added to the queue.
        """
        self._lock.acquire()  # -- BEGIN CRITCAL SECTION
        try:
            r = RedisQueue(connection_pool=self.redis_pool)
            if not hasattr(user, 'id'):
                self._lock.release()
                raise AttributeError('user has no `id` attribute')
            r.qpush(self.REDIS_KEY, user.id)
        except Exception as e:
            pass
        except TypeError as te:
            pass
        self._lock.release()  # -- END CRITICAL SECTION
        return True

    def __del__(self):
        self._lock.acquire()  # -- BEGIN CRITCAL SECTION
        r = RedisQueue(connection_pool=self.redis_pool)
        if not r.exists(self.REDIS_KEY):
            r.set(self.REDIS_KEY, '')
        del r
        self._lock.release()  # -- END CRITICAL SECTION

    def __str__(self):
        """ String format. """
        return "<{} ({} users)>".format(self.__class__.__name__,
                                        len(self.users))


class EmailUserQueue(GeneralizedUserQueue):

    def __init__(self, escargo, *args, **kwargs):
        self.subject = kwargs.pop('subject', None)
        self.escargo = escargo
        self.escargo_server = kwargs.pop('escargo_server', ('127.0.0.1', 5000))
        super(EmailUserQueue, self).__init__(*args, **kwargs)


class UserVerificationQueue(EmailUserQueue):

    def __init__(self, verification_url, *args, **kwargs):
        self.verification_url = verification_url
        super(UserVerificationQueue, self).__init__(*args, **kwargs)

    def process(self, user):
        user.send_verification_email(self.escargo,
                                     self.verification_url,
                                     self.subject,
                                     self.escargo_server)


class UserPasswordResetQueue(EmailUserQueue):

    def __init__(self, reset_url, *args, **kwargs):
        self.reset_url = reset_url
        super(UserPasswordResetQueue, self).__init__(*args, **kwargs)

    def process(self, user):
        return user.send_password_reset_email(self.escargo,
                                              self.reset_url,
                                              self.subject,
                                              self.escargo_server)
