import os, email_auto

from flask import Flask, render_template, request

app = Flask(__name__)

# @app.route(path) sets up a URL path that HTML can use for links/redirects within our site.
@app.route("/") # The path "/" in HTML code redirects to index.html, but the URL will show "/"
def home():
    return render_template("index.html") # Sets which HTML file is linked to via a function which returns the page. Same for all of the routes.

@app.route("/contact_us") # The path "/contact_us" in HTML code redirects to contact_us.html, but the URL will show "/contact_us"
def contact_us():
    return render_template("contact_us.html")

@app.route("/about_us") # The path "/about_us" in HTML code redirects to about_us.html, but the URL will show "/about_us"
def about_us():
    return render_template("about_us.html")

@app.route("/contact", methods=["POST"])        # The path "/contact" in HTML code does *NOT* redirect to an HTML page we wrote, 
def email_form():                               # but the URL will show "/contact".
    user_email = request.form.get("email", "")
    body = request.form.get("comments", "")
    if not user_email or not body:
        return "Invalid input for form submission."
    try:
        email_auto.send_email(user_email, body)
    except Exception as exception:
        print(exception)
        return "Form not implemented."
    return render_template("index.html") # After filling out the form, the return value generates an html page.


