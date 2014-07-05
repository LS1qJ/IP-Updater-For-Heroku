#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import bmemcached

"""
Memcache Client
"""


class MCache(object):

    def __init__(self, server, username, password):
        self.server = bmemcached.Client(server, username, password)

    def set(self, key, value, sec=600):
        """
        Set a new value in the memcache server.
        Expire time is given with "sec" argument.
        """
        key = self._keystr(key)
        self.server.set(key, value, sec)

    def get(self, key):
        """
        Retrieve a value from the memcache server
        """
        key = self._keystr(key)
        val = self.server.get(key)

        if not val:
            if val == []:
                return val
            return None
        return val

    def delete(self, key):
        """
        Delete a value from the memcached server.
        """
        key = self._keystr(key)
        self.server.delete(key)

    def refresh(self):
        self.server.flush_all()

    def _keystr(sekf, string):
        key = str(string)
        if len(string) > 250:
            key = hashlib.sha1(string).hexdigest()
        return key
