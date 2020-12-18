from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField#imported fields that leter get rendered in my HTML files that have imput fields
from wtforms.validators import DataRequired, Length, Email, ValidationError#imports various validators so that they don't need to be coded from scratch
from flask_wtf import Form, RecaptchaField, Recaptcha #needed to be able to insert a recaptcha field and validate it
from wtforms import BooleanField as WTBool
from email_validator import validate_email
#Defines forms that are use on the website and this file gets imported in browebgen_backend.py to get these forms
import re#allows to read regular expression for email validation in the russian version of the form

class contact_form(FlaskForm):

    recaptcha = RecaptchaField(validators=[Recaptcha(message="Please verify that you're not a robot")])#Displays the message specified instead of a defoult one

    name = StringField("Name", validators=[DataRequired(),#"Name" is used as a label and bassed to html using jinja
                                 Length(min=3, max=10)])#sets length for the data input
    email = StringField("Email",
                        validators=[DataRequired(), Email()])#Email() validator check if data imputed follows email standard
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=20, max=200)])

    privacy_pol_checkbox = BooleanField("I Agree to Privacy Policy", validators=[DataRequired()])
    
    submit = SubmitField("Send the message")
        

class contact_form_ru(FlaskForm):#using different form for the russian version of the page to be able to translate the rror messages

    recaptcha = RecaptchaField(validators=[Recaptcha(message="Подтвердите что вы не робот.")])#Displays the message specified instead of a defoult one

    name = StringField("Name")
    email = StringField("Email")
    message = TextAreaField("Message")
    submit = SubmitField("Отправить")
    privacy_pol_checkbox = BooleanField("I Agree to Privacy Policy")

    def validate_name(self, name):#using custom validator to have the error message in russian when field is empty 
        if not name.data:
            self.name.errors += (ValidationError("Это поле обязательно."),)#self.name.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 
        elif len(name.data) < 3:
             self.name.errors += (ValidationError("В поле должно быть между 3 и 10 букв."),)#self.name.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 
        elif len(name.data) > 10:
            self.name.errors += (ValidationError("В поле должно быть между 3 и 10 букв."),)#self.name.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 

    def validate_email(self, email):#using custom validator to have the error message in russian when field is empty 
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not email.data:
            self.email.errors += (ValidationError("Это поле обязательно."),)#self.email.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 
        elif not (re.search(regex,email.data)):
            self.email.errors += (ValidationError("Неверный формат почты."),)
 
    def validate_message(self, message):#using custom validator to have the error message in russian when field is empty 
        if not message.data:
            self.message.errors += (ValidationError("Это поле обязательно."),)#self.message.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 
        elif len(message.data) < 20:
             self.message.errors += (ValidationError("В поле должно быть между 20 и 200 букв."),)#self.message.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 
        elif len(message.data) > 200:
            self.message.errors += (ValidationError("В поле должно быть между 20 и 200 букв."),)#self.message.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 

    def validate_privacy_pol_checkbox(self, privacy_pol_checkbox):#using custom validator to have the error message in russian when field is empty 
        if not privacy_pol_checkbox.data:
            self.privacy_pol_checkbox.errors += (ValidationError("Отметьте это поле если хотите продолжить."),)#self.message.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 


class testimonial(FlaskForm):

    name = StringField("Name", validators=[DataRequired(),
                                 Length(min=3, max=10)])

    testimonial = StringField("Testimonial", validators=[DataRequired(), 
                                Length(min=6, max=150)])

    submit = SubmitField("Post testimonial")

    recaptcha = RecaptchaField(validators=[Recaptcha(message="Please verify that you're not a robot")])

class testimonial_ru(FlaskForm):

    name = StringField("Name")

    testimonial = StringField("Testimonial")

    submit = SubmitField("Отправить")

    recaptcha = RecaptchaField(validators=[Recaptcha(message="Подтвердите что вы не робот.")])

    def validate_name(self, name):#using custom validator to have the error message in russian when field is empty 
        if not name.data:
            self.name.errors += (ValidationError("Это поле обязательно."),)#self.name.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 
        elif len(name.data) < 3:
             self.name.errors += (ValidationError("В поле должно быть между 3 и 10 букв."),)#self.name.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 
        elif len(name.data) > 10:
            self.name.errors += (ValidationError("В поле должно быть между 3 и 10 букв."),)#self.name.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 

    def validate_testimonial(self, testimonial):#using custom validator to have the error message in russian when field is empty 
        if not testimonial.data:
            self.testimonial.errors += (ValidationError("Это поле обязательно."),)#self.testimonial.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 
        elif len(testimonial.data) < 6:
             self.testimonial.errors += (ValidationError("В поле должно быть между 6 и 150 букв."),)#self.testimonial.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 
        elif len(testimonial.data) > 150:
            self.testimonial.errors += (ValidationError("В поле должно быть между 6 и 150 букв."),)#self.testimonial.errors is tuple of Validation errors. It creates tuple from single ValidationError and adds it to your errors 