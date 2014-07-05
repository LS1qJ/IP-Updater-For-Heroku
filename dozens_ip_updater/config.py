#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class Config(object):

    #Cron Schedule
    CRON = '0-59/20'  # kick the job once per 20 minutes

    #Dozens settings
    DOZENS_ID = "your-dozens-id"
    DOZENS_APIKEY = "your-dozens-APIKEY"
    DEFAULT_TTL = 7200

    #Your custom domain settings. You can add multiple custom domains.
    APPHOSTS = [{"custom_domain":"your-custom-domain",
                    "heroku_host":"yourapp.herokuapp.com"}]

    #Memcach settings
    USEMEMCACHED = True
    CACHE_KEY_PREFIX = "dozens_a_record"


    #Error Mail Setting
    SEND_MAIL = False
    FROM_ADDRESS = 'xxxx@foo.com'
    TO_ADDRESS = 'xxxxx@coo.com'
    SMTP = 'smtp.gmail.com'
    MAIL_ACCOUNT = 'xxxxx@gmail.com'
    MAIL_PWD = 'xxxxx'

    #You do not need to modify these settings.
    #Env vars are privided by heroku when you add Memcashier addon.
    DEFAULT_MEMCACHED_SERVER = "127.0.0.1:11211"
    MEMCACHED_SERVER = os.environ.get('MEMCACHIER_SERVERS')
    MEMCACHED_USERNAME = os.environ.get('MEMCACHIER_USERNAME')
    MEMCACHED_PASSWORD = os.environ.get('MEMCACHIER_PASSWORD')

    #When you run this program local and the env vars are not given.
    #DEFAULT_MEMCACHED_SERVER gonna be used
    if os.environ.get('MEMCACHIER_SERVERS') is None:
        MEMCACHED_SERVER = DEFAULT_MEMCACHED_SERVER
