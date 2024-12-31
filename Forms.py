from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, TextAreaField,BooleanField, SelectField,DateField, URLField,TelField,RadioField,FloatField,TimeField,SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from flask_wtf.file import FileField , FileAllowed,FileRequired
from flask import jsonify
# from wtforms.fields.html5 import DateField,DateTimeField


class Register(FlaskForm):

    name = StringField('name', validators=[DataRequired(),Length(min=2,max=24)])
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm = PasswordField('confirm', validators=[DataRequired(),EqualTo('password'), Length(min=8, max=64)])
    admin_bool = BooleanField('Register as Admin?')

    submit = SubmitField('Create Account!')

    def validate_email(self,email):
        from app import db, User, app

        # with db.init_app(app):
        user_email = User.query.filter_by(email = self.email.data).first()
        if user_email:
            print("CHECKING EMAIL: " , user_email)
            return user_email


class UserAccountForm(FlaskForm):

    address = StringField('Physical Address')
    contacts = TelField('Phone Number', validators=[DataRequired()])
    church_local = StringField('Local Church', validators=[DataRequired()])
    church_branch = StringField('Church Branch', validators=[DataRequired()])
    state = StringField('Region / State / Province', validators=[Optional()])
    title = RadioField('Title', validators=[Optional()],choices=[("Mr", "Mr"),("Mrs", "Mrs"),("Ms", "Ms"),("Br", "Br")])
    marital = RadioField('Mairatl Status', validators=[Optional()],choices=[("Married", "Married"),("Single", "Single"),("Single (Engaged)", "Single (Engaged)")])
    gender = SelectField('Gender',choices=[("----", "-----"),("Male", "Male"),("Female", "Female")])
    # pastor = SelectField('Are You a Pastor?',choices=[("None", "None"),("Pastor", "Pastor"),("Reverend", "Reverend")])
    age_group = SelectField('Group',choices=[("Null", "-----"),("Youth", "Youth"),("Mothers", "Mothers"),("Fathers", "Fathers"),("Children", "Children")])
    other = StringField('')
    other2 = StringField('')
    other3 = StringField('')
    image = FileField('Profile Picture',validators=[FileAllowed(['jpg', 'png', 'webp'], 'Images only!')])
    next_of_kin = StringField('Emergency Contact Person')
    next_of_kin_no = TelField('Their Contacts')
    employ_status = SelectField('Employment Status', validators=[Optional()],choices=[("Entreprenuer", "Entreprenuer/Self-Employed"),("Working", "Employed"),("Un-employed","No Job")])
    employer = StringField('Employer (If Working)')
    skills = StringField('Skills')
    qualifications = StringField('Qualifications (If Applicable)', validators=[Optional(),Length(max=200)])
    experience = StringField('Experience', validators=[Optional(),Length(max=200)])
    church_activity = RadioField('Choose Your Role',choices=[("None", "None"),("Praise Team", "Praise Team"),("Ushering", "Ushering"),("Cleaner", "Cleaner"),("Band", "Band")])
    country = SelectField('Country',choices=[("----", "-----"),("Eswatini", "Eswatini"),("South Africa", "South Africa"),("Mozambique", "Mozambique"),
                                                     ("Botswana", "Botswana"),("Zimbabwe", "Zimbabwe"),("Lesotho", "Lesotho"),("Namibia", "Namibia"),("Zimabwe", "Zimabwe"),("Zambia", "Zambia")])
    submit = SubmitField('Update')


