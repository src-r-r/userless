#!/usr/bin/env python3

# SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://userless:8Hdsj8cYuk@localhost/userless_unittest_0_1'
CELERY_RESULT_BACKEND = 'rpc://rabit@sumo//'
CELERY_BROKER_URL = 'rpc://rabit@sumo//'
