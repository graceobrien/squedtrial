from google.appengine.api import urlfetch
from google.appengine.api import users
import webapp2
import jinja2
from google.appengine.ext import ndb
import datetime

env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))

class User(ndb.Model):
    user_property = ndb.UserProperty()
    firstname = ndb.TextProperty()
    lastname = ndb.TextProperty()
    school = ndb.TextProperty()
    age = ndb.TextProperty()
    subject = ndb.StringProperty()
    latlng = ndb.GeoPtProperty()
    profile = ndb.BlobProperty()

class Message(ndb.Model):
    content = ndb.TextProperty()
    user = ndb.KeyProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
         user =users.get_current_user()
         template_var = {}
         if user is None:
             login_url = users.create_login_url('/userinfo')
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

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('profile.html')
        self.response.write(template.render())

class MessagesHandler(webapp2.RequestHandler):
    def get(self):
        post = Message.query(Message.user == ndb.Key(User, users.get_current_user().user_id())).fetch()
        variables = {'posts': post}
        template = env.get_template('messages.html')
        self.response.write(template.render(variables))

    def post(self):
        content = self.request.get('content')
        post = Message(content = content,
                        user = ndb.Key(User, users.get_current_user().user_id()))
        post.put()
        return self.redirect('/message')
class PostHandler(webapp2.RequestHandler):
    def get(self):
        urlsafe_post_key = self.request.get('key')
        post_key = ndb.Key(urlsafe = urlsafe_post_key)
        post = post_key.get()
        template = env.get_template('messages.html')
        variables = {'post': post}
        self.response.write(template.render(variables))
    def post(self):
        urlsafe_post_key = self.request.get('post_key')
        content = self.request.get('content')
        post_key = ndb.Key(urlsafe = urlsafe_post_key)
        return self.redirect('/message?key=%s' & urlsafe_post_key)

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

class UserInfoHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('userinfo.html')
        self.response.write(template.render())

    def post(self):
        firstname = self.request.get("firstname")
        lastname = self.request.get("lastname")
        school = self.request.get("school")
        age = self.request.get("age")
        profile = self.request.get("profile")
        
app = webapp2.WSGIApplication([
    ('/home', MainHandler),
    ('/profile', ProfileHandler),
    ('/map', MapHandler),
    ('/message', MessagesHandler),
    ('/post', PostHandler),
    ('/login', LoginHandler),
    ('/signup', SignUpHandler),
    ('/userinfo', UserInfoHandler)
], debug=True)
