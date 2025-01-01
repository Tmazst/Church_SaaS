
# from alchemy_db import db.Model
from sqlalchemy import  MetaData, ForeignKey
from flask_login import login_user, UserMixin
from sqlalchemy.orm import backref, relationship
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from app import app

db = SQLAlchemy()

#from app import login_manager

metadata = MetaData()

class all_churches(db.Model):

    __table_name__ = "all_churches"

    id = db.Column(db.Integer,primary_key=True)
    church_name = db.Column(db.String(100))
    registered_by=db.Column(db.String(100))
    registered_by_contact=db.Column(db.String(100))
    church_contacts=db.Column(db.String(100))
    slogan = db.Column(db.String(100))
    location = db.Column(db.String(100))
    church_email = db.Column(db.String(120),unique=True)
    church_web = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    image = db.Column(db.String(100))
    church_senior_pastor = db.Column(db.String(100))
    description = db.Column(db.String(100))
    country = db.Column(db.String(100))
    edited_by = db.Column(db.String(50))
    region = db.Column(db.String(100))
    location = db.Column(db.String(100))
    users_ids = relationship("User", backref='all_churches', lazy=True)
    events_ids = relationship("open_event", backref='all_churches', lazy=True)
    open_pledges_ids = relationship("open_pledges", backref='all_churches', lazy=True)
    announcements_ids = relationship("announcements", backref='all_churches', lazy=True)
    church_services_ids = relationship("church_services", backref='all_churches', lazy=True)
    calender_ids = relationship("calender", backref='all_churches', lazy=True)
    subscription_ids = relationship("subscription", backref='all_churches', lazy=True)
    timestamp = db.Column(db.DateTime)


class subscription(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    chrch_id = db.Column(db.Integer, ForeignKey('all_churches.id'))
    updated_by = db.Column(db.Integer)
    subscrptn = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)


#Users class'
class User(db.Model,UserMixin):

    __table_args__ = {'extend_existing': True}

    #Create db.Columns
    id = db.Column(db.Integer,primary_key=True)
    chrch_id = db.Column(db.Integer, ForeignKey('all_churches.id'))
    name = db.Column(db.String(24))
    email = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(120), unique=True)
    confirm_password = db.Column(db.String(120), unique=True)
    timestamp = db.Column(db.DateTime)
    verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(120))
    image = db.Column(db.String(120))
    next_of_kin = db.Column(db.String(120))
    next_of_kin_no = db.Column(db.String(120))
    employ_status = db.Column(db.String(120))
    employer = db.Column(db.String(120))
    skills = db.Column(db.String(255))
    qualifications = db.Column(db.String(255))
    experience = db.Column(db.String(255))
    state = db.Column(db.String(60))
    absent = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(50))
    marital = db.Column(db.String(50))
    age_group = db.Column(db.String(120))
    absent_reason = db.Column(db.String(50))
    absent_no = db.Column(db.Integer)
    country = db.Column(db.String(120))
    # Part 2
    church_local = db.Column(db.String(50))
    church_branch = db.Column(db.String(50))
    gender = db.Column(db.String(30))
    pastor = db.Column(db.String(30))#Fix Duplicate ----------------
    church_activity = db.Column(db.String(30))
    pledges_ids = relationship("pledges", backref='user', lazy=True)
    

    __mapper_args__={
        "polymorphic_identity":'user',
        'polymorphic_on':role
    }


class church_services(db.Model):

    __table_name__ = "church_services"

    id = db.Column(db.Integer,primary_key=True)
    usr_id = db.Column(db.Integer)
    chrch_id = db.Column(db.Integer, ForeignKey('all_churches.id'))
    title = db.Column(db.String(100))
    day = db.Column(db.String(50))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    edited_by = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)


class open_pledges(db.Model):

    __table_name__="open_pledges"

    id = db.Column(db.Integer,primary_key=True)
    usr_id = db.Column(db.Integer, ForeignKey('user.id'))
    chrch_id = db.Column(db.Integer, ForeignKey('all_churches.id'))
    title = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    fundraising_amount = db.Column(db.Float)
    information = db.Column(db.String(100))
    open = db.Column(db.Boolean, default=True)
    end_date = db.Column(db.Date)
    edited_by = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    pledges_id = relationship("pledges", backref='open_pledges', lazy=True)
    


class pledges(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    usr_id = db.Column(db.Integer, ForeignKey('user.id'))
    chrch_id = db.Column(db.Integer, ForeignKey('all_churches.id'))
    open_pledge_id = db.Column(db.Integer, ForeignKey('open_pledges.id'))
    amount = db.Column(db.Float)
    other = db.Column(db.String(120))
    other2 = db.Column(db.String(120))
    paid = db.Column(db.Boolean, default=False)
    remove_plg = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime)
    


class calender(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    chrch_id = db.Column(db.Integer, ForeignKey('all_churches.id'))
    usr_id = db.Column(db.Integer)
    title = db.Column(db.String(50))
    other_info = db.Column(db.String(100))
    venue = db.Column(db.String(50))
    registrations = db.Column(db.String(100))
    other = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    time = db.Column(db.DateTime)
    edited_by = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime)


class announcements(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    chrch_id = db.Column(db.Integer, ForeignKey('all_churches.id'))
    usr_id=db.Column(db.Integer)
    title = db.Column(db.String(50))
    directed_to = db.Column(db.String(50))
    info = db.Column(db.String(255))
    edited_by = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime)


