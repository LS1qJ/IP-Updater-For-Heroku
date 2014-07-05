#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apscheduler.scheduler import Scheduler
import logging
import traceback
from dozens_ip_updater.ip_updater import IPUpdater
from dozens_ip_updater.config import Config
from mail.simple_mail import SimpleMail


logging.basicConfig()


def scheduled_job():
    try:
        iu = IPUpdater()
        results = iu.main()
        for r in results:
            print r[1]
    except Exception, e:
        if Config().SEND_MAIL:
            sub = 'Error on IP-Updater worker.py'
            mailaddr = Config.TO_ADDRESS
            msg = traceback.format_exc()
            SimpleMail.post(mailaddr, sub, msg)
            print "Error Occurs. Send E-mail." + str(e)
        else:
            raise

sched = Scheduler(standalone=True, coalesce=True)
sched.add_cron_job(scheduled_job, minute=Config.CRON)
sched.start()
