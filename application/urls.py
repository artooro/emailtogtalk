from application import app
from application import views


app.add_url_rule('/app/subscribe', 'start', view_func=views.start)
app.add_url_rule('/app/retrieve', 'retrieve', view_func=views.retrieve)