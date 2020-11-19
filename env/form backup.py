from flask import Flask, render_template, request, redirect, flash, url_for
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
from forms import contact_form
from wtforms.validators import DataRequired, Length, Email
import os

app = Flask(__name__)# instentiates Flask app
app.secret_key = "secret"# because "flash" uses cookies you have to use the secret key so that cookies are incripted and 
# an error doesn't get thrown
app.config['SECRET_KEY'] = "1859956eb4f0c6adf72c10cab1f3445f"#

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # doesn't change anything just makes a warning message go away
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///my_form_database.db'# IMPORTANT: Defines location of the database, SQLlite
 # is easier to get working than other file connection URI formats, no additional libraries are required, not tricky to get working on different computers
app.config["RECAPTCHA_PUBLIC_KEY"] = "6LdjN9gZAAAAAELZcLuhEW3g4UXhxAYwjT0iL1Uw"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6LdjN9gZAAAAACu-ZLZDHxjhjGZwr1vTLnol5Z_z"


db = SQLAlchemy(app)# instentiates the database

class form_database(db.Model):# table model or table with the name "form_database", this class represents a table in the database, class inherits from db.Model
    # !!when you added new column you need to create a new database file to be able to see the change!!
    
    id = db.Column(db.Integer, primary_key=True)# every time you deal with databases you always want an id 
    # to keep track of the entries into your database, id for each entry will be unique it makes filtering
    #possible if you have two e.g.  Adams in the database it helps to specify which of them you want to delete
    # "db.Integer specifies which data type will be handled by this column and id is "primary_key", that's why it equals "True""
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=False)

class testimonial_database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    testimonial = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default= datetime.now)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')



@app.route('/main_page', methods=["GET", "POST"]) 

def form_data():

    if request.method == "POST" and "translate" in request.form:
        operation = request.form["operation"]
        if operation == "russian":
            language1 = "russian"
            return render_template("/browebgen.com/Pages/Main page/main_page.html", a=language1)
      
        elif operation == "english":
            language2 = "english"
            return render_template("/browebgen.com/Pages/Main page/main_page.html", b=language2)

    if request.method == "POST" and "Send" in request.form:
    
        client_name = request.form["name"]
        client_email = request.form["email"]
        client_message = request.form["message"]

        #form validator
        if client_name == "":
            flash("Name field is required", 'empty_name') #'empty_name' defines the flash message category so that it can be filtered in the template
            return render_template("/browebgen.com/Pages/Main page/main_page.html")
        elif client_email == "":
            flash("Email field is required", 'empty_email')
            return render_template("/browebgen.com/Pages/Main page/main_page.html")
        elif client_message == "":
            flash("Message field is required", 'empty_message')
            return render_template("/browebgen.com/Pages/Main page/main_page.html")
        else:
            pass


        new_client_details = form_database(name=client_name, email=client_email, message=client_message)
       
        flash("Thank you for submitting the form. I'll be in touch soon.", "success")

        MY_EMAIL = os.environ.get('MY_EMAIL')
        MY_EMAIL_PASSWORD = os.environ.get('MY_EMAIL_PASSWORD')
        
        message_for_me = EmailMessage()
        message_for_me = f"<b>Client name:</b> {client_name}<br></br> <b>Email:</b> {client_email} <br></br> <b>Message:</b> {client_message}"
        msg_for_me = MIMEText( message_for_me, "html")
        msg_for_me['Subject'] = "New form submitted"
        msg_for_me['From'] = MY_EMAIL
        msg_for_me['To'] = "svistoplaskino@hotmail.com"

        message_for_customer = EmailMessage()
        message_for_customer = f"<p>Dear {client_name},<br></br> Thank you for expressing your interest in browebgen web services. I will be in touch with you in the next 24 hours.<br></br> Yours sincerely, <br></br> Dmitry </p>"
        msg_for_customer = MIMEText(message_for_customer, "html")
        msg_for_customer['Subject'] = "Thank you from Browebgen"
        msg_for_customer['From'] = MY_EMAIL
        msg_for_customer['To'] = client_email
            
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(MY_EMAIL, MY_EMAIL_PASSWORD)
            smtp.send_message(msg_for_me)
            smtp.send_message(msg_for_customer)
        try:
            db.session.add(new_client_details)
            db.session.commit()
            return redirect("/main_page")
        except:
            return redirect("/main_page")
    return render_template("/browebgen.com/Pages/Main page/main_page.html")


@app.route('/blog', methods=["GET", "POST"])

