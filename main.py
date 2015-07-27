
import webapp2
import jinja2
from google.appengine.ext import ndb

env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('home.html')
        self.response.write(template.render())

class BlurryProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('blurryprofile.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/home', MainHandler),
    ('/blurryprofile', BlurryProfileHandler),
], debug=True)
