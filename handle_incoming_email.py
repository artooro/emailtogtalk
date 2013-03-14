from application import model

import webapp2
import re
import logging

from google.appengine.api import xmpp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        """

        :param mail_message:
        """
        logging.info("Received a message from: " + mail_message.sender)

        prog = re.compile('([\w\-\.+]+)@(\w[\w\-\.]+)')
        if 'X-Forwarded-To' in mail_message.original:
            logging.info('Using X-Forwarded-To')
            tostring = mail_message.original['X-Forwarded-To']
        else:
            if 'Delivered-To' in mail_message.original:
                logging.info('Using Delivered-To')
                tostring = mail_message.original['Delivered-To']
            else:
                logging.info('Fell back to To field')
                tostring = mail_message.to
        logging.info('Delivered to is %s' % tostring)

        for m in prog.finditer(tostring):
            logging.info('Address: ' + m.group(1))

            # get message body
            bodytext = u""
            plaintext_bodies = mail_message.bodies('text/plain')
            for content_type, body in plaintext_bodies:
                bodytext += body.decode()

            # Check if a subscriber exists with that address
            q = model.Subscriber.query(model.Subscriber.address == m.group(1))
            if q.count() == 1:
                subscriber = q.get()

                # Send XMPP message
                user_address = subscriber.user.email()
                chat_message_sent = False
                try:
                    subject = mail_message.subject
                except:
                    subject = 'No subject'
                msg = "From: %s\nSubject: %s\nBody: %s" % (mail_message.sender, subject, bodytext)
                status_code = xmpp.send_message(user_address, msg)
                chat_message_sent = (status_code == xmpp.NO_ERROR)

                if not chat_message_sent:
                    logging.warning("Was not able to send XMPP message")

app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)

