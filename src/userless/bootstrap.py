#!/usr/bin/env python3

import os
import logging

from userless.paths import (
    _REQUIRED_DIRS,
    _REQUIRED_FILES,
    _SUGGESTED_FILES,
)

log = logging.getLogger(__name__)

def check():
    for d in _REQUIRED_DIRS:
        log.debug('check if dir exists: {}'.format(d))
        if not os.path.exists(d):
            os.makedirs(d)
    missing_required = []
    for f in _REQUIRED_FILES:
        log.debug('check for file: {}'.format(f))
        if not os.path.exists(f):
            missing_required.append(f)
    if len(missing_required) > 0:
        log.error("Missing required files:")
        for f in missing_required:
            log.error('✘ {}'.format(f))
        return False
    missing_suggested = []
    for d in _SUGGESTED_FILES:
        log.debug('(optional) check file: {}'.format(f))
        if not os.path.exists(f):
            missing_suggested.append(f)

    if len(missing_suggested) > 0:
        log.warn('missing {} suggested files:'.format(len(missing_suggested)))
        for ms in missing_suggested:
            log.warn('⚠ {}'.format(ms))

    log.info('[✔] preflight check successful')
    return True