class AdminAccountForm(FlaskForm):

    address = StringField('Physical Address')
    contacts = TelField('Phone Number', validators=[DataRequired()])
    age_group = SelectField('Group',choices=[("Null", "-----"),("Youth", "Youth"),("Mothers", "Mothers"),("Fathers", "Fathers")])
    title = RadioField('Title',validators=[Optional()],choices=[("Null", "-----"),("Mr", "Mr"),("Mrs", "Mrs"),("Ms", "Ms"),("Br", "Br")])
    marital = RadioField('Mairatl Status',validators=[Optional()],choices=[("Married", "Married"),("Single", "Single"),("Single (Engaged)", "Single (Engaged)")])
    church_local = StringField('Local Church', validators=[DataRequired()])

    church_branch = StringField('Branch', validators=[Optional()])
    state = StringField('Region / State / Province', validators=[Optional()])
    gender = SelectField('Gender',choices=[("Null", "-----"),("Male", "Male"),("Female", "Female")])
    pastor = SelectField('Are You a Minister?',choices=[("None", "None"),("Pastor", "Pastor"),("Reverend", "Reverend"),("Prophet", "Prophet")
                                                      ,("Apostle", "Apostle"),("Evangelist", "Evangelist"),("Apostle", "Apostle"),("Bishop", "Bishop"),("Arch Bishop", "Arch Bishop")])
    senior_pastor = BooleanField('Senior Church Minister?',validators=[Optional()])
    committee_local_group=SelectField('Local Committee Group',choices=[("None", "None"),("Deacons", "Deacons"),("Elders", "Elders"),
                                                                          ("Youth Committee", "Youth Committee"),("Brothers Committee", "Brothers Committee"),("Sisters Committee", "Sisters Committee"),("Fathers Committee", "Fathers Committee"),("Womens Committee", "Womens Commiittee")
                                                                          ,("Sunday School", "Sunday School")])
    committee_local_pos=SelectField('Local Committee Membership',choices=[("None", "None"),("Chairman", "Chairman"),("Vice-Chairman", "Vice-Chairman"),
                                                                          ("Secretary", "Secretary"),("Vice-Secretary", "Vice-Secretary"),("Treasurer", "Treasurer")
                                                                          ,("Add Member", "Add Member"),("Sunday School Teacher", " Sunday School Teacher")])
    # committee_mission_grp=SelectField('Mission Committee Group',choices=[("None", "None"),("MSAC Committee", "MSAC Committee"),("MYC Committee", "MYC Committee")
    #                                                                       ,("CYC Committee", "CYC Committee")])
    # committee_mission_pos=SelectField('Mission Committee Membership',choices=[("None", "None"),("Chairman", "Chairman"),("Vice-Chairman", "Vice-Chairman"),
    #                                                                       ("Secretary", "Secretary"),("Vice-Secretary", "Vice-Secretary"),("Treasurer", "Treasurer")
    #                                                                       ,("Add Member", "Add Member")])
    other = StringField('')
    other2 = StringField('')
    other3 = StringField('')
    next_of_kin = StringField('Emergency Contact Person')
    next_of_kin_no = StringField('Their Contacts')
    employ_status = SelectField('Employment Status', validators=[Optional()],choices=[("Entreprenuer", "Entreprenuer/Self-Employed"),("Working", "Working"),("Employed","No Job")])
    employer = StringField('Employer (If Working)')
    skills = StringField('Skills')
    qualifications = StringField('Qualifications (If Applicable)')
    experience = StringField('Experience')
    image = FileField('Profile Picture',validators=[FileAllowed(['jpg', 'png', 'webp'], 'Images only!')])
    church_activity = RadioField('Choose Your Role',choices=[("None", "None"),("Praise Team", "Praise Team"),("Ushering", "Ushering"),("Cleaner", "Cleaner"),("Band", "Band")])
    country = SelectField('Country',choices=[("Eswatini", "Eswatini"),("South Africa", "South Africa"),("Mozambique", "Mozambique"),
                                                     ("Botswana", "Botswana"),("Zimbabwe", "Zimbabwe"),("Lesotho", "Lesotho"),("Namibia", "Namibia"),("Zimabwe", "Zimabwe"),("Zambia", "Zambia"),])
    
    submit = SubmitField('Update')


class AllChurchesForm(FlaskForm):
    church_name = StringField('Church Name', validators=[DataRequired()])
    slogan = StringField('Church Slogan / Verse', validators=[Optional()])
    church_contacts = TelField('Church Contacts', validators=[DataRequired()])
    location = StringField('Church Physical Address', validators=[DataRequired()])
    image = FileField('Church Logo',validators=[FileAllowed(['jpg', 'png', 'webp'], 'Images only!')])
    church_email = StringField('email', validators=[DataRequired(),Email()])
    church_web = URLField('Church Website', validators=[Optional()])
    facebook = URLField('Church Facebook', validators=[Optional()])
    registered_by=StringField('Name', validators=[DataRequired()])
    registered_by_contact=TelField('Contact No.', validators=[DataRequired()])
    church_senior_pastor = StringField('Senior Pastor', validators=[Optional()])
    country = SelectField('Country',choices=[("Eswatini", "Eswatini"),("South Africa", "South Africa"),("Mozambique", "Mozambique"),
                                                     ("Botswana", "Botswana"),("Zimbabwe", "Zimbabwe"),("Lesotho", "Lesotho"),("Namibia", "Namibia"),("Zimabwe", "Zimabwe"),("Zambia", "Zambia")])
    region = StringField('State / Region', validators=[Optional()])

    submit = SubmitField('Submit')


class AnnouncementsForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])
    directed_to = SelectField('Targeted Group',choices=[("Whole Church", "Whole Church"),("Youth", "Youth"),("Young Adults", "Young Adults"),("Women", "Women")
                                               ,("Men", "Men"),("Sunday School", "Sunday School"),("Couples", "Couples"),("Singles", "Singles"),("Sisters", "Sisters"),("Brother", "Brother")])
    
    info = TextAreaField('Announcement', validators=[DataRequired(),Length(min=5,max=200)])
    emails = BooleanField('Send Email to Users?', validators=[Optional()])
    submit = SubmitField('Submit')


class CalenderForm(FlaskForm):

    title = StringField('Event Title*', validators=[DataRequired()])
    start_date = DateField('Start Date (Event)*',validators=[DataRequired()])
    end_date = DateField('End Date',validators=[Optional()])
    venue = StringField('Venue',validators=[Optional(),Length(min=3,max=50)])
    registrations = TextAreaField('Registrations Details',validators=[Optional(),Length(min=5,max=100)])
    time = TimeField('Time',validators=[Optional()])

    submit = SubmitField('Submit')


