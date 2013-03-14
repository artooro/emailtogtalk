from google.appengine.ext import ndb

class Subscriber(ndb.Model):
    user = ndb.UserProperty()
    address = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)