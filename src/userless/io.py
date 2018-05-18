#!/usr/bin/env python3

# from queue import Queue
from threading import (
    Thread,
    Semaphore,
)
from time import sleep

class EmailVerificationQueue(Thread):

    SLEEP_TIME = 10

    def __init__(*args, **kwargs):
        self.users = []
        self._lock = Semaphore()
        self._running = False
        super(EmailVerificationQueue, self).__init__(*args, **kwargs)

    def run(self):
        self._running = True
        while self._running:
            if len(self.users) == 0:
                continue
            u = self.users.pop(0)

    def add_user(self)
