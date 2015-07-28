from google.appengine.api import urlfetch
from google.appengine.api import users
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.api import users

env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))

class Database(ndb.Model):
    name = ndb.TextProperty()
    school = ndb.TextProperty()
    age = ndb.IntegerProperty()
    subject = ndb.StringProperty()
    location = ndb.GeoPtProperty()
    picture = ndb.BlobProperty()

class User(ndb.Model):
    user_property = ndb.UserProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
         user =users.get_current_user()
         template_var = {}
         if user is None:
             login_url = users.create_login_url('/map')
             template_var["login"] = login_url
         else:
             logout_url = users.create_logout_url('/home') #creates a logout url
             self.response.write('Welcome %s!' % user.email())
             self.response.write('<a href = "%s"> Log Out </a>' % logout_url)
             if len(User.query(User.user_property == user).fetch()) == 0:
                new_user = User(user_property = user)
                new_user.put()

         template = env.get_template('home.html')
         self.response.write(template.render(template_var))


class BlurryProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('blurryprofile.html')
        self.response.write(template.render())


class MapHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('map.html')
        self.response.write(template.render())

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('login.html')
        self.response.write(template.render())

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('signup.html')
        self.response.write(template.render())

class FacebookHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('facebook.html')
        self.response.write(template.render())



app = webapp2.WSGIApplication([
    ('/home', MainHandler),
    ('/profile', BlurryProfileHandler),
    ('/map', MapHandler),
    ('/login', LoginHandler),
    ('/signup', SignUpHandler),
    ('/facebook', FacebookHandler)
], debug=True)
