

from flask import Flask, request, redirect, render_template, url_for, flash, get_flashed_messages
import requests, json


app = Flask(__name__)

# Secret for message flashing

app.secret_key = '6LdjN9gZAAAAACu-ZLZDHxjhjGZwr1vTLnol5Z_z'


@app.route("/", methods=["GET", "POST"])
def home():
  
    return redirect(url_for("contact"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
  
    
    sitekey = "6LdjN9gZAAAAAELZcLuhEW3g4UXhxAYwjT0iL1Uw"

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        msg = request.form['message']
        captcha_response = request.form['g-recaptcha-response']
        
        if is_human(captcha_response):
            # Process request here
            status = "Detail submitted successfully."
        else:
             # Log invalid attempts
            status = "Sorry ! Bots are not allowed."

        flash(status)
        return redirect(url_for('contact'))

    return render_template("abc.html", sitekey=sitekey)
                

                
def is_human(captcha_response):
  
    secret = "6LdjN9gZAAAAACu-ZLZDHxjhjGZwr1vTLnol5Z_z"
    payload = {'response':captcha_response, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


if __name__ == '__main__':
    app.run()