class church_user(User):

    __table_name__ = "church_user"

    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    contacts = db.Column(db.String(20))
    address = db.Column(db.String(255))
    age_group = db.Column(db.String(120))
    other = db.Column(db.String(120))
    other2 = db.Column(db.String(120))
    other3 = db.Column(db.String(120))
    pop_ids = relationship("pop_transactions", backref='church_user', lazy=True)
    # jobs_applied_for = relationship("Applications", backref='Applications.job_title', lazy=True)
    # hired_user = relationship("hired", backref='Hired Applicant', lazy=True)

    __mapper_args__={
            "polymorphic_identity":'church_user'
        }


class admin_user(User):

    __table_name__ = "admin_user"

    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    contacts = db.Column(db.String(20))
    address = db.Column(db.String(120))
    age_group = db.Column(db.String(120))
    other = db.Column(db.String(120))
    other2 = db.Column(db.String(120))
    committee_local_pos=db.Column(db.String(120))
    committee_local_group=db.Column(db.String(120))#Youth, Brothers,Women,Men,Deacons
    # committee_mission_grp=db.Column(db.String(120))#msac,myc,cyc
    # committee_mission_pos=db.Column(db.String(120))
    pastor=db.Column(db.String(120))
    senior_pastor=db.Column(db.Boolean)
    other3 = db.Column(db.String(120))
    other4 = db.Column(db.String(120))
    admin_code = db.Column(db.Numeric(5),unique=True,nullable=True)
    image_ad = db.Column(db.String(30), nullable=True)
    pop_id = relationship("pop_transactions", backref='admin_user', lazy=True)
    session_id = relationship("open_event", backref='admin_user', lazy=True)

    __mapper_args__={
            "polymorphic_identity":'admin_user'
        }


#Open & Closed sessions for registrations
class open_event(db.Model):

    __table_name__ = "open_events"

    id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.Integer, ForeignKey('user.id'))
    chrch_id = db.Column(db.Integer, ForeignKey('all_churches.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    event_title = db.Column(db.String(60), nullable=False)
    event_abbr = db.Column(db.String(60), nullable=True)
    event_venue = db.Column(db.String(60), nullable=False)
    event_theme = db.Column(db.String(60), nullable=True)
    poster = db.Column(db.String(100))
    event_other_info = db.Column(db.String(60), nullable=True)
    registration_group1=db.Column(db.String(80))
    reg_fee_amnt1=db.Column(db.Float, nullable=True)
    registration_group2=db.Column(db.String(80))
    reg_fee_amnt2=db.Column(db.Float, nullable=True)
    registration_group3=db.Column(db.String(80))
    reg_fee_amnt3=db.Column(db.Float, nullable=True)
    registration_group4=db.Column(db.String(80))
    reg_fee_amnt4=db.Column(db.Float, nullable=True)
    registration_group5=db.Column(db.String(80))
    reg_fee_amnt5=db.Column(db.Float, nullable=True)
    registration_group6=db.Column(db.String(80))
    reg_fee_amnt6=db.Column(db.Float, nullable=True)
    event_closed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, nullable=False) #DateTime
    event_ids = relationship("pop_transactions", backref='events', lazy=True)


#For registration
class pop_transactions(db.Model):

    __table_name__ = "pop_transactions"

    id = db.Column(db.Integer, primary_key=True)
    usr_id = db.Column(db.Integer, ForeignKey('user.id'))
    chrch_id = db.Column(db.Integer, ForeignKey('all_churches.id'))
    event_id = db.Column(db.Integer, ForeignKey('open_event.id'))
    transaction_id = db.Column(db.String(120), unique=True)
    transaction_token = db.Column(db.String(120), unique=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    registration = db.Column(db.String(120))
    reg_tag = db.Column(db.String(120))#
    age_group = db.Column(db.String(120))
    special_diet = db.Column(db.String(120))
    payment_platform = db.Column(db.String(120))
    accommodation_bool = db.Column(db.Boolean)
    accommodation_add_info = db.Column(db.Boolean)
    pop_image = db.Column(db.String(120))
    church_local = db.Column(db.String(50))
    church_branch = db.Column(db.String(50))
    children_id = relationship("children", backref='pop_transactions', lazy=True)


class children(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    parent_id = db.Column(db.Integer, ForeignKey('pop_transactions.usr_id'))
    chrch_id = db.Column(db.Integer, ForeignKey('all_churches.id'))
    age_group = db.Column(db.String(120))
    denom_structure = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, nullable=False)







#
# class Project_Brief(db.Model,UserMixin):
#
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer,ForeignKey('user.id'))
#     name = db.Column(db.String(120))
#     brief_date = db.Column(db.String(120))
#     token = db.Column(db.String(120))
#
#
# class Curr_Projects(db.Model,UserMixin):
#
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, ForeignKey('user.id'))
#     name = db.Column(db.String(120))
#     deposit = db.Column(db.Numeric(20))
#     installments = db.Column(db.Numeric(20))
#     proj_charge = db.Column(db.Numeric(20))
#     proj_started = db.Column(db.Date())
#     proj_deadline = db.Column(db.Date())
#     comments = db.Column(db.String(120))
#     submitted = db.Column(db.Date())


