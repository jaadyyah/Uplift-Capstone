import os, sqlite3, json, requests

from flask import Flask, g, render_template, request

app = Flask(__name__)

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("Uplift.db")
    return g.db

def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

app.teardown_appcontext(close_db)

def addToUsers(Email, FName, LName, PhoneNumber):
    db = get_db()
    db.execute("""
    insert or ignore into Users (Email, FName, LName, PhoneNumber)
        values
        (?, ?, ?, ?)
    """, (Email, FName, LName, PhoneNumber))
    db.commit()

def addToReplies(Email, Data):
    db = get_db()
    db.execute("""
    insert into Replies (Email, Data)
        values
        (?, ?)
    """, (Email, Data))
    db.commit()

def setUserEmailAsInvalid(Email, PermanentlyInvalid):
    db = get_db()
    cursor = db.execute("""
    update Users
        set ValidEmail = 0, PermanentlyInvalid = ?
    where email = ?
    """, (PermanentlyInvalid, Email))
    if cursor.rowcount <= 0:
        print(f"No user found for email {Email}")
    db.commit()


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
    name = request.form.get("name", "").split(" ")
    fname = name[0]
    lname = name[1] if len(name) > 1 else ""
    phone = request.form.get("phone", "")
    user_email = request.form.get("email", "")
    body = request.form.get("comments", "")
    if not user_email or not body:
        return "Invalid input for form submission."
    try:
        addToUsers(user_email, fname, lname, phone)
        addToReplies(user_email, body)
    except Exception as exception:
        print(exception)
        return "Form not implemented."
    return render_template("index.html") # After filling out the form, the return value generates an html page.


@app.route("/ses-bounce-events", methods=["POST"])
def ses_events():
    payload = request.get_json(force=True)

    # 1. SNS subscription confirmation
    if payload.get("Type") == "SubscriptionConfirmation":
        subscribe_url = payload.get("SubscribeURL")
        if subscribe_url:
            requests.get(subscribe_url)  # confirm subscription
        return "confirmed", 200

    # 2. Actual notification
    if payload.get("Type") == "Notification":
        message = json.loads(payload.get("Message", "{}"))

        event_type = message.get("notificationType")

        if event_type == "Bounce":
            bounce = message.get("bounce", {})
            bounceType = bounce.get("bounceType")
            recipients = bounce.get("bouncedRecipients", [])
            for r in recipients:
                email = r.get("emailAddress")
                if not email:
                    continue
                print("BOUNCE:", bounceType, email)
                if (bounceType == "Permanent"):
                    setUserEmailAsInvalid(email, 1)
                else:
                    setUserEmailAsInvalid(email, 0)

        elif event_type == "Complaint":
            complaint = message.get("complaint", {})
            recipients = complaint.get("complainedRecipients", [])
            for r in recipients:
                email = r.get("emailAddress")
                if not email:
                    continue
                print("COMPLAINT:", email)
                setUserEmailAsInvalid(email, 1)

                # : suppress email
    return "OK", 200