from google.appengine.api import urlfetch
from google.appengine.api import users
import webapp2
import jinja2
import json
from google.appengine.ext import ndb
import datetime
import mimetypes

env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))

class User(ndb.Model):
    user_property = ndb.UserProperty()
    firstname = ndb.TextProperty()
    lastname = ndb.TextProperty()
    school = ndb.TextProperty()
    age = ndb.TextProperty()
    subject = ndb.StringProperty()
    latlng = ndb.GeoPtProperty()
    profile = ndb.BlobProperty(default=None)
    background = ndb.BlobProperty()
    bio = ndb.TextProperty()

class Message(ndb.Model):
   # post = ndb.KeyProperty(kind = User.user_property)
    content = ndb.TextProperty()
    user = ndb.KeyProperty()

    # class Redirect(webapp2.RequestHandler):
    #     def post(self):
    #         self.redirect('/home')

# class FormHandler(webapp.RequestHandler):
#   def post(self):
#     if processFormData(self.request):
#       self.redirect("http://squednetwork.appspot.com/home")

class MainHandler(webapp2.RequestHandler):
    def get(self):
         user =users.get_current_user()
         template_var = {}
         if user is None:
             login_url = users.create_login_url('/userinfo')
             template_var["login"] = login_url
         else:
             logout_url = users.create_logout_url('/home')
             self.response.write('Welcome %s!' % user.email())
             self.response.write('<a href = "%s"> Log Out </a>' % logout_url)
             if len(User.query(User.user_property == user).fetch()) == 0:
                new_user = User(user_property = user)
                new_user.put()

         template = env.get_template('home.html')
         self.response.write(template.render(template_var))

class UserInfoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user_info= User.query(User.user_property == user).get()

        if user_info:
            self.redirect(users.create_login_url('/profile?user=' + user_info.key.urlsafe()))
        else:
            template = env.get_template('userinfo.html')
            self.response.write(template.render())

    def post(self):
        firstname = self.request.get("firstname")
        lastname = self.request.get("lastname")
        school = self.request.get("school")
        age = self.request.get("age")
        profile = self.request.get("profile")
        bio = self.request.get("bio")

        user = users.get_current_user()

        user_entity = User.query(User.user_property == user).get()
        user_entity.firstname = firstname
        user_entity.lastname = lastname
        user_entity.school = school
        user_entity.age = age
        user_entity.bio = bio

        user_entity.put()

        self.redirect('/profile?user=' + user_entity.key.urlsafe())

# class ImageHandler(webapp2.RequestHandler):
#     def get(self):
#         key_id_urlsafe = self.request.get("user")
#         profile_key = ndb.Key(urlsafe = key_id_urlsafe)
#         profile = profile_key.get()
#
#         if profile and key_id_urlsafe:
#             self.response.headers['Content-Type'] = "image/jpegs"
#             self.response.out.write(profile.image)
#
#         else:
#             self.redirect('/static/noimage.jpg')

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('profile.html')
        user_entity_key_urlsafe = self.request.get('user')
        user_entity_key = ndb.Key(urlsafe = user_entity_key_urlsafe)
        user_entity = user_entity_key.get()

        variables = {'firstname': user_entity.firstname,
                     'lastname' : user_entity.lastname,
                     'age': user_entity.age,
                     'school': user_entity.school,
                     'bio': user_entity.bio}

        self.response.write(template.render(variables))
class MessagesHandler(webapp2.RequestHandler):
    def get(self):
        post = Message.query(Message.user == ndb.Key(User, users.get_current_user().user_id())).fetch()
        variables = {'posts': post}
        template = env.get_template('messages.html')
        self.response.write(template.render())

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
        userlocations = []
        for user in userlist :
            userloc = user.latlng
            userlocations.append(userloc)
        template = env.get_template('map.html')
        self.response.write(template.render(locationlist=userlocations))
        user = users.get_current_user()
        User.query(User.user_property == user).fetch()

class SaveLocHandler(webapp2.RequestHandler):
    def post (self):

                latitude = self.request.POST.get("latitude")
                longitude = self.request.POST.get("longitude")
                user = users.get_current_user()

                user_entity = User.query(User.user_property == user).get()
                if latitude is None:
                    user_entity.latlng = None
                else:
                    user_entity.latlng = ndb.GeoPt(latitude, longitude)

                user_entity.put()

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('login.html')
        self.response.write(template.render())

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('signup.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    # ('/', FormHandler),
    ('/home', MainHandler),
    ('/profile', ProfileHandler),
    ('/map', MapHandler),
    # ('/images', ImageHandler),
    ('/message', MessagesHandler),
    ('/post', PostHandler),
    ('/login', LoginHandler),
    ('/signup', SignUpHandler),
    ('/userinfo', UserInfoHandler),
    ('/saveloc', SaveLocHandler),
], debug=True)
