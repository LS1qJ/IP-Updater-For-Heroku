#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from config import Config


class DozensApi(object):
    """
    Wrapping DozensAPI
    (https://sites.google.com/a/dozens.jp/docs/)
    This class do not wrap whole apis.
    Implementing minimum APIs to maitan A records.
    """

    def __init__(self):
        request_token = self._get_request_token()
        self.common_headers = {
                "X-Auth-Token": request_token,
                "Content-Type": " application/json"
                }

    def _get_request_token(self):
        url = 'http://dozens.jp/api/authorize.json'
        headers = {
                "X-Auth-User": Config.DOZENS_ID,
                "X-Auth-Key": Config.DOZENS_APIKEY
                }
        r = requests.get(url, headers = headers)
        r.raise_for_status()
        return r.json()["auth_token"]

    def get_records(self, zone_name):
        url = "http://dozens.jp/api/record/%s.json" % zone_name
        r = self._get(url)
        return r.json()

    def post_update_record(self, record_id, prio, content, ttl):
        url = "http://dozens.jp/api/record/update/%s.json" % record_id
        payload = {"prio": prio,
                "content": content,
                "ttl": ttl}
        r = self._post(url, payload)
        return r.json()

    def post_create_record(self, domain, name,
                        record_type, prio, content, ttl):
        url = "http://dozens.jp/api/record/create.json"
        payload = {"domain": domain,
                "name": name,
                "type": record_type,
                "prio": prio,
                "content": content,
                "ttl": ttl}
        r = self._post(url, payload)
        return r.json()

    def _get(self, url):
        r = requests.get(url, headers = self.common_headers)
        r.raise_for_status()
        return r

    def _post(self, url, payload):
        r = requests.post(url, data = json.dumps(payload),
                headers = self.common_headers)
        r.raise_for_status()
        return r
