from wtforms import Form, StringField, TextAreaField, PasswordField,SubmitField,validators, ValidationError
from wtforms.validators import DataRequired, Email
import email_validator
from flask_wtf.file import FileRequired,FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Register, ContactInfo
from shop.products.forms import Addproducts
from shop.admin.models import DiscountGenerator

class CustomerRegisterForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message=' Both password must match! ')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])

    submit = SubmitField('Register')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")

class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired()])

class contactForm(FlaskForm):
    name = StringField('Name: ', render_kw={"placeholder": "Enter your name"}, validators=[DataRequired()])
    email = StringField('Email: ', render_kw={"placeholder": "Enter your email"}, validators=[DataRequired(), Email(granular_message=True)])
    message = TextAreaField('Your Message: ', render_kw={"placeholder": "Enter your message"}, validators=[validators.length(max=200), DataRequired() ])
    submit = SubmitField('ContactInfo')

   
   
