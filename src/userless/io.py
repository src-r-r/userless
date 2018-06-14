#!/usr/bin/env python3

# from queue import Queue
from threading import (
    Thread,
    Semaphore,
)
from time import sleep


class EmailVerificationQueue(Thread):
    """ Queue for email verification. """

    SLEEP_TIME = 10

    def __init__(self, email_config, *args, **kwargs):
        """ Construct a new email verification queue.

        :param email_config: Configuration to pass of to escargo.

        :param args: Args for the thread.

        :param kwargs: keyword args for the thread.
        """
        self.users = []
        self._lock = Semaphore()
        self._running = False
        self.email_config = email_config
        super(EmailVerificationQueue, self).__init__(*args, **kwargs)

    def run(self):
        """ Run the email verification queue. """
        self._running = True
        while self._running:
            if len(self.users) == 0:
                continue
            self._lock.acquire()
            # !! BEGIN CRITICAL SECTION
            u = self.users.pop(0)
            u.send_verification_email()
            # !! END REGIION !!
            self._lock.release()

    def add_user(self, user):
        """ Add a user to the queue.

        :param user: User to be added to the queue.
        """
        self._lock.acquire()  # -- BEGIN CRITCAL SECTION
        self.users.append(user)
        self._lock.release()  # -- END CRITICAL SECTION

    def __str__(self):
        """ String format. """
        return "<{} ({} users)>".format(self.__class__.__name__,
                                        len(self.users))