class PledgesForm(FlaskForm):
    amount = FloatField('My Pledge (Do not include currency)',validators=[DataRequired()]) #User
    remove_plg = BooleanField('Remove Pledge') #User Can disable after end date
    submit = SubmitField('Submit')


class OpenPledgesForm(FlaskForm):

    title = StringField('Title*', validators=[DataRequired()]) #Admin Only
    information = StringField('Additional Info', validators=[Optional(),Length(min=5,max=100)])
    start_date = DateField('Pledges Start Date*',validators=[DataRequired()]) #Admin Only
    end_date = DateField('Pledges End Date*',validators=[DataRequired()]) #Admin Only
    fundraising_amount = FloatField('Amount Required* (Do not include currency)',validators=[DataRequired()]) 
    paid = BooleanField('Pledge Paid?') #Admin Only
    submit = SubmitField('Submit')


class ChurchServicesForm(FlaskForm):

    title = StringField('Title*', validators=[DataRequired()])
    day = StringField("Day(s)*", validators=[DataRequired()])
    start_time = TimeField('Start Time*',validators=[DataRequired()])
    end_time = TimeField('End Time',validators=[Optional()])
    submit = SubmitField('Submit')


class OpenEventForm(FlaskForm):

    start_date = DateField('Start Date (Event)',validators=[DataRequired()])
    end_date = DateField('End Date',validators=[DataRequired()])
    event_title = StringField('Services Title', validators=[DataRequired()])
    event_abbr = StringField('Abbreviation (Optional)')#
    event_theme = StringField('Services Theme (Optional)')
    event_venue = StringField('Venue', validators=[DataRequired()])#
    poster = FileField('Upload Event Poster',validators=[FileAllowed(['jpg', 'png', 'webp'], 'Images only!')])
    registration_group1 = SelectField('Select Group',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    reg_fee_amnt1 = FloatField("Amount", validators=[Optional()])
    registration_group2 = SelectField('Select Group',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    reg_fee_amnt2 = FloatField("Amount", validators=[Optional()])
    registration_group3 = SelectField('Select Group',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    reg_fee_amnt3 = FloatField("Amount", validators=[Optional()])
    registration_group4 = SelectField('Select Group',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    reg_fee_amnt4 = FloatField("Amount", validators=[Optional()])
    registration_group5 = SelectField('Select Group',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    reg_fee_amnt5 = FloatField("Amount", validators=[Optional()])
    registration_group6 = SelectField('Select Group',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    reg_fee_amnt6 = FloatField("Amount", validators=[Optional()])
    event_other_info = StringField('Other Info')
    submit = SubmitField('Submit')


class RegistrationsForm(FlaskForm):

    transaction_id = StringField('Transaction Reference No.')
    pop_image = FileField('Upload Proof of Payment')
    pop_image_comp = FileField('Upload Proof of Payment')
    no_pop = BooleanField('None')
    payment_platform = SelectField('Payment Platform?',
                                  choices=[("Mobile Money", "Mobile Money"),("FNB", "FNB"),("Standard Bank", "Standard Bank"),("NedBank", "NedBank")
                                           ,("Eswatini Bank", "Eswatini Bank"),("Swaziland Building Society", "Swaziland Building Society")])
    registration = SelectField('Registration',
                            choices=[("VIP", "VIP"),("Adults", "Adults"),("Working Youth", "Working Youth"),("Non Working Youth", "Non Working Youth"),("Children", "Children")])
    special_diet_bool = RadioField('Special Diet?',choices=[(0, "No"),(1, "Yes")], validators=[Optional()])
    special_diet = StringField('Please Specify')
    accommodation_bool = BooleanField('Accommodation Required?')
    # accommodation_add_info = RadioField('Accommodation (Will you be staying at the conference venue?")',choices=[(0, "No"),(1, "Yes")],default=0)
    submit = SubmitField('Submit')


class AddChildrenForm(FlaskForm):
    child_name_1 = StringField('Child Name')
    child_name_2 = StringField('Child Name')
    child_name_3 = StringField('Child Name')
    child_name_4 = StringField('Child Name')
    child_name_5 = StringField('Child Name')
    child_name_6 = StringField('Child Name')

    submit = SubmitField('Submit')

    

class Login(FlaskForm):
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=64)])
    submit = SubmitField('Login')


class Contact_Form(FlaskForm):

    name = StringField('name')
    email = StringField('email', validators=[DataRequired(),Email()])
    contact = TelField('contact')
    subject = StringField("subject")
    message = TextAreaField("Message",validators=[Length(min=8, max=255)])
    submit = SubmitField("Send")


class Reset(FlaskForm):

    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password'), Length(min=8, max=64)])

    reset = SubmitField('Reset')


class Reset_Request(FlaskForm):

    email = StringField('email', validators=[DataRequired(), Email()])
    reset = SubmitField('Submit')

    # def validate_email(self,email):
    #     user = user.query.filter_by