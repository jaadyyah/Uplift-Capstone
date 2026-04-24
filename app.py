import os, sqlite3, json, requests, uplift_dbutil, uplift_emailutil, botocore

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

uplift_dbutil.init_db()

app.teardown_appcontext(uplift_dbutil.close_db)

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
        uplift_dbutil.addToUsers(user_email, fname, lname, phone)
        uplift_dbutil.addToReplies(user_email, body)
        uplift_emailutil.send_email(user_email, "Thanks from Uplift", "Thank you for reaching out to us! Your response has been recorded.")
    except Exception as exception:
        print(exception)
        return "There was an error loading the form." # Change this later and add flask route + redirect for error!
    return redirect(url_for("home")) # After filling out the form, the return value reroutes to home functions.


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
                    uplift_dbutil.setUserEmailAsInvalid(email, 1)
                else:
                    uplift_dbutil.setUserEmailAsInvalid(email, 0)

        elif event_type == "Complaint":
            complaint = message.get("complaint", {})
            recipients = complaint.get("complainedRecipients", [])
            for r in recipients:
                email = r.get("emailAddress")
                if not email:
                    continue
                print("COMPLAINT:", email)
                uplift_dbutil.setUserEmailAsInvalid(email, 1)

                # : suppress email
    return "OK", 200