#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email.Header import Header
from dozens_ip_updater.config import Config


class SimpleMail():

    fromAddress = Config.FROM_ADDRESS
    smtpServer = Config.SMTP
    mailAccount = Config.MAIL_ACCOUNT
    mailPass = Config.MAIL_PWD

    @classmethod
    def post(cls, toAddress, subject, body):
        fromAddress = cls.fromAddress
        msg = cls.create_message(fromAddress, toAddress, subject, body)
        cls.send_massage(fromAddress, toAddress, msg)

    @classmethod
    def create_message(cls, fromAddress, toAddress, subject, body):
        enc = 'utf-8'
        msg = MIMEText(body, 'plain', enc)
        msg['From'] = fromAddress
        msg['To'] = toAddress
        msg['Subject'] = Header(subject, enc)
        msg['Date'] = formatdate()
        return msg

    @classmethod
    def send_massage(cls, fromAddress, toAddress, msg):
        try:
            s = None
            s = smtplib.SMTP(cls.smtpServer, 587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(cls.mailAccount, cls.mailPass)
            s.sendmail(fromAddress, [toAddress], msg.as_string())
        except smtplib.SMTPException:
            raise
        except smtplib.socket.error:
            raise
        except Exception:
            raise
        finally:
            if s is not None:
                s.close()
