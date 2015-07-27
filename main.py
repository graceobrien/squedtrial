from google.appengine.api import urlfetch
from google.appengine.api import users
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.api import users

env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))

class Database(ndb.Model):
    user = ndb.TextProperty()
    name = ndb.TextProperty()
    school = ndb.TextProperty()
    age = ndb.IntegerProperty()
    subject = ndb.StringProperty()
    location = ndb.GeoPtProperty()
    picture = ndb.BlobProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):

         template = env.get_template('home.html')
         self.response.write(template.render())


class BlurryProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('blurryprofile.html')
        self.response.write(template.render())


class MapHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('map.html')
        self.response.write(template.render())


class GmailHandler(webapp2.RequestHandler):
   def get(self):
       user = users.get_current_user()
       if user:
           greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                       (user.nickname(), users.create_logout_url('/home')))
       else:
           greeting = ('<a href="%s">Sign in or register</a>.' %
                       users.create_login_url('/map'))

       self.response.out.write("<html><body>%s</body></html>" % greeting)

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('login.html')
        self.response.write(template.render())

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('signup.html')
        self.response.write(template.render())



app = webapp2.WSGIApplication([
    ('/home', MainHandler),
    ('/profile', BlurryProfileHandler),
    ('/map', MapHandler),
    ('/gmail', GmailHandler),
    ('/login', LoginHandler),
    ('/signup', SignUpHandler)
], debug=True)
