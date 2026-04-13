import chilkat, os, dotenv

from flask import Flask, render_template, request

app = Flask(__name__)
dotenv.load_dotenv()
apppass = os.environ.get("GMAIL_APP_PASS")
if (not apppass):
    raise RuntimeError("API key not found, check environment!")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")

@app.route("/members")
def members():
    return render_template("members.html")

@app.route("/contact", methods=["POST"])
def send_email():
    user_email = request.form.get("email", "")
    body = request.form.get("comments", "")
    if not user_email or not body:
        return "Invalid input for form submission."

    mailman = chilkat.CkMailMan()
    mailman.put_SmtpHost("smtp.gmail.com")
    mailman.put_SmtpPort(587)
    mailman.put_StartTLS(True)
    mailman.put_SmtpUsername("upliftcompany13@gmail.com")
    
    mailman.put_SmtpPassword(apppass)
    internal_email = chilkat.CkEmail()
    internal_email.put_Subject("Automated Contact Submission From " + user_email)
    internal_email.put_Body(body)
    internal_email.put_From("Uplift Contact Submission")
    internal_email.put_ReplyTo("")
    internal_email.AddTo("Uplift Contact", "upliftcompany13@gmail.com")
    
    thanks_email = chilkat.CkEmail()
    thanks_email.put_Subject("Thanks For Your Submission!")
    thanks_email.put_Body("We are glad that you have taken the time to get in touch with us. Your input is appreciated!")
    thanks_email.put_From("Uplift Inc.")
    thanks_email.put_ReplyTo("")
    thanks_email.AddTo("", user_email)

    success = mailman.SendEmail(internal_email) and mailman.SendEmail(thanks_email)
    if (success == False):
        print(mailman.lastErrorText())
        return "Email failed to send", 500
    return "Email sent successfully"