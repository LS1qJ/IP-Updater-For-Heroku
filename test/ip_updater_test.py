# -*- coding: utf-8 -*-


import unittest
import sys
sys.path.append('.')

from dozens_ip_updater.ip_updater import IPUpdater
from dozens_ip_updater.mcache import MCache
from dozens_ip_updater.config import Config
from dozens_ip_updater.dozens_api import DozensApi


class TestIPUpdater(unittest.TestCase):

    def setUp(self):
        self.iu = IPUpdater()
        self.api = DozensApi
        self.mc = MCache(server = Config.MEMCACHED_SERVER,
                              username = Config.MEMCACHED_USERNAME,
                              password = Config.MEMCACHED_PASSWORD)
        self.mc.refresh()
        self.dummy_A_record_0 = {u'name': u'hoge.me',
                                u'prio': None,
                                u'content': u'168.0.0.1',
                                u'ttl': u'7200',
                                u'type': u'A',
                                u'id': u'1'}
        self.dummy_A_record_1 = {u'name': u'hoge.me',
                                u'prio': None,
                                u'content': u'168.0.0.2',
                                u'ttl': u'7200',
                                u'type': u'A',
                                u'id': u'2'}
        self.dummy_A_record_2 = {u'name': u'hoge.me',
                                u'prio': None,
                                u'content': u'168.0.0.2',
                                u'ttl': u'7200',
                                u'type': u'C',
                                u'id': u'3'}

    def test_001_extract_A_records(self):
        dummy_A_records = [self.dummy_A_record_0, self.dummy_A_record_1]
        with self.assertRaises(Exception):
            self.iu.extract_A_records(dummy_A_records)

    def test_002_extract_A_records(self):
        dummy_A_records = [self.dummy_A_record_2]
        res = self.iu.extract_A_records(dummy_A_records)
        self.assertIsNone(res)

    def test_003_extract_A_records(self):
        dummy_A_records = []
        res = self.iu.extract_A_records(dummy_A_records)
        self.assertIsNone(res)

    def test_004_extract_A_records(self):
        dummy_A_records = [self.dummy_A_record_0]
        res = self.iu.extract_A_records(dummy_A_records)
        self.assertEqual(res['content'],
                    self.dummy_A_record_0['content'])

    def test_004_get_dns_A_record(self):
        zone_name = "test.com"
        mc_key = Config.CACHE_KEY_PREFIX + zone_name
        self.mc.set(mc_key,
                    self.dummy_A_record_0,
                    Config.DEFAULT_TTL / 2)
        res = self.iu.get_dns_A_record(zone_name)
        self.assertEqual(res['content'],
                    self.dummy_A_record_0['content'])

    def test_005_get_dns_A_record(self):
        pass


if __name__ == '__main__':
    unittest.main()
