#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from config import Config
from dozens_api import DozensApi
from mcache import MCache


class IPUpdater(object):
    def __init__(self):
        """
        MCache is used to store the A record value of
        Dozens API Server.
        """
        if Config.USEMEMCACHED is True:
            self.mc = MCache(server = Config.MEMCACHED_SERVER,
                              username = Config.MEMCACHED_USERNAME,
                              password = Config.MEMCACHED_PASSWORD)
        else:
            self.mc = None
        self.api = DozensApi()

    def extract_A_records(self, records):
        """
        Extract A record from DNS records.
        The DNS records is exepected to DozensAPI json format.
        The count of A records must be 1 or 0.
        If the count is more than 2, Excexption is generated.
        When there is A record, this function will return the
        A record data as DozensAPI json format.
        When there is not A record, this function will return None.
        """
        a_records = []
        for record in records:
            if record["type"] == "A":
                a_records.append(record)

        #Check the results of Arecords
        if len(a_records) > 1:
            raise Exception()  # "A" record should be a one.
        elif a_records == []:  # No "A" records
            return None
        else:
            return a_records[0]

    def get_dns_A_record(self, zone_name):
        """
        Retrieve the A record data from DozensAPI server.
        If you set the config of MEMCACHED true, the A record value
        is may stored in memcached server.
        After checking the memcache server, if there is no data
        in memcached server, this function retrieve the A record data
        from DozensDNS server and store the result to memcached.
        """
        a_record = None

        a_record = self._get_cache(zone_name)  # check memcached server
        if a_record is not None:
            return a_record

        r = self.api.get_records(zone_name)  # Retrive A record from Dozens
        a_record = self.extract_A_records(r["record"])
        if a_record is not None:
            self._set_cache(zone_name, a_record)
        return a_record

    def update_A_record(self, heroku_host_ip, dns_a_record):
        """
        Update A record in Dozens DNS Server.
        Return the updated A record value as DozensAPI json form.
        """
        r = self.api.post_update_record(
                record_id = dns_a_record.get('id'),
                prio = dns_a_record.get('prio'),
                content = heroku_host_ip,
                ttl = dns_a_record.get('ttl'))
        dns_a_record = self.extract_A_records(r["record"])
        return dns_a_record

    def create_A_record(self, heroku_host_ip, domain, ttl):
        """
        Create A record in Dozens DNS Server.
        Return the updated A record value as DozensAPI json form.
        """
        r = self.api.post_create_record(
                domain = domain,
                name = None,
                record_type = "A",
                prio = None,
                content = heroku_host_ip,
                ttl = ttl)
        dns_a_record = self.extract_A_records(r["record"])
        return dns_a_record

    def get_heroku_host_ip(self, host):
        """
        Get IP Address by hostname.
        Hostname is expected to Heroku app name.
        eg)myApp.herokuapp.com
        """
        if "herokuapp.com" not in host:
            raise Exception()  # host must point to the default heroku domain
        ipaddr = socket.gethostbyname(host)
        return ipaddr

    def ip_update(self, custom_domain, heroku_host):
        """
        Update A records in DozensDNS Server.
        Check the current IP Address for heroku application.

        If the current IP is different from the A record's in DNS,
        this function update the A records in the DozensDNS server.

        If there is no A record in DozensDNS Server,
        this function will create new A record in the sever.

        If there is already A record in the DozensDNS server, this function
        will update its value.

        If there is already A record in the DozensDNS server and the
        A record's value is same as current IP, this function do nothing.
        """
        update_pattern = None
        resultmsg = "TargetHost:%s Result:" % custom_domain
        new_dns_a_record = None

        dns_a_record = self.get_dns_A_record(custom_domain)
        heroku_host_ip = self.get_heroku_host_ip(heroku_host)

        #Store A record to Dozens Server
        if dns_a_record is None:
            update_pattern = "Create"
            new_dns_a_record = self.create_A_record(heroku_host_ip,
                                  custom_domain, Config.DEFAULT_TTL)
        elif dns_a_record["content"] != heroku_host_ip:
            update_pattern = "Update"
            new_dns_a_record = self.update_A_record(heroku_host_ip,
                                    dns_a_record)
        elif dns_a_record["content"] == heroku_host_ip:
            update_pattern = "Already updated"
            new_dns_a_record = dns_a_record

        #Evaluate and cache the result
        if new_dns_a_record is not None:
            resultmsg += "Success.%s%s" % (update_pattern, new_dns_a_record)
            resultflg = True
            if update_pattern != "Alread updated":
                self._set_cache(custom_domain, new_dns_a_record)
        else:
            resultmsg += "Fail. %s." % update_pattern
            resultflg = False

        return (resultflg, resultmsg)

    def main(self):
        """
        Update A record's ip Address for all hosts in config.
        """
        results = []
        for t in Config.APPHOSTS:
            custom_domain = t["custom_domain"]
            heroku_host = t["heroku_host"]
            result = self.ip_update(custom_domain, heroku_host)
            results.append(result)
        return results

    def _get_cache(self, zone_name):
        if Config.USEMEMCACHED is False:
            return None
        mc_key = Config.CACHE_KEY_PREFIX + zone_name
        return self.mc.get(mc_key)

    def _set_cache(self, zone_name, a_record):
        if Config.USEMEMCACHED is False:
            return None
        mc_key = Config.CACHE_KEY_PREFIX + zone_name
        self.mc.set(mc_key, a_record, Config.DEFAULT_TTL / 2)

if __name__ == "__main__":
    iu = IPUpdater()
    results = iu.main()
    for r in results:
        print r[1]
