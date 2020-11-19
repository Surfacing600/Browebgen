from flask import Flask, render_template, request, redirect, flash, url_for
from flask_wtf import Form, RecaptchaField
from flask_sqlalchemy import SQLAlchemy
from forms import contact_form, testimonial#imported forms from the "forms" file in the same directory as this file
from wtforms.validators import DataRequired, Length, Email
from datetime import datetime#used in testimonial db to sort them by date and time submitted
import smtplib#for email to work
from email.message import EmailMessage#for email to work
from email.mime.text import MIMEText#to be able to send HTML formatted email
import os#to be able to use environmental variables for extra security

app = Flask(__name__)# instentiates Flask app
app.secret_key = "secret"# because "flash" uses cookies you have to use the secret key so that cookies are incripted and 
# an error doesn't get thrown
app.config['SECRET_KEY'] = "1859956eb4f0c6adf72c10cab1f3445f"#the secret key needed to be set because 
#anything that requires encryption (for safe-keeping against tampering by attackers) requires the secret
#key to be set. The secret plus the data-to-sign are used to create a signature string, a hard-to-recreate 
#value using a cryptographic hashing algorithm; only if you have the exact same secret and the original data 
#can you recreate this value, letting Flask detect if anything has been altered without permission.


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # doesn't change anything just makes a warning message go away
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///my_form_database.db'# IMPORTANT: Defines location of the database, SQLlite
 # is easier to get working than other file connection URI formats, no additional libraries are required, not tricky to get working on different computers
app.config["RECAPTCHA_PUBLIC_KEY"] = "6LdjN9gZAAAAAELZcLuhEW3g4UXhxAYwjT0iL1Uw"#the key taken from my Google reCapcha account
app.config["RECAPTCHA_PRIVATE_KEY"] = "6LdjN9gZAAAAACu-ZLZDHxjhjGZwr1vTLnol5Z_z"#the key taken from my Google reCapcha account
app.config['TESTING'] = False# FOR TESTING: if you put the value "True" the form will get submitted without recaptcha solved

db = SQLAlchemy(app)# instentiates the database


class form_database(db.Model):# table model or table with the name "form_database", this class represents a table in the database, class inherits from db.Model
    # !!when you added new column you need to create a new database file to be able to see the change!!
    id = db.Column(db.Integer, primary_key=True)# every time you deal with databases you always want an id 
    # to keep track of the entries into your database, id for each entry will be unique it makes filtering
    #possible if you have two e.g.  Adams in the database it helps to specify which of them you want to delete
    # "db.Integer specifies which data type will be handled by this column and id is "primary_key", that's why it equals "True""
    name = db.Column(db.String(50), nullable=False)#specifies a name column
    email = db.Column(db.String(50), nullable=False)#specifies an email column
    message = db.Column(db.String(200), nullable=False)#specifies a message column

class testimonial_database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    testimonial = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default= datetime.now)




@app.route('/main_page', methods=["GET", "POST"]) 

def form():

    form = contact_form()#make one of the forms in the "forms" file an object to be used below
    
    if request.method == "POST" and "translate" in request.form:#checks the method and whether the 
        #passed value is translate upon clicking a button to translate the web page
        operation = request.form["operation"]
        if operation == "russian":#if option's value in the HTML file is "russian"
            language1 = "russian"
            return render_template("/Pages/Main page/main_page.html", a=language1, form=form)#"a" variable used for jinja to react 
            #on the function to choose russian version of HTML
      
        elif operation == "english":#if option's value in the HTML file is "english"
            language2 = "english"
            return render_template("/Pages/Main page/main_page.html", b=language2, form=form)#"b" variable used for jinja to react 
            #on the function to choose english version of HTML

    if form.validate_on_submit():#will tell me if the form was validated when it was submitted
        flash("Your message has been sent successfully. I'll be in touch shortly.")#the message to notify the user of a successfull submition of the form
        new_data = form_database(name=form.name.data, email=form.email.data, message=form.message.data)#grabs user input from the form and prepares it for the database push
     

        MY_EMAIL = os.environ.get('MY_EMAIL')#gets my email from the environmental variable
        MY_EMAIL_PASSWORD = os.environ.get('MY_EMAIL_PASSWORD')#gets the password to my email from the environmental variable
        
        message_for_me = EmailMessage()#It is the base class for the email object model. EmailMessage provides 
        #the core functionality for setting and querying header fields, for accessing message bodies, and for 
        # creating or modifying structured messages.
        message_for_me = f"<b>Client name:</b> {form.name.data}<br></br> <b>Email:</b> {form.email.data} <br></br> <b>Message:</b> {form.message.data}"#an email content formatted in "f" string which uses the data a user inputed in the form
        msg_for_me = MIMEText( message_for_me, "html")#allows to use HTML in the "f" string above
        msg_for_me['Subject'] = "New form submitted"#email subject
        msg_for_me['From'] = MY_EMAIL#uses one of my emails to send this email from to my email below
        msg_for_me['To'] = "svistoplaskino@hotmail.com"

        message_for_customer = EmailMessage()
        message_for_customer = f"<p>Dear {form.name.data},<br></br> Thank you for expressing your interest in browebgen web services. I will be in touch with you in the next 24 hours.<br></br> Yours sincerely, <br></br> Dmitry </p>"
        msg_for_customer = MIMEText(message_for_customer, "html")
        msg_for_customer['Subject'] = "Thank you from Browebgen"
        msg_for_customer['From'] = MY_EMAIL
        msg_for_customer['To'] = form.email.data
            
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:#An SMTP instance encapsulates an SMTP connection. It has methods that support a full repertoire of SMTP and ESMTP operations.'smtp.gmail.com' is Gmail server (use this because email is sent from a gmail email address) and 465 is corresponding port
            smtp.login(MY_EMAIL, MY_EMAIL_PASSWORD)#logs in to my gmail using its password
            smtp.send_message(msg_for_me)#sends an email with the form data to me once a new form has been submitted
            smtp.send_message(msg_for_customer)#sends an email to the customer adressing them by the name they specified in the form with an HTML formatted email above
        try:
            db.session.add(new_data)#adds new data from the form to the database
            db.session.commit()#comitts this data to the database 
            return redirect('/main_page')
        except:
            return redirect('/main_page')#redirects to the same page if something went wrong
    return render_template("/Pages/Main page/main_page.html", form=form)#renders the template at first access to the page and displays the form on the page




