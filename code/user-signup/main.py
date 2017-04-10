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
import re
import cgi

form = """
<form method="post">
    <h1>User Signup</h1>
    <br>
    <label>
        Username
        <input type = "text", name = "username", value = "%(username_error)s"/>
        <div style = "color: red">%(username_error)s</div>
    </label>
    <br>
    <label>
        Password
        <input type="password" name="password" value="%(password_error)s"/>
        <div style = "color: red">%(password_error)s</div>
    </label>
    <br>
    <label>
        Verify Password
        <input type="password" name="confirmation" value="%(confirmation_error)s">
        <div style = "color: red">%(confirmation_error)s</div>
    </label>
    <br>
    <label>
        Email (optional)
        <input type = "text", name = "email", value = "%(email_error)s"/>
        <div style = "color: red">%(email_error)s</div>
    </label>
    <br>
    <input type = "submit"/>
</form>
"""
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def verify_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def verify_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or USER_EMAIL.match(email)

def escape(s):
    return cgi.escape(s, quote=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(form)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        confirmation = self.request.get("confirmation")
        email = self.request.get("email")

        if not verify_username(username):
            error="That is not a valid username!"
            self.response.out.write(form %{"username_error": error})

        if not verify_password(password):
            error="That is not a valid password!"
            self.response.out.write(form % {"password_error": error})

        if not password == confirmation:
            error="Your emails do not match."
            self.response.out.write(form % {"confirmation_error": error})

        if not valid_email(email):
            error="That is not a valid email."
            self.response.out.write(form % {"email_error":error})

        else:
            self.redirect("/welcome?username="+username)
        #redirect "/welcome+?username=" + username
class Welcome(webapp2.RequestHandler):
    def get(self):
# get username paramater
#print and use substitution top print welcome message
        username = self.request.get('username')
        self.response.out.write("Welcome, {0}" .format(username))

app = webapp2.WSGIApplication([
('/',MainPage),
('/welcome', Welcome)
], debug=True)
