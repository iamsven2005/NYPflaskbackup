from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms.fields import EmailField

class Addproducts(Form):
    name = StringField('Name:', [validators.DataRequired()], render_kw={'placeholder':'Enter product name'})
    price = FloatField('Price:', [validators.DataRequired()], render_kw={'placeholder': 'Enter Price'})
    discount = IntegerField('Discount:',[validators.DataRequired()] ,default=0)
    stock = IntegerField('Units in Stock:', [validators.DataRequired()], render_kw={'placeholder': 'Enter Stock'})
    description = TextAreaField('Description:', [validators.DataRequired()], render_kw={'placeholder': 'Enter Description'})
    expenses = FloatField('Expenses:', [validators.DataRequired()], render_kw={"placeholder": 'Enter expenses'})

    addstock = IntegerField('Amount to add:', [validators.DataRequired()])

    brand = StringField('Brand Name: ', [validators.DataRequired()], render_kw={'placeholder': "Enter brand name"})
    category = StringField('Category: ', [validators.DataRequired()], render_kw={'placeholder': 'Enter Category'})
    discount = StringField('Discount: ',[validators.Optional()], render_kw={"placeholder": "Enter discount code"})

class ship(Form):
    first_name = StringField('First Name: ',[validators.DataRequired()], render_kw={'placeholder': 'John'})
    last_name = StringField('Last Name: ',[validators.DataRequired()], render_kw={'placeholder': 'Lee'})
    company = StringField('Company (optional)', [validators.Optional()], render_kw={'placeholder': 'SGMART PTE LTD'})
    address = StringField('Address', [validators.DataRequired()], render_kw={'placeholder': '542 W.15th Street'})
    unit_number = StringField('Unit Number', [validators.DataRequired()], render_kw={'placeholder': '#03-1234'})
    postal_code = IntegerField('Postal Code',[validators.DataRequired(message='Invalid Postal Code'), validators.NumberRange(min=100000, max=999999, message='Invalid Postal code')], render_kw={'placeholder': '123456'})
    phone = IntegerField('Phone Number', [validators.DataRequired(message='Invalid Phone Number'), validators.NumberRange(min=10000000, max=99999999, message='Invalid Number')], render_kw={'placeholder': '91234567'})
    email = EmailField('Email', [validators.DataRequired()], render_kw={'placeholder': 'Email'})