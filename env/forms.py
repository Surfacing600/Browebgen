from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField#imported fields that leter get rendered in my HTML files that have imput fields
from wtforms.validators import DataRequired, Length, Email#imports various validators so that they don't need to be coded from scratch
from flask_wtf import Form, RecaptchaField, Recaptcha #needed to be able to insert a recaptcha field and validate it

#Defines forms that are use on the website and this file gets imported in browebgen_backend.py to get these forms

class contact_form(FlaskForm):

    recaptcha = RecaptchaField(validators=[Recaptcha(message="Please verify that you're not a robot")])#Displays the message specified instead of a defoult one

    name = StringField("Name", validators=[DataRequired(),#"Name" is used as a lable and bassed to html using jinja
                                 Length(min=3, max=10)])#sets length for the data input
    email = StringField("Email",
                        validators=[DataRequired(), Email()])#Email() validator check if data imputed follows email standard
    message = StringField("Message", validators=[DataRequired(), Length(min=20, max=100)])

    submit = SubmitField("Submit")


class testimonial(FlaskForm):

    recaptcha = RecaptchaField()

    name = StringField("Name", validators=[DataRequired(),
                                 Length(min=3, max=10)])

    testimonial = StringField("Testimonial", validators=[DataRequired(), 
                                Length(min=6, max=50)])

    submit = SubmitField("Submit")

