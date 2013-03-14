from flask import request, render_template

from google.appengine.api import users
from google.appengine.api import xmpp
from google.appengine.api import mail
from forms import StartForm
import model
import uuid

import logging


# Retrieve lost address
def retrieve():
    form = StartForm(request.values)
    if form.validate():
        user = users.User(form.email.data)
        q = model.Subscriber.query(model.Subscriber.user == user)
        if q.count() > 0:
            subscriber = q.get()

            mail.send_mail(sender="Email to Gtalk <info@emailtogtalk.appspotmail.com>",
                           to=form.email.data,
                           subject="Your Email to Gtalk Info",
                           body="Your gateway email address is %s@emailtogtalk.appspotmail.com" % subscriber.address)

    return "OK"



# Initiate a new user
def start():
    form = StartForm(request.values)
    if form.validate():
        user = users.User(form.email.data)
        q = model.Subscriber.query(model.Subscriber.user == user)
        if q.count() >= 1:
            return "EXISTS"

        subscriber = model.Subscriber()
        subscriber.user = user

        # Generate address
        address_uuid = uuid.uuid1()
        address = address_uuid.hex
        subscriber.address = address

        subscriber.put()

        # Send user invitation
        xmpp.send_invite(form.email.data)

        return '%s@emailtogtalk.appspotmail.com' % subscriber.address
    else:
        return "INVALID"
