# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# # Define the User registration form
# # It augments the Flask-User RegisterForm with additional fields
# class MyRegisterForm(RegisterForm):
#     first_name = StringField('First name', validators=[
#         validators.DataRequired('First name is required')])
#     last_name = StringField('Last name', validators=[
#         validators.DataRequired('Last name is required')])


# Define the User profile form
class UserProfileForm(FlaskForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    submit = SubmitField('Save')
    
class Unit(db.Model):
	__tablename__ = "unit"
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), unique=True, index=True)
	items = db.relationship('Item', backref='unit', lazy=True)

	def __init__(self, name):
		self.name = name

class Item(db.Model):
	__tablename__ = "item"
	id = db.Column(db.Integer(), primary_key=True)
	unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
	name = db.Column(db.String(50), unique=True, index=True)
	description = db.Column(db.Text)
	supplys = db.relationship('Supply', backref='supply', lazy=True)

	def __init__(self, name, description):
		self.name = name
		self.description = description

class SupplyInfo(db.Model):
	__tablename__ = 'supply_info'
	id = db.Column(db.Integer(), primary_key=True)
	supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
	supply_id = db.Column(db.String(50), nullable=False, index=True)
	supplys = db.relationship('Supply', backref='supply_info', lazy=True)
	censuses = db.relationship('Census', backref='supply_info', lazy=True)

	def __init__(self, supply_id):
		self.supply_id = supply_id

class Supply(db.Model):
	__tablename__ = "supply"
	id = db.Column(db.Integer(), primary_key=True)
	item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
	supply_info_id = db.Column(db.Integer, db.ForeignKey('supply_info.id'))
	new_no = db.Column(db.Float, nullable=False)

	def __init__(self, new_no, supply_id):
		self.new_no = new_no
		self.supply_id = supply_id

class Supplier(db.Model):
	__tablename__ = "supplier"
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(50), unique=True, index=True)
	latitude = db.Column(db.Integer)
	longitude = db.Column(db.Integer)
	supplys_info = db.relationship('SupplyInfo', backref='supplier', lazy=True)

	def __init__(self, name, latitude, longitude):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude

class Census(db.Model):
	__tablename__ = "census"
	id = db.Column(db.Integer(), primary_key=True)
	item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
	all_no = db.Column(db.Integer, nullable=False)
	supply_info_id = db.Column(db.Integer, db.ForeignKey('supply_info.id'))

	def __init__(self, all_no):
		self.all_no = all_no
        
# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