@app.route('/blog')#needed for the page to get loaded

def blog():
    return render_template("/Pages/Blog/blog.html")



@app.route('/about_me')#needed for the page to get loaded

def about_me():
    return render_template("/Pages/About me/about_me_page.html")



@app.route('/my_projects', methods=["GET", "POST"])

def testimonials():

#"form" and "testimonials" need to be defined before both if statements below as both are used for rendering of the page
#it is important so that the testimonials are visible when either a form is submitted or page translated
#if also prevents the form valiadion messages to be displayed when the web page gets translated
    form = testimonial()
    testimonials = testimonial_database.query.order_by(testimonial_database.date_created)#orders testimonials by 
    #date before being displayed on the screen
    if request.method == "POST" and "translate" in request.form:#this "if" statement has to be here
        operation = request.form["operation"]
        if operation == "russian":
            language1 = "russian"
            return render_template("/Pages/My projects/my_projects.html", a=language1, form=form, testimonials=testimonials)
    
        elif operation == "english":
            language2 = "english"
            return render_template("/Pages/My projects/my_projects.html", b=language2, form=form, testimonials=testimonials)#displays form AND name and testimonial on the page after rendering
    if form.validate_on_submit():#will tell me if the form was walidated when it was submitted
        flash("Your message has been sent successfully. I'll be in touch shortly.")
        new_testimonial = testimonial_database(name=form.name.data, testimonial=form.testimonial.data)
     

        MY_EMAIL = os.environ.get('MY_EMAIL')
        MY_EMAIL_PASSWORD = os.environ.get('MY_EMAIL_PASSWORD')
        
        message_for_me = EmailMessage()
        message_for_me = f"<b>Client name:</b> {form.name.data} <br></br> <b>Testimonial:</b> {form.testimonial.data} "
        msg_for_me = MIMEText( message_for_me, "html")
        msg_for_me['Subject'] = "New form submitted"
        msg_for_me['From'] = MY_EMAIL
        msg_for_me['To'] = "svistoplaskino@hotmail.com"
            
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(MY_EMAIL, MY_EMAIL_PASSWORD)
            smtp.send_message(msg_for_me)
        try:
            db.session.add(new_testimonial)
            db.session.commit()
            return redirect('/my_projects')#redirects to "my_projects" page
        except:#if there is an error it just loads the page again
            return redirect('/my_projects')
    return render_template("/Pages/My projects/my_projects.html", form=form, testimonials=testimonials)#displays form AND name and testimonial on the page after rendering



@app.route('/blog1')#needed for the page to get loaded

def blog1():
    return render_template("/Pages/Blog/blog1/blog1.html")


@app.route('/home_page')#needed for the page to get loaded

def index():
    return render_template("/index.html")


def my_projects_ru():
    return render_template("/Pages/My projects/my_projects-ru.html")#needed for the page to get loaded

if __name__ == '__main__': #The statement is saying: Is this file being run directly 
#by python or is it being imported? Python assigns the name "__main__" to the script 
# when the script is executed. If the script is imported from another script, the 
# script keeps it given name (e.g. hello.py). In our case we are executing the script. 
# Therefore, __name__ will be equal to "__main__". That means the if conditional 
# statement is satisfied and the app.run() method will be executed. This technique 
# allows the programmer to have control over script’s behavior.

    app.run(debug=True)#Notice also that we are setting the debug parameter to true. That will print out 
    #possible Python errors on the web page helping us trace the errors. However, in a production environment, 
    # you would want to set it to False as to avoid any security issues.