def contact_for():
    form = contact_form()
    if form.validate_on_submit():#will tell me if the form was walidated when it was submitted
        flash("Sent successfully")
        new_data = Data(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(new_data)
        db.session.commit()
    return render_template("/browebgen.com/Pages/Blog/blog.html", form=form)



@app.route('/about_me', methods=["GET", "POST"])

def about_me():
    return render_template("/browebgen.com/Pages/About me/about_me_page.html")


@app.route('/my_projects', methods=["GET", "POST"])

def testimonials():

    if request.method == "POST" and "translate" in request.form:
        operation = request.form["operation"]
        if operation == "russian":
            language1 = "russian"
            return render_template("/browebgen.com/Pages/My projects/my_projects.html", a=language1)
      
        elif operation == "english":
            language2 = "english"
            return render_template("/browebgen.com/Pages/My projects/my_projects.html", b=language2)

    if request.method == "POST" and "post" in request.form:
        
        customer_name = request.form["name"]# takes name from the form and puts it in this variable
        customer_testimonial = request.form["testimonial"]

        if customer_name == "":
            flash("Name field is required", 'empty_name')
            return render_template("/browebgen.com/Pages/My projects/my_projects.html", testimonial=customer_testimonial)
        elif customer_testimonial == "":
            flash("Testimonial field is required", 'empty_testimonial')
            return render_template("/browebgen.com/Pages/My projects/my_projects.html", testimonial=customer_testimonial)
        else:
            pass

        new_testimonial = testimonial_database(name=customer_name, testimonial=customer_testimonial)# once we have it in the variable we ask to add the name from the form to the "name" column in our database

        MY_EMAIL = os.environ.get('MY_EMAIL')
        MY_EMAIL_PASSWORD = os.environ.get('MY_EMAIL_PASSWORD')
        
        message_for_me = EmailMessage()
        message_for_me = f"<b>Customer name:</b> {customer_name}<br></br> <b>Testimonial:</b> {customer_testimonial}"
        msg_for_me = MIMEText( message_for_me, "html")
        msg_for_me['Subject'] = "New testimonial left"
        msg_for_me['From'] = MY_EMAIL
        msg_for_me['To'] = "svistoplaskino@hotmail.com"

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(MY_EMAIL, MY_EMAIL_PASSWORD)
            smtp.send_message(msg_for_me)
        
        try:
            db.session.add(new_testimonial)
            db.session.commit()
            return redirect("/my_projects")
        except:
            return "There was an error adding your testimonial"
    else:
        testimonials = testimonial_database.query.order_by(testimonial_database.date_created)#orders the list of testimonials by date
    return render_template("/browebgen.com/Pages/My projects/my_projects.html", testimonials=testimonials)


def my_projects_ru():
    return render_template("/browebgen.com/Pages/My projects/my_projects-ru.html")

@app.route('/blog1', methods=["GET", "POST"])

def blog1():
    return render_template("/browebgen.com/Pages/Blog/blog1/blog1.html")


@app.route('/home_page', methods=["GET", "POST"])

def index():
    return render_template("/browebgen.com/index.html")

@app.route('/my_projects-ru', methods=["GET", "POST"])

def testimonials_ru():
    if request.method == "POST":
        customer_name = request.form["name"]# takes name from the form and puts it in this variable
        customer_testimonial = request.form["testimonial"]

        if customer_name == "":
            flash("Name field is required", 'empty_name')
            return render_template("/browebgen.com/Pages/My projects/my_projects-ru.html")
        elif customer_testimonial == "":
            flash("Testimonial field is required", 'empty_testimonial')
            return render_template("/browebgen.com/Pages/My projects/my_projects-ru.html")
        else:
            pass

        new_testimonial = testimonial_database(name=customer_name, testimonial=customer_testimonial)# once we have it in the variable we ask to add the name from the form to the "name" column in our database

        MY_EMAIL = os.environ.get('MY_EMAIL')
        MY_EMAIL_PASSWORD = os.environ.get('MY_EMAIL_PASSWORD')
        
        message_for_me = EmailMessage()
        message_for_me = f"<b>Customer name:</b> {customer_name}<br></br> <b>Testimonial:</b> {customer_testimonial}"
        msg_for_me = MIMEText( message_for_me, "html")
        msg_for_me['Subject'] = "New testimonial left"
        msg_for_me['From'] = MY_EMAIL
        msg_for_me['To'] = "svistoplaskino@hotmail.com"

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(MY_EMAIL, MY_EMAIL_PASSWORD)
            smtp.send_message(msg_for_me)
        
        try:
            db.session.add(new_testimonial)
            db.session.commit()
            return redirect("/my_projects-ru")
        except:
            return "There was an error adding your testimonial"
    else:
        testimonials = testimonial_database.query.order_by(testimonial_database.date_created)#orders the list of testimonials by date
    return render_template("/browebgen.com/Pages/My projects/my_projects-ru.html", testimonials=testimonials)


def my_projects_ru():
    return render_template("/browebgen.com/Pages/My projects/my_projects-ru.html")

if __name__ == '__main__':
    app.run(debug=True)