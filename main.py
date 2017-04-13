#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import cgi
# importing a model for database
from google.appengine.ext import db

#setting up jinja

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)
class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.write(*a,**kw)

    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))


class Blog(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add= True)
def get_posts(self,limit,offset):
    post = db.GqlQuery("select * from Blog order by created desc limit (limit) offset")
    return post


class MainHandler(Handler):
    def render_index(self):
        blogs = db.GqlQuery("select * from Blog order by created desc limit 5")
        self.render("listing.html",blogs=blogs)
    def get(self):
        self.render_index()
class PostBlog(Handler):
    def render_index(self,title="",body="",error=""):
        self.render("newpost.html",title = title,body = body,error = error)
    def get(self):
        self.render_index()
    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")
        if title and body:
            a= Blog(title = title,body = body)
            a.put()

            self.redirect("/blog/"+str(a.key().id()))
        else:
            error = "we need both title and body."
            self.render_index(title,body,error)
class ViewPostHandler(Handler):
    def get(self,id):
        post = Blog.get_by_id(int(id))
        if post:
            self.render("viewpost.html",post=post)
        else:
            error = "The id not found."
            self.render("viewpost.html",error=error)

app = webapp2.WSGIApplication([
    ('/blog', MainHandler),
    ('/newpost', PostBlog),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
    ], debug=True)
