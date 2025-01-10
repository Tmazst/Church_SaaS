
from flask import Flask,render_template,url_for,redirect,request,flash,jsonify,session,send_file
from flask_login import login_user, LoginManager,current_user,logout_user, login_required
from urllib.parse import quote
from Forms import *
from models import *
from flask_bcrypt import Bcrypt
import secrets
# import MySQLdb
import time
import os
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
# from bs4 import BeautifulSoup as bs
from flask_colorpicker import colorpicker
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
import itsdangerous
from sqlalchemy.exc import IntegrityError
from authlib.integrations.flask_client import OAuth
import json
from sqlalchemy import inspect
from PIL import Image
import mysql.connector
import random
from faker import Faker
from urllib.parse import quote
# import logging


#Change App
app = Flask(__name__)
app.config['SECRET_KEY'] = "sdsdjfe832j2rj_32j"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///techxicons_db.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:tmazst41@localhost/all_churches"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://techtlnf_tmaz:!Tmazst41#@localhost/techtlnf_all_churches"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle':280}
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOADED"] = 'static/uploads'
# app.config['JSON_AS_ASCII'] = True

oauth = OAuth(app)
db.init_app(app)

application = app

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Log in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

ALLOWED_EXTENSIONS = {"txt", "xlxs", 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'gif',"JPG"}

if os.path.exists('client.json'):
    # Load secrets from JSON file
    with open('client.json') as f:
        creds = json.load(f)

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# # Set up logging configuration
# logging.basicConfig(level=logging.INFO)

# # Suppress Werkzeug logger
# werkzeug_logger = logging.getLogger('werkzeug')
# werkzeug_logger.setLevel(logging.ERROR)

# # Create a logs directory and setup the log file path
# log_dir = os.path.join(os.path.dirname(__file__), 'logs')
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)
    
# # Configure logger for SQLAlchemy
# sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
# sqlalchemy_logger.setLevel(logging.INFO)
# sqlalchemy_logger.propagate = False

# # File handler for SQL logs (user entries)
# file_handler = logging.FileHandler(os.path.join(log_dir, 'user_queries.log'))
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
# sqlalchemy_logger.addHandler(file_handler)

from authlib.integrations.base_client.errors import MismatchingStateError

@app.errorhandler(MismatchingStateError)
def handle_mismatching_state_error(error):
    return "Authentication is Terminated due to Security Measures, Please Go Back To Login Again.", 400


class user_class:
    s = None

    def get_reset_token(self, c_user_id):

        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': c_user_id, 'expiration_time': time.time() + 300}).encode('utf-8')

    @staticmethod
    def verify_reset_token(token, expires=1800):

        s = Serializer(app.config['SECRET_KEY'], )

        try:
            user_id = s.loads(token, max_age=300)['user_id']
        except itsdangerous.SignatureExpired:
           return f'Token has expired!, Please Create a New Token'
        except itsdangerous.BadSignature:
            return f'Token has expired, Please Create a New Token'
        except:
            return f'Something Went Wrong'
         
        return user_id

if os.path.exists('client.json'):
    appConfig = {
        "OAUTH2_CLIENT_ID" : creds['clientid'],
        "OAUTH2_CLIENT_SECRET":creds['clientps'],
        "OAUTH2_META_URL":"",
        "FLASK_SECRET":"sdsdjsdsdjfe832j2rj_32jfesdsdjfe832j2rj32j832",
        "FLASK_PORT": 5000  
    }


    oauth.register("fearegistra",
                client_id = appConfig.get("OAUTH2_CLIENT_ID"),
                client_secret = appConfig.get("OAUTH2_CLIENT_SECRET"),
                    api_base_url='https://www.googleapis.com/',
                    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo', 
                client_kwargs={ "scope" : "openid email profile"},
                server_metadata_url= 'https://accounts.google.com/.well-known/openid-configuration',
                jwks_uri = "https://www.googleapis.com/oauth2/v3/certs"
                )


def compress_image(image_path, target_size_kb):
    # Open an image file
    with Image.open(image_path) as img:

        try:
            img = img.convert('RGB')  # Convert to RGB for compatibility with JPEG
            # if img.mode in ('RGBA', 'LA'):
            #     img = img.convert('RGB')  # Convert to RGB
            # elif img.mode == 'L':
            #     img = img.convert('L')  # Convert to L if you want to keep it grayscale without alpha
            # Calculate quality based on the target size
            quality = 85  # Starting quality
            while True:
                # Save to a temporary file to check the size
                temp_file = image_path.replace(os.path.splitext(image_path)[1], "_temp.jpg")
                img.save(temp_file, format='JPEG', quality=quality)

                # Check size
                if os.path.getsize(temp_file) <= target_size_kb * 1024:  # Convert KB to bytes
                    break
                quality -= 5  # Decrease quality to reduce file size

                if quality < 10:  # Minimum quality threshold
                    break

            # Move the temp file to the original file name or save as a new file
            os.replace(temp_file, image_path)
            
        except Exception as e:
            print(f"Error standardizing image input: {e}")
            return None 


def process_file(file):
    
    print("Check File: ",file)
    if isinstance(file, str):
        return file
    else:
        filename = secure_filename(file.filename)

        _img_name, _ext = os.path.splitext(filename)
        gen_random = secrets.token_hex(8)
        new_file_name = gen_random + _ext

        if file.filename == '':
            return 'No selected file'

        print("DEBUG FILE NAME: ", file.filename)
        file_path = os.path.join("static/images", new_file_name)
        
        # Save the file first
        file.save(file_path)
        
        # Compress the image to ~90KB
        compress_image(file_path, target_size_kb=90)

        # flash("File Upload Successful!!", "success")
        return new_file_name


def process_pop_file(file,usr_id):
    print("Check File: ",file)
    if file.startswith("default"):
        return file
    else:
        filename = secure_filename(file.filename)

        _img_name, _ext = os.path.splitext(filename)
        gen_random = secrets.token_hex(8)
        new_file_name = gen_random + str(usr_id) + _ext

        if file.filename == '':
            return 'No selected file'

        if file.filename:
            file_saved = file.save(os.path.join(app.config["UPLOADED"],new_file_name))
            # flash(f"File Upload Successful!!", "success")
            return new_file_name

        else:
            return f"Allowed are [.txt, .xls,.docx, .pdf, .png, .jpg, .jpeg, .gif] only"


def createall(db_):
    db_.create_all()


encry_pw = Bcrypt()


ser=Serializer(app.config['SECRET_KEY'])

@app.context_processor
def inject_ser():
    # global ser
    church = None
    event = open_event.query.filter_by(event_closed=False).first()
    user_no_base=None

    #Pledges
    days_left = 0
    pledges_pocket = None
    subscr_package = None
    pledges_nm = None
    events_nm = None
    announce_nm = None
    registered_nm = None
    services_nm = None
    # pledges = None
    # events = None

    if current_user.is_authenticated:
        
        latest_subcription = subscription.query.filter_by(chrch_id=current_user.chrch_id).order_by(subscription.timestamp.desc()).first()

        if latest_subcription:
            subscr_package = latest_subcription

        user_no_base=User.query.filter_by(chrch_id=current_user.chrch_id).all()
        church = all_churches.query.get(current_user.chrch_id)
        pledges_pocket = open_pledges.query.filter_by(chrch_id=current_user.chrch_id,open=True).first()
        pledges_nm = len(pledges.query.filter_by(chrch_id=current_user.chrch_id).all())
        events_nm = len(calender.query.filter_by(chrch_id=current_user.chrch_id).all())
        announce_nm = len(announcements.query.filter_by(chrch_id=current_user.chrch_id).all())
        registered_nm = len(pop_transactions.query.filter_by(chrch_id=current_user.chrch_id).all())
        services_nm = len(church_services.query.filter_by(chrch_id=current_user.chrch_id).all())
        if pledges_pocket:
            left = pledges_pocket.end_date - datetime.now().date()
            days_left = left.days

    return dict(event_details=event,pop_transts=pop_transactions,user_no_base=user_no_base,ser=ser,church=church,
                days_left=days_left,pocket=pledges_pocket,subscr_package=subscr_package,pledges_pocket_nm=pledges_pocket,
                pledges_nm=pledges_nm, envts_nm=events_nm,announce_nm=announce_nm,services_nm=services_nm,registered_nm=registered_nm)


#Users faker
fake = Faker()

# Function to create a random user
def create_random_user(chrch_id):

    return church_user(
        chrch_id=chrch_id,
        name=fake.name(),
        email=fake.unique.email(),
        password=fake.password(), #In a real app, hash this password before saving
        confirm_password=fake.password(), # Same here
        timestamp = datetime.now(),
        verified = True,
        role = "church_user",
        image = "default.jpg",
        next_of_kin = "Mrs Nontobeko",
        next_of_kin_no = "7910 4621",
        employ_status = "Working",
        employer = "Shoprite",
        skills = "Accountant",
        qualifications = "Degree in Accounting",
        experience = "3 year experience at Camp Hills Hotel",
        state = "Hhohho",
        title = "Br",
        marital = "Single (Engaged)",
        age_group = "Youth",
        country = "Eswatini",
        contacts = "7611 6584",
        # Part 2
        church_local = "Hosea Calvary Ministries",
        church_branch = "Lobamba",
        gender = "Female",
        pastor = "Bisho Osborn",
        church_activity = "Band",
    )


@app.route("/create_users")
def generate_and_save_users(num_users=20, chrch_id_range=(1)):
    for _ in range(num_users):
        chrch_id = 1 #random.randint(chrch_id_range[0], chrch_id_range[1])
        user = create_random_user(chrch_id)
        db.session.add(user)
    db.session.commit()

    return jsonify({"Created Users":"Did"})


@app.route("/", methods=['POST','GET'])
def home():

    with app.app_context():
       db.create_all()

    event_details=None
    nearest_event =None

    if current_user.is_authenticated:
        if open_event.query.filter_by(event_closed=False).first():
            event_details = open_event.query.filter_by(event_closed=False).first()

        cal_events = calender.query.all()

        # Assuming cal_events is a list of event objects
        # Ensure cal_events is not empty
        if not cal_events:
            print("No events available.")
        else:
            # Calculate the differences in days
            dates_diff = [(event.start_date - datetime.now().date()).days for event in cal_events] #Output e.g. [1,23,4,3,5] days

            # Filter out past events (i.e., negative days left)
            future_events = [(i, diff) for i, diff in enumerate(dates_diff) if diff >= 0] #Output e.g. [(0,1),(1,23),(2,4),(3,3),(4,5)] index,days

            if not future_events:
                print("No upcoming events.")
            else:
                # Find the minimum difference and its index
                min_index, min_days = min(future_events, key=lambda x: x[1])

                # Retrieve the corresponding event
                nearest_event = cal_events[min_index]

                # Print the nearest event and days left
                print(f"The nearest event is {nearest_event} and it starts in {min_days} days.")
    else:
        return redirect(url_for("login"))
    
    if current_user.is_authenticated and current_user.role == 'admin_user':
        flash("For an enhanced interface experience, we encourage admin users to use media devices with wide screens i.e. PC or tablet.","success")
    
    
    return render_template("index.html", event_details=event_details, nearest_event=nearest_event)


@app.route('/church_registration',methods=["POST","GET"])
@login_required
def church_registration():

    church_form = AllChurchesForm()

    # if not current_user.chrch_id:
    #     flash("Your Account has not been Mapped with any church account yet!")
    #     log_out()
    #     return redirect(url_for("home"))

    if request.method =="POST":
        church = all_churches(
            church_name=church_form.church_name.data,
            church_email=church_form.church_email.data,
            church_web=church_form.church_web.data,
            church_senior_pastor=church_form.church_senior_pastor.data,
            country=church_form.country.data,
            facebook=church_form.facebook.data,
            region=church_form.region.data,
            church_contacts= church_form.church_contacts.data,
            location=church_form.location.data,
            timestamp=datetime.now(),
            registered_by=church_form.registered_by.data,
            registered_by_contact=church_form.registered_by_contact.data,
            description = church_form.branch.data
        )

        if current_user.is_authenticated:
            church.registered_by=current_user.id
            usr = admin_user.query.get(current_user.id)
            usr.contacts=church_form.registered_by_contact.data

        if church_form.image.data:
            church.image = process_file(church_form.image.data)

        db.session.add(church)
        db.session.commit()

        church_id = all_churches.query.filter_by(registered_by=current_user.id).first()

        try:
            sub_pckg = subscription(
                chrch_id = church_id.id,
                updated_by = current_user.id,
                subscrptn = church_form.subscribe.data,
                timestamp = datetime.now()
            )
            db.session.add(sub_pckg)
            db.session.commit()
        except:
            return jsonify({"Error Sub-800":"You Might Be Skipping some steps, Please Contact Service Provider for Assistance"})


        flash(f"You have successfully registered {church.church_name} Church Account","success")
        flash(f"Now, select your church and proceed","success")
        return redirect(url_for("select_church"))

    return render_template("church_registration.html",church_form=church_form)


@app.route('/church_registration_edit',methods=["POST","GET"])
@login_required
def church_registration_edit():

    church = all_churches.query.get(current_user.chrch_id)
    church_form = AllChurchesForm(obj=church)

    if request.method =="POST":
        church.church_name=church_form.church_name.data
        church.church_email=church_form.church_email.data
        church.church_contacts= church_form.church_contacts.data
        church.church_web=church_form.church_web.data
        church.country=church_form.country.data
        church.facebook=church_form.facebook.data
        church.region=church_form.region.data
        church.location=church_form.location.data
        church.edited_by=current_user.id

        if church_form.image.data:
                church.image = process_file(church_form.image.data)
                flash(f"Update Successful {church.image}","success")

        db.session.commit()
        flash("Update Successful","success")

    return render_template("church_registration_edit.html",church_form=church_form,church_details=church)


@app.route('/church_account')
@login_required
def church_account():

    church = all_churches.query.get(ser.loads(request.args.get("chrch")["data"]))
    church_form = AllChurchesForm(obj=church)

    if request.method =="POST":
        
        church.church_name=church_form.church_name.data
        church.church_email=church_form.church_email.data
        church.church_web=church_form.church_web.data
        church.church_senior_pastor=church_form.church_senior_pastor.data
        church.country=church_form.country.data
        church.region=church_form.region.data
        church.location=church_form.location.data
        church.timestamp=datetime.now()
        church.registered_by=church_form.registered_by.data
        church.registered_by_contact=church_form.registered_by_contact.data

        if church_form.image.data:
                church.image = process_file(church_form.image.data)

        db.session.add(church)
        db.session.commit()

    return render_template("church_account.html",church_form=church_form,church=church)


@app.route('/share_image/<img_share>')
def share_image(img_share):
    # Name of your image and its path
    image_name = img_share
    image_path = os.path.join('images', image_name)  # Relative path from the static folder
    image_url = url_for('static', filename=image_path, _external=True)  # Full URL to the image
    
    # WhatsApp message with the image URL
    message = f"Check out this image from FEA: {image_url}"
    whatsapp_link = f"https://wa.me/?text={quote(message)}"
    
    return render_template('share_image.html', whatsapp_link=whatsapp_link, image_url=image_url)

@app.route('/share_whatsapp/<img_share>')
def share_whatsapp(img_share):
    # Name of your image and its path
    image_name = img_share
    image_path = os.path.join('images', image_name)  # Relative path from the static folder
    image_url = url_for('static', filename=image_path, _external=True)  # Full URL to the image
    
    # WhatsApp message with the image URL
    message = f"Check out this image from FEA: {image_url}"
    whatsapp_link = f"https://wa.me/?text={quote(message)}"
    
    return render_template('share_image.html', whatsapp_link=whatsapp_link, image_url=image_url)


@app.route('/download_file/<filename>')
def download_file(filename):
    # This serves the file for download
    return send_file(os.path.join(app.static_folder,'images', filename), as_attachment=True)


#Admins Opening & Closing Registrations
@app.route("/open_event_form", methods=["POST", "GET"])
def open_event_form():

    open_reg_form = OpenEventForm()
    event_details=None

    if not current_user.chrch_id:
        flash("Your Account has not been Mapped with any church account yet!")
        log_out()
        return redirect(url_for("home"))

    if open_event.query.filter_by(event_closed=False).first():
        event_details = open_event.query.filter_by(event_closed=False).first()

    if open_reg_form.validate_on_submit():

        open_event_ = open_event(start_date=open_reg_form.start_date.data,end_date=open_reg_form.end_date.data,event_title=open_reg_form.event_title.data,
                        event_abbr=open_reg_form.event_abbr.data,event_theme=open_reg_form.event_theme.data,event_venue=open_reg_form.event_venue.data,
                        registration_group1=open_reg_form.registration_group1.data,reg_fee_amnt1=open_reg_form.reg_fee_amnt1.data,registration_group2=open_reg_form.registration_group2.data,
                        reg_fee_amnt2=open_reg_form.reg_fee_amnt2.data,registration_group3=open_reg_form.registration_group3.data,reg_fee_amnt3=open_reg_form.reg_fee_amnt3.data,
                        event_other_info=open_reg_form.event_other_info.data,timestamp=datetime.now(),
                        chrch_id=current_user.chrch_id
                        )
        
        if open_reg_form.poster.data:
            open_event_.poster = process_file(open_reg_form.poster.data)
        
        db.session.add(open_event_)
        if not event_details:
            db.session.commit()
            flash("Event Opened Successfully!","success")
            return redirect(url_for("home"))
        else:
            flash("Event Already Opened","success")
            return redirect(url_for("home"))      
    else:
        for error in open_reg_form.errors:
            print("Reg Form Errors: ",error)

    return render_template('open_event.html',open_reg_form=open_reg_form)


#Admins Opening & Closing Registrations
@app.route("/opened_event_edit", methods=["POST", "GET"])
def opened_event_edit():

    event_edit = open_event.query.filter_by(event_closed=False).first()
    open_reg_form = OpenEventForm(obj=event_edit)

    if open_reg_form.validate_on_submit():

        event_edit.start_date=open_reg_form.start_date.data
        event_edit.end_date=open_reg_form.end_date.data
        event_edit.event_title=open_reg_form.event_title.data
        event_edit.event_abbr=open_reg_form.event_abbr.data
        event_edit.event_theme=open_reg_form.event_theme.data
        event_edit.event_venue=open_reg_form.event_venue.data
        event_edit.registration_group1=open_reg_form.registration_group1.data
        event_edit.reg_fee_amnt1=open_reg_form.reg_fee_amnt1.data
        event_edit.registration_group2=open_reg_form.registration_group2.data
        event_edit.reg_fee_amnt2=open_reg_form.reg_fee_amnt2.data
        event_edit.registration_group3=open_reg_form.registration_group3.data
        event_edit.reg_fee_amnt3=open_reg_form.reg_fee_amnt3.data

        if open_reg_form.poster.data:
            event_edit.poster = process_file(open_reg_form.poster.data)
        
        db.session.commit()
        flash("Update Successful!","success")
        return redirect(url_for('home'))

    return render_template('opened_event_edit.html',open_reg_form=open_reg_form,event_details=event_edit)


def reg_confirmation():
    
    accommodation="No"
    event = open_event.query.filter_by(event_closed=False).first()
    print("CHECK EVENT: ",event)
    usr_ = church_user.query.get(current_user.id)
    reg_info = pop_transactions.query.filter_by(usr_id=current_user.id).first()

    if reg_info.accommodation_add_info == 1:
        accommodation = "Yes"

    def send_veri_mail():

        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] = creds.get('email')  # os.getenv("MAIL")
        app.config["MAIL_PASSWORD"] = creds.get('gpass') #os.getenv("PWD")
        app.config["MAIL_DEFAULT_SENDER"] = "noreply@gmail.com"

        mail = Mail(app)

        token = user_class().get_reset_token(current_user.id)
        usr_email = usr_.email

        msg = Message(subject="Registration Confirmation", sender="no-reply@gmail.com", recipients=[usr_email])

        msg.html = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #4CAF50;
        }}
        p,li{{font-weight:500;color:#707070 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
        <img style="" src="https://yt3.googleusercontent.com/ytc/AIdro_kWhxLUK_wGrRkKhCAr_L_oGH2T1c-HMvF8VW0odpZ80g=s160-c-k-c0x00ffffff-no-rj" />
        <h2>Hi, {usr_.name}</h2>
        <p>This is to confirm that your registration for the African Evangelical Church's upcoming event was successful.</p>
        <p>Please see details below for your perusal:</p>
        <h3>Event Details:</h3>
        <ul>
            <li><span>Event Title:</span> {event.event_title}</li>
            <li><span>Date:</span> {event.start_date} - {event.end_date} </li>
            <li><span>Venue:</span> {event.event_venue}</li>
        </ul>
        <h3>Registration Information:</h3>
        <ul>
            <li><span>Name:</span> {church_user.query.get(reg_info.usr_id).name}</li>
            <li><span>Age Group:</span> {reg_info.age_group}</li>
            <li><span>Special Diet:</span> {reg_info.special_diet}</li>
            <li><span>Accommodation:</span> {accommodation}</li>
            <li><span>Denominational Structure:</span> {reg_info.registration}</li>
            <li><span>Reg. Date:</span> {reg_info.timestamp.strftime("%d %b %y")}</li>
            <li><span>Payment Mode:</span> {reg_info.payment_platform}</li>
            <li><span>Transaction Token:</span> {reg_info.transaction_token}</li>
        </ul>
        <p class="footer">Thank you for registering!</p>
    </div>
</body>
</html>
"""


        try:
            mail.send(msg)
            flash(f'We have sent you an email with Registration Details', 'success')
            return "Email Sent"
        except Exception as e:
            flash(f'Email not sent here', 'error')
            return "The mail was not sent"

    # try:
    send_veri_mail() 
    # except:


@app.route("/add_children_form", methods=["POST", "GET"])
@login_required
def add_children_form():

    add_child_form = AddChildrenForm()
    # sq_num=["child_name_2","child_name_3","child_name_4","child_name_5","child_name_6","child_name_7"]
    
    if request.method == "POST":
        if add_child_form.validate_on_submit():
            child = children(name=add_child_form.child_name_1.data,parent_id=current_user.id,denom_structure="Sunday School",age_group="Sunday School",timestamp=datetime.now())
            db.session.add(child)
            #Processing many fields
            for key in list(request.form.keys()):
                if key.startswith('child-') and request.form.get(key): 
                    child = children(name=request.form.get(key),parent_id=current_user.id,denom_structure="Sunday School",age_group="Sunday School",timestamp=datetime.now())
                    db.session.add(child)

        db.session.commit()
        flash("Children Registered Successfully!")

    return render_template('add_children_form.html', add_child_form=add_child_form)


#User Registrations Form Edit Confirm
@app.route("/registration_form_edit_confirm", methods=["POST", "GET"])
@login_required
def registration_form_edit_confirm():
    val_registration = None
    
    get_user = User.query.get(current_user.id)
    usr_reg_details = pop_transactions.query.filter_by(usr_id=current_user.id).first()
    registration_form = RegistrationsForm(obj=usr_reg_details)
    event = open_event.query.filter_by(event_closed=False).first()

    if registration_form.validate_on_submit():
        db.session.commit()
        flash("Update Successful!", "success")
        print("Details: ",usr_reg_details.special_diet)


    return render_template('confirm_form_edit.html',usr_reg_details=usr_reg_details,registration_form=registration_form,user=get_user,
                           event_details=event,val_registration=val_registration)


def Get_Registration_Amount(val):
     
    event = open_event.query.filter_by(event_closed=False).first()

    event_dict = event.__dict__
    key_found = None

    # Get the key of the pop_transactions.registration
    for key,value in event_dict.items():
        if value == val:
            key_found = key
            break
    
    # Cook up the fee key using the last digit of val's key to the amount 
    amount = event_dict.get("reg_fee_amnt" + key[-1])

    return amount


@app.route("/view_member", methods=["POST", "GET"])
@login_required
def view_member():

    usr = None
    loc_pastor = None

    user_qrd=User.query.get(request.args.get('id'))
    if user_qrd.role == "church_user":
        usr = church_user.query.get(user_qrd.id)
    elif user_qrd.role == "admin_user":
        usr = admin_user.query.get(user_qrd.id)

    check_loc_pastor = admin_user.query.filter_by(church_local=current_user.church_local,senior_pastor=True).first()
    if check_loc_pastor:
        loc_pastor = check_loc_pastor.name


    return render_template("view_member.html",user=usr,reg_details=pop_transactions,loc_pastor=loc_pastor)


# User Information
@app.route("/reg_view_member", methods=["POST", "GET"])
@login_required
def reg_view_member():


    usr=User.query.get(request.args.get('id'))

    return render_template("reg_view_member.html",user=usr,reg_details=pop_transactions)


# User Information
@app.route('/loc_commitee_memberships')
@login_required
def loc_committee_members():

    committees = ["Deacons","Youth Committee","Fathers Committee","Mothers Committee","Brothers Committee","Sisters Committee"]

    admins = admin_user.query.filter_by(church_local=current_user.church_local).all()

    deacons = admin_user.query.filter_by(church_local=current_user.church_local,committee_local_group="Deacons").all()
    youth_com = admin_user.query.filter_by(church_local=current_user.church_local,committee_local_group="Youth Committee").all()
    fathers_com = admin_user.query.filter_by(church_local=current_user.church_local,committee_local_group="Fathers Committee").all()
    mothers_com = admin_user.query.filter_by(church_local=current_user.church_local,committee_local_group="Mothers Committee").all()
    brothers_com = admin_user.query.filter_by(church_local=current_user.church_local,committee_local_group="Brothers Committee").all()
    sisters_com = admin_user.query.filter_by(church_local=current_user.church_local,committee_local_group="Sisters Committee").all()

    return render_template("local_church_committees.html",admins=admins,deacons=deacons,youth_com=youth_com,fathers_com=fathers_com,
                           mothers_com=mothers_com,brothers_com=brothers_com,sisters_com=sisters_com,committees=committees,admin_obj=admin_user)


# User Information
@app.route('/mission_commitee_memberships')
@login_required
def mission_committee_members():

    
    committees = ["MSAC Committee","MYC Committee"]

    admins = admin_user.query.filter_by(church_local=current_user.church_local).all()

    return render_template("mission_committees.html",admins=admins,committees=committees,admin_obj=admin_user)


#User Registrations Form
@app.route("/user_registration_form", methods=["POST", "GET"])
@login_required
def user_registration_form():

    if not current_user.chrch_id:
        flash("Your Account has not been Mapped with any church account yet!")
        log_out()
        return redirect(url_for("home"))

    val_registration = None
    event=open_event.query.filter_by(event_closed=0,chrch_id=current_user.chrch_id).first()
    # selected_platform = request.form.get('platform')
    registration_form = RegistrationsForm()

    get_user = User.query.get(current_user.id)

    # Update validators based on selection
    # registration_form.update_validators(registration_form.payment_platform.data)

    if event:
        val_registration = pop_transactions.query.filter_by(usr_id=current_user.id).first()
    
    if val_registration:
        flash(f"You are already registered.", "success")
        return redirect(url_for("already_registered"))# redirect(url_for("home"))
    
    if not current_user.church_local:
        flash("Please Finish Up Your Account Setup, First. You're Almost Done!","success")
        if current_user.role == "church_user":
            return redirect(url_for("usr_finish_signup"))
        else:
            return redirect(url_for("admin_finish_signup"))
    
    if registration_form.validate_on_submit():

        reg =registration_form.registration.data + " " + str(Get_Registration_Amount(registration_form.registration.data))
        registration = pop_transactions(
            usr_id=current_user.id,transaction_id=secrets.token_hex(16),transaction_token=secrets.token_hex(16)+str(current_user.id),chrch_id=current_user.chrch_id,
            timestamp=datetime.now(),payment_platform=registration_form.payment_platform.data,registration=reg,reg_tag=registration_form.registration.data, #accomodation = registration_form.accomodation.data
            accommodation_bool=registration_form.accommodation_bool.data,church_branch=current_user.church_branch,church_local=current_user.church_local,
            special_diet=registration_form.special_diet.data,event_id=event.id
            )
        
        if registration_form.pop_image.data:
            file =  process_pop_file(registration_form.pop_image.data,current_user.id)
            registration.pop_image = file

        db.session.add(registration)

        db.session.commit()
        reg_confirmation()

        return redirect(url_for("registration_success"))

    return render_template('registrations_form.html',registration_form=registration_form,user=get_user,event_details=event,val_registration=val_registration)


#User Registrations Form Edit
@app.route("/user_registration_form_edit", methods=["POST", "GET"])
@login_required
def user_registration_form_edit():
    val_registration = None
    get_user = User.query.get(current_user.id)
    usr_reg_details = pop_transactions.query.filter_by(usr_id=current_user.id).first()
    registration_form = RegistrationsForm(obj=usr_reg_details)
    event = open_event.query.filter_by(event_closed=False).first()

    if not usr_reg_details:
        flash("Registration Form","success")
        return redirect(url_for('user_registration_form'))

    if event:
        val_registration = pop_transactions.query.filter_by(usr_id=current_user.id).first()
    
    if not current_user.church_local and not current_user.church_zone:
        flash("Please Finish Up Your Account Setup, First. You're Almost Done!","success")
        return redirect(url_for("finish_signup"))

    if registration_form.validate_on_submit():

        usr_reg_details.payment_platform=registration_form.payment_platform.data
        usr_reg_details.registration=registration_form.registration.data
        usr_reg_details.transaction_id=registration_form.transaction_id.data
        # usr_reg_details.accomodation = registration_form.accomodation.data
        usr_reg_details.accommodation_bool=registration_form.accommodation_bool.data
        usr_reg_details.accommodation_add_info=bool(registration_form.accommodation_add_info.data)
        if registration_form.special_diet_bool:
            usr_reg_details.special_diet=registration_form.special_diet.data

        if registration_form.pop_image.data:
            file =  process_pop_file(registration_form.pop_image.data,current_user.id)
            usr_reg_details.pop_image = file

        db.session.commit()
        flash("Please, Confirm Your Update", "success")
        # return redirect(url_for("registration_form_edit_confirm",registration_form=registration_form))
        # print("Details: ",usr_reg_details.special_diet)

    elif registration_form.errors:
        for error in registration_form.errors:
            print("Update Error: ",error)


    return render_template('registrations_form_edit.html',usr_reg_details=usr_reg_details,registration_form=registration_form,user=get_user,
                           event_details=event,val_registration=val_registration)


#User Registrations Form
@app.route("/already_registered", methods=["POST", "GET"])
@login_required
def already_registered():

    registered_user = church_user.query.get(current_user.id)
    _children = children.query.filter_by(parent_id=current_user.id).all()
    print("Debug Children: ", _children)
    for child in _children:
        print("Debug Children: ", child)

    return render_template('already-registered.html',user=registered_user,reg_info=pop_transactions,children=_children)


# User Information
@app.route("/local_members", methods=["POST", "GET"])
@login_required
def local_members():

    local = None
    loc_pastor = None

    if not current_user.chrch_id:
        flash("Your Account has not been Mapped with any church account yet!")
        log_out()
        return redirect(url_for("home"))

    local_members = User.query.filter_by(chrch_id=current_user.chrch_id).all()
    loc_church = all_churches.query.get(current_user.chrch_id)

    return render_template('local_members.html',loc_church=loc_church,local_members=local_members,
                           local=local,needed=None,loc_pastor=loc_pastor)


# User Information
# @app.route("/local_mem_filtered", methods=["POST", "GET"])
# @login_required
# def local_mem_filtered():

#     local = None
#     loc_pastor = None

#     filter = User.query.filter_by(chrch_id=current_user.chrch_id,)

#     local_members = User.query.filter_by(chrch_id=current_user.chrch_id).all()
#     loc_church = all_churches.query.get(current_user.chrch_id)

#     return render_template('local_mem_filtered.html',loc_church=loc_church,local_members=local_members,
#                            local=local,needed=None,loc_pastor=loc_pastor)


# User Registrations
@app.route("/registered_local", methods=["POST", "GET"])
@login_required
def registered_local():

    local = None

    registered_children = children.query.all()
    
    if request.args.get('loc'):
        local = request.args.get('loc')
    else:
        local = current_user.church_local

    print('Final: ',request.args.get('loc'))

    registered_users =pop_transactions.query.filter_by(church_local=local).all()


    return render_template('registered_local.html',users=User,reg_details=registered_users,registered_children=registered_children,pop_transactions=pop_transactions,
                           local=local,needed=None)


# User Registrations
@app.route("/registered_users", methods=["POST", "GET"])
@login_required
def registered_users():

    registered_users =pop_transactions.query.all()
    registered_children = children.query.all()
    # registered_no = pop_transactions.query.all()

    missions = {entry.church_mission for entry in pop_transactions.query.all()}
    
    print("MISSIONs: ",missions)

    for mission in missions:
        print("MISSION: ",mission)

    return render_template('registered_users.html',users=User,reg_details=registered_users,registered_children=registered_children,pop_transactions=pop_transactions,
                           missions=missions,needed=None)


# User Registrations
@app.route("/my_mission_registrations", methods=["POST", "GET"])
@login_required
def my_mission_registrations():

    registered_users =pop_transactions.query.filter_by(church_mission=current_user.church_mission).all()
    registered_children = children.query.all()
    # registered_no = pop_transactions.query.all()

    missions = {entry.church_mission for entry in pop_transactions.query.all()}
    
    print("MISSIONs: ",missions)

    for mission in missions:
        print("MISSION: ",mission)

    return render_template('my_mission_registrations.html',users=User,reg_details=registered_users,registered_children=registered_children,pop_transactions=pop_transactions,
                           missions=missions,needed=None)


# User Registrations
@app.route("/my_zone_registrations", methods=["POST", "GET"])
@login_required
def my_zone_registrations():

    registered_users =pop_transactions.query.filter_by(church_zone=current_user.church_zone).all()
    registered_children = children.query.all()
    # registered_no = pop_transactions.query.all()

    missions = {entry.church_mission for entry in pop_transactions.query.all()}
    
    print("MISSIONs: ",missions)

    for mission in missions:
        print("MISSION: ",mission)

    return render_template('my_zone.html',users=User,reg_details=registered_users,registered_children=registered_children,pop_transactions=pop_transactions,
                           missions=missions,needed=None)

# User Registrations
@app.route("/registered_zones", methods=["POST", "GET"])
@login_required
def registered_zones():

    registered_users =pop_transactions.query.all()
    registered_children = children.query.all()
    mission=request.args.get("missn")
    # registered_no = pop_transactions.query.all()

    zones = {entry.church_zone for entry in pop_transactions.query.filter_by(church_mission=mission).all()}
    
    # print("MISSIONs: ",missions)

    # for mission in missions:
    #     print("MISSION: ",mission)

    return render_template('registered_zones.html',users=User,reg_details=registered_users,registered_children=registered_children,pop_transactions=pop_transactions,
                           zones=zones,mission=mission,needed=None)


# User Registrations
@app.route("/registrations", methods=["POST", "GET"])
@login_required
def registrations():

    registered_users = church_user.query.all()
    registered_no = pop_transactions.query.all()

    return render_template('registrations.html',users=registered_users,reg_details=pop_transactions,registered_no=registered_no)


@app.route("/registration_success", methods=["POST", "GET"])
@login_required
def registration_success():

    registered_user = church_user.query.get(current_user.id)
    

    return render_template('registration-success.html',user=registered_user,reg_info=pop_transactions)


@app.route("/contact_form", methods=["POST", "GET"])
def contact_form():

    contact_form = Contact_Form()
    
    if request.method == 'POST':
       
        if contact_form.validate_on_submit():
            
            
            # Get user details through their email
            

            def send_link():
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                em = app.config["MAIL_USERNAME"] = creds.get('email') #os.getenv("EMAIL")
                app.config["MAIL_PASSWORD"] = creds.get('gpass') # os.getenv("PWD")

                mail = Mail(app)

                # token = user_class().get_reset_token(usr_email.id)
                msg = Message("Inquiry Message", sender="noreply@demo.com", recipients=[em])
                msg.html = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #4CAF50;
        }}
        p,li{{font-weight:500;color:#505050 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
        <img style="" src="https://camm.churchregistry.org/static/images/camm_logo.png" /> 
        <h4>Name:       {contact_form.name.data}</h4>
        <h4>Email:      {contact_form.email.data}</h4>
        <h4>Contact:    {contact_form.contact.data}</h4>
        <h4>Message:</h4>
        <p> {contact_form.message.data}</p>

        
        <p class="footer">powered by: techxolutions.com</p>
    </div>
</body>
</html>
"""

                try:
                    mail.send(msg)
                    flash('Email Successful Sent!', 'success')
                    return "Email Sent"
                except Exception as e:

                    flash('Ooops, Something went wrong Please Retry!!', 'error')
                    return "The mail was not sent"
        


            # Send the pwd reset request to the above email
            send_link()

            return redirect(url_for('home'))
        elif contact_form.errors:
            for error in contact_form.errors:
                flash(f"Error! Please Check the {error} Field", 'error')

    return render_template("issues_contact_form.html", contact_form=contact_form,user=User)


@app.route("/select_church", methods=["POST","GET"])
def select_church():

    churches = all_churches.query.all()

    for chu in churches:
        print("CHURCHES: ",chu.church_name)

    if request.method == "POST":
        church = all_churches.query.filter_by(church_name=request.form.get("church_chosen")).first()

        if church:
            user = User.query.get(current_user.id)
            user.chrch_id = church.id

            db.session.commit()
            flash("This is the Last Step of your Signup Process!","success")
            if current_user.role == "church_user":
                return redirect(url_for('usr_finish_signup'))
            else:
                return redirect(url_for('admin_finish_signup'))
        else:
            print(f"ERROR! User {user.id}, Church {church} ")
            return jsonify({"Error":"Something Went Wrong!, If problem persists please contact service provider"})
            

    return render_template('select_church.html',churches=churches)


@app.route("/signup", methods=["POST","GET"])
def sign_up():

    register = Register()
    church = None
    show_admin_btn = "True"

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    church = all_churches.query.filter_by(church_name=request.args.get("nm")).first()

    if register.validate_on_submit():

        #print(f"Account Successfully Created for {register.name.data}")
        if request.method == 'POST':
            # context
            hashd_pwd = encry_pw.generate_password_hash(register.password.data).decode('utf-8')
            user1 = church_user(name=register.name.data, email=register.email.data, password=hashd_pwd,
                         confirm_password=hashd_pwd, image="default.jpg",timestamp=datetime.now()
                         )

            try:
                Register().validate_email(register.email.data)
                db.session.add(user1)
                db.session.commit()
  
                flash(f"Account Successfully Created for {register.name.data}", "success")
                # flash(f"Please Enter Login Details", "success")
                return redirect(url_for('login'))
                # return jsonify({"message": "User registered successfully"}), 201
            except IntegrityError:
                db.session.rollback()  # Rollback the session on error
                return jsonify({"message": "Email already exists"}), 409
            except Exception as e:
                db.session.rollback()  # Rollback on any other error
                return jsonify({"message": "An error occurred"}), 500

            # #print(register.name.data,register.email.data)
    elif register.errors:
        flash(f"Account Creation Unsuccessful ", "error")
        #print(register.errors)

    # from myproject.models import user
    return render_template("manual_signup.html",register=register,show_admin_btn=show_admin_btn)


@app.route("/pricing", methods=["POST","GET"])
def pricing():
    
    return render_template("camm_pricing.html")


@app.route("/suscribe", methods=["POST","GET"])
@login_required
def subscribe():

    if request.method == "GET":
        print("Lets see if we can update subscription")
        sub = request.args.get("sub")

        obj = subscription(
            chrch_id = current_user.chrch_id,
            updated_by = current_user.id,
            subscrptn = sub,
            timestamp = datetime.now()
        )

        db.session.add(obj)
        db.session.commit()
        flash("We have updated Your Subscription Package Successfully!", "success")

        return redirect(url_for('home'))


# @app.route("/subscription", methods=["POST","GET"])
# @login_required
# def subscrption():
    
#     return render_template("")


@app.route("/livedemo", methods=["POST","GET"])
def livedemo():

    user_login = User.query.get(1)
    login_user(user_login)

    flash("🎉 Welcome to our live demo! We're excited to have you here. Good luck as you dive in and test things out👍","success")

    return redirect(url_for('home'))

#Verification Pending
@app.route("/login", methods=["POST","GET"])
def login():

    login = Login()

    if login.validate_on_submit():

        if request.method == 'POST':

            user_login = User.query.filter_by(email=login.email.data).first()
            if user_login and encry_pw.check_password_hash(user_login.password, login.password.data):

                if not user_login.verified:
                    login_user(user_login)
                    return redirect(url_for('verification'))
                # else:
                # After login required prompt, take me to the page I requested earlier
                # login_user(user_login)
                # print("No Verification Needed: ", user_login.verified)

                # Check If are they allocated to a church 
                if user_login.chrch_id:
                    login_user(user_login)
                    flash(f"Hey! {user_login.name.title()} You're Logged In!", "success")
                    if user_login.role == "church_user":
                        user = church_user.query.get(user_login.id)
                        if not user.gender or not user.contacts or not user.address:
                                print(user.gender ,user.contacts, user.address)
                                return redirect(url_for('usr_finish_signup'))
                    else:
                        user = admin_user.query.get(user_login.id)
                        if not user.gender or not user.contacts or not user.address:
                            return redirect(url_for('admin_finish_signup'))
                else:
                    flash(f"Please Select Your Local Church", "success")
                    login_user(user_login)
                    return redirect(url_for('select_church'))

                req_page = request.args.get('next')
                return redirect(req_page) if req_page else redirect(url_for('home'))
                
            else:
                flash(f"Login Unsuccessful, please use correct email or password", "error")
                # print(login.errors)
    else:
        print("No Validation")
        if login.errors:
            for error in login.errors:
                print("Errors: ", error)
        else:
            print("No Errors found", login.email.data, login.password.data)

    return render_template("login.html",login=login)


@app.route("/admin_signup", methods=["POST","GET"])
def admin_signup():

    register = Register()
    show_admin_btn = None

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if register.validate_on_submit():

        #print(f"Account Successfully Created for {register.name.data}")
        if request.method == 'POST':
            # context
            hashd_pwd = encry_pw.generate_password_hash(register.password.data).decode('utf-8')
            user1 = admin_user(name=register.name.data, email=register.email.data, password=hashd_pwd,
                         confirm_password=hashd_pwd, image="default.jpg", timestamp=datetime.now()
                         )

            try:
                email = Register().validate_email(register.email.data)
                if email:
                    return jsonify({"Error":"This email Already Exists"})
                db.session.add(user1)
                db.session.commit()
                flash(f"Account Successfully Created for {register.name.data}", "success")
                return redirect(url_for('login'))
            except IntegrityError:
                flash(f"Something went wrong, check for errors", "success")
                jsonify({"Error":"This Email Already Exists"})

            # #print(register.name.data,register.email.data)
    elif register.errors:
        flash(f"Account Creation Unsuccessful ", "error")
        #print(register.errors)

    # from myproject.models import user
    return render_template("manual_signup.html",register=register,show_admin_btn=show_admin_btn)


def update_zone(registration_form):
    zone = registration_form.church_zone.data.title()
    
    # Check if 'zone' is part of the input data
    if 'Zone' not in zone.split():
        zone += ' Zone'  # Append "zone" with a space if it is not present

    return zone

@app.route("/absent", methods=["POST","GET"])
@login_required
def absent():
    pass

#Signup Confirmation Email
def signup_confirm():
   
    usr_ = church_user.query.get(current_user.id)
    church = all_churches.query.filter_by(id=current_user.chrch).first()

    def send_veri_mail():

        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] = creds.get('email')  # os.getenv("MAIL")
        app.config["MAIL_PASSWORD"] = creds.get('gpass') #os.getenv("PWD")
        app.config["MAIL_DEFAULT_SENDER"] = "noreply@gmail.com"

        mail = Mail(app)

        token = user_class().get_reset_token(current_user.id)
        usr_email = usr_.email

        msg = Message(subject="Registration Confirmation", sender="no-reply@gmail.com", recipients=[usr_email])

        msg.html = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #4CAF50;
        }}
        p,li{{font-weight:500;color:#707070 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
        <img style="" src="https://camm.churchregistry.org/{church.image}" />
        <h2>Hi, {usr_.name}</h2>
        <p>Thank you for registering! Your account with {church.church_name} has been successfully created.</p>
        <p>For your records, please find the details below:</p>
        <h3>Account Details:</h3>
        <ul>
            <li><span>Name:</span> {usr_.name}</li>
            <li><span>Title:</span> {usr_.title}</li>
            <li><span>Email:</span> {usr_.email}</li>
            <li><span>Marital Status:</span> {usr_.marital}</li>
            <li><span>Sex:</span> {usr_.gender}</li>
            <li><span>Age Group:</span> {usr_.age_group}</li>
            <li><span>Address:</span> {usr_.address} </li>
            <li><span>Region/Province/State:</span> {usr_.state}</li>
            <li><span>Country:</span> {usr_.country}</li>
            <li><span>Family Member:</span> {usr_.next_of_kin}</li>
            <li><span>Thier Contact:</span> {usr_.next_of_kin_no}</li>
            <li><span>Church Activity/Role:</span> {usr_.church_activity}</li>
        </ul>
        <h3>Other:</h3>
        <ul>
            <li><span>Employment Status:</span> {usr_.employ_status}</li>
            <li><span>Employer:</span> {usr_.employer}</li>
            <li><span>Skills:</span> {usr_.skills}</li>
            <li><span>Qualification:</span> {usr_.qualifications}</li>
            <li><span>Experience:</span> {usr_.experience}</li>
        </ul>
        <h3>Church Details:</h3>
        <ul>
            <li><span>Local Church:</span> {church.church_name}</li>
            <li><span>Branch:</span> {church.description}</li>
            <li><span>Location:</span> {church.location}</li>
            <li><span>Contacts:</span> {church.church_contacts}</li>
            <li><span>Email:</span> {church.church_email}</li>
            <li><span>Website:</span> {church.church_web}</li>
            <li><span>Facebook:</span> {church.facebook}</li>
            <li><span>Senior Pastor:</span> {church.church_senior_pastor}</li>
        </ul>
        <p class="footer">"Thank you for registering! Don’t miss out on upcoming updates from the church, including announcements, church services, details on event registrations, the church calendar, and more!"</p>
        
    </div>
</body>
</html>
"""


        try:
            mail.send(msg)
            flash(f'We have sent you an email with Registration Details', 'success')
            return "Email Sent"
        except Exception as e:
            flash(f'Email not sent here', 'error')
            return "The mail was not sent"

    # try:
    send_veri_mail() 
    # except:


@app.route("/usr_finish_signup", methods=["POST","GET"])
@login_required
def usr_finish_signup():

    user=None

    user = church_user.query.get(current_user.id)
    finish_register = UserAccountForm(obj=user)
    loc_church = all_churches.query.get(current_user.chrch_id)

    if finish_register.validate_on_submit():

        if request.method == 'POST':

            user.contacts=finish_register.contacts.data
            user.address=finish_register.address.data
            user.church_local=finish_register.church_local.data 
            user.church_branch=finish_register.church_branch.data
            user.age_group=finish_register.age_group.data
            user.gender=finish_register.gender.data
            user.country = finish_register.country.data
            user.church_activity = finish_register.church_activity.data

            if finish_register.image.data:
                user.image = process_file(finish_register.image.data)

            db.session.commit()
            if loc_church:
                signup_confirm()
            flash(f"Congratulations✨, You have just finished signing up for your {loc_church.church_name} membership", "success")

            return redirect(url_for('home'))

    elif finish_register.errors:
        for error in finish_register.errors:
            print("Error: ", error)
        flash(f"Account Creation Unsuccessful", "error")

    # from myproject.models import user
    return render_template("usr_finish_signup.html",finish_register=finish_register,user=user,loc_church=loc_church)


@app.route("/admin_finish_signup", methods=["POST","GET"])
@login_required
def admin_finish_signup():

    user=None
    
    loc_church = all_churches.query.get(current_user.chrch_id)

    user = admin_user.query.get(current_user.id)
    finish_register = AdminAccountForm(obj=user)

    if finish_register.validate_on_submit():

        if request.method == 'POST':

            user.contacts=finish_register.contacts.data
            user.address=finish_register.address.data
            user.church_local=finish_register.church_local.data
            user.church_branch=finish_register.church_branch.data
            user.pastor=finish_register.pastor.data
            user.committee_local_group=finish_register.committee_local_group.data
            user.committee_local_pos=finish_register.committee_local_pos.data
            # user.committee_mission_grp=finish_register.committee_mission_grp.data
            # user.committee_mission_pos=finish_register.committee_mission_pos.data
            user.age_group=finish_register.age_group.data
            user.gender=finish_register.gender.data
            user.senior_pastor=finish_register.senior_pastor.data
            user.country = finish_register.country.data
            user.church_activity = finish_register.church_activity.data

            if finish_register.image.data:
                user.image = process_file(finish_register.image.data)

            db.session.commit()
            if loc_church:
                signup_confirm()
            flash(f"Congratulations✨, You have just finished signing up for your {loc_church.church_name} membership", "success")
            
            return redirect(url_for('home'))

    elif finish_register.errors:
        for error in finish_register.errors:
            print("Error: ",error)
        flash(f"Account Creation Unsuccessful ", "error")

    # from myproject.models import user
    return render_template("admin_finish_signup.html",finish_register=finish_register,user=user,loc_church=loc_church)


# User Account
@app.route("/user_account", methods=["POST", "GET"])
def user_account():


    usr_account=church_user.query.get(current_user.id)
    account_form = UserAccountForm(obj=usr_account)

    if account_form.validate_on_submit():

        if request.method == 'POST':

            usr_account.contacts=account_form.contacts.data
            usr_account.address=account_form.address.data
            usr_account.church_branch=account_form.church_branch.data
            usr_account.age_group=account_form.age_group.data
            usr_account.church_local=account_form.church_local.data
            usr_account.gender=account_form.gender.data
            usr_account.next_of_kin=account_form.next_of_kin.data
            usr_account.next_of_kin_no=account_form.next_of_kin_no.data
            usr_account.marital=account_form.marital.data
            usr_account.title=account_form.title.data
            usr_account.employ_status=account_form.employ_status.data
            usr_account.employer=account_form.employer.data
            usr_account.skills=account_form.skills.data
            usr_account.qualifications=account_form.qualifications.data
            usr_account.experience=account_form.experience.data
            usr_account.country = account_form.country.data
            usr_account.church_activity = account_form.church_activity.data

            if account_form.image.data:
                # print("Image Data", account_form.image.data)
                usr_account.image = process_file(account_form.image.data)

            # try:
            db.session.commit()
            flash(f"Update Successful!", "success")
            print("Update Successful!")


    return render_template('user_account.html',account_form =account_form, usr_account=usr_account)


# Admin Account
@app.route("/admin_account", methods=["POST", "GET"])
def admin_account():

    
    usr_account=admin_user.query.get(current_user.id)
    account_form = AdminAccountForm(obj=usr_account)

    if account_form.validate_on_submit():

        if request.method == 'POST':

            usr_account.contacts=account_form.contacts.data
            usr_account.church_branch=account_form.church_branch.data
            usr_account.age_group=account_form.age_group.data
            usr_account.church_local=account_form.church_local.data
            usr_account.gender=account_form.gender.data
            usr_account.next_of_kin=account_form.next_of_kin.data
            usr_account.next_of_kin_no=account_form.next_of_kin_no.data
            usr_account.employ_status=account_form.employ_status.data
            usr_account.employer=account_form.employer.data
            usr_account.marital=account_form.marital.data
            usr_account.title=account_form.title.data
            usr_account.skills=account_form.skills.data
            usr_account.qualifications=account_form.qualifications.data
            usr_account.experience=account_form.experience.data
            usr_account.pastor=account_form.pastor.data
            usr_account.committee_local_pos=account_form.committee_local_pos.data
            usr_account.committee_local_group=account_form.committee_local_group.data
            usr_account.senior_pastor=account_form.senior_pastor.data
            usr_account.country=account_form.country.data
            usr_account.church_activity=account_form.church_activity.data

            if account_form.image.data:
                usr_account.image = process_file(account_form.image.data)

            # try:
            db.session.commit()
            flash(f"Update Successful!", "success")
            print("Update Successful!")
    else:
        for error in account_form.errors:
            print("Admin Account Errors: ",error)

    return render_template('admin_account.html',usr_account=usr_account,account_form=account_form)


@app.route("/reset/<token>", methods=['POST', "GET"])
def reset(token):
    reset_form = Reset()

    if request.method == 'POST':

        # try:

        usr_obj = user_class().verify_reset_token(token)
        pass_reset_hash = encry_pw.generate_password_hash(reset_form.new_password.data)
        usr_obj = User.query.get(usr_obj)
        usr_obj.password = pass_reset_hash
        db.session.commit()

        flash(f"You have Successfully Changed your Password! You can now Login with your New Password", "success")

        return redirect(url_for("login"))
        # except:
        #     print("Password Reset Failed!!")
        #     flash(f"Password Reset Failed, Please try again later", "error")
        #     return f'Reset Failed, Try again later'

    return render_template("pass_reset.html", reset_form=reset_form)


@app.route("/forgot_password", methods=['POST', "GET"])
def reset_request():

    reset_request_form = Reset_Request()

    if current_user.is_authenticated:
        logout_user()

    if request.method == 'POST':
        if reset_request_form.validate_on_submit():
            # Get user details through their email
            usr_email = User.query.filter_by(email=reset_request_form.email.data).first()

            if usr_email is None:
                # print("The email you are request for is not register with T.H.T, please register first, Please Retry")
                flash("The email you are requesting a password reset for, is not registered, please register an account first",
                    'error')

                return redirect(url_for("reset_request"))

            def send_link(usr_email):
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                em = app.config["MAIL_USERNAME"] = creds.get('email') #os.getenv("EMAIL")
                app.config["MAIL_PASSWORD"] = creds.get('gpass') # os.getenv("PWD")

                mail = Mail(app)

                token = user_class().get_reset_token(usr_email.id)
                msg = Message("Password Reset Request", sender="noreply@demo.com", recipients=[usr_email.email])
                msg.html = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #2b54a5;
        }}
        p,li{{font-weight:500;color:#505050 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
        <h2>Good day, {usr_email.name}</h2>

        <p>You have requested a password reset for your CAMM Sys+ (Church Administration & Membership Management Sys) Account</p>
        <p style="font-weight:600">To reset your password, visit the following link;</p>
        <a href="{url_for('reset', token=token, _external=True)}" 
            style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #f2f2f2; background-color: #2b54a5; 
                    border: none; border-radius: 15px; text-decoration: none; text-align: center;">
            Reset
        </a>
        <p class="footer">If you did not request the above message please ignore it, and your password will remain unchanged.</p>
    </div>
</body>
</html>
"""

                try:
                    mail.send(msg)
                    flash('An email has been sent with instructions to reset your password', 'success')
                    return "Email Sent"
                except Exception as e:

                    flash('Ooops, Something went wrong Please Retry!!', 'error')
                    return "The mail was not sent"


            # Send the pwd reset request to the above email
            send_link(usr_email)

            return redirect(url_for('login'))

    return render_template("password_reset_req.html", reset_request_form=reset_request_form)


@app.route("/verification", methods=["POST", "GET"])
# User email verification @login
# @login the user will register & when the log in the code checks if the user is verified first...
def verification():

    usr_ = User.query.get(current_user.id)

    def send_veri_mail():

        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] = creds.get('email')  # os.getenv("MAIL")
        app.config["MAIL_PASSWORD"] =  creds.get('gpass') #os.getenv("PWD")
        app.config["MAIL_DEFAULT_SENDER"] = "noreply@gmail.com"

        mail = Mail(app)

        token = user_class().get_reset_token(current_user.id)
        usr_email = usr_.email

        msg = Message(subject="Email Verification", sender="no-reply@gmail.com", recipients=[usr_email])

        msg.html = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #2b54a5;
        }}
        p,li{{font-weight:500;color:#505050 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
        <h2>Hi, {usr_.name}</h2>

        <p>Please follow the link below to verify your email with CAMM Sys+ (Church Administration & Membership Management Sys):</p>
        <p style="font-weight:600">Verification link;</p>
        <a href="{ url_for('verified', token=token, _external=True) }" 
            style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #fff; background-color: #2b54a5; 
                    border: none; border-radius: 15px; text-decoration: none; text-align: center;">
            Verify Email
        </a>
        <p class="footer">Thank you for registering an account!</p>
    </div>
</body>
</html>
"""


        # try:
        mail.send(msg)
        flash(f'An email has been sent with a verification link to your email account', 'success')
        log_out()
        return "Email Sent"
        # except Exception as e:
        #     flash(f'Email not sent here', 'error')
        #     return "The mail was not sent"

    # try:
    if not usr_.verified:
        send_veri_mail()
    else:
        log_out()
        return redirect(url_for("home"))
    # except:
    #     flash(f'Email Not Sent. Please try again', 'error')
    #     log_out()
    #     return redirect(url_for("login"))

    return render_template('verification.html')


@app.route("/verified/<token>", methods=["POST", "GET"])
# Email verification link verified with a token
def verified(token):
    # Check to verify the token received from the user email
    # process the user_id for the following script
    user_id = user_class.verify_reset_token(token)

    try:
        usr = User.query.get(user_id)
        usr.verified = True
        db.session.commit()
        if usr.verified:
            login_user(usr)
            # if not current_user.is_authenticated:
            #     if not current_user.church_local and not current_user.church_zone:
            print(f"Finish Setup, {usr.id}")
            flash(f"Please Select Your Church", "success")
            return redirect(url_for('select_church'))
            # return redirect(url_for('account'))
    except Exception as e:
        flash(f"Something went wrong, Please try again ", "error")
        return redirect(url_for('home'))

    return render_template('verified.html')


@app.route('/logout')
def log_out():

    logout_user()

    return redirect(url_for('home'))


def add_column(cls,attr):
    with app.app_context():
        # Check if the 'age' column already exists
        if not hasattr(cls, attr):
            db.session.execute.text(f'ALTER TABLE {cls} ADD COLUMN {attr} INT;')
            db.session.commit()
            print(f"Column {attr} added successfully.")
        else:
            print(f"Column {attr}  already exists.")


def get_class_attributes(cls):
    # Use vars() to get instance attributes (for an instance of the class)
    # For the class itself, use cls.__dict__ to get class attributes
    class_attributes = vars(cls) if isinstance(cls, object) else cls.__dict__
    
    # Retrieve only the attribute names
    attribute_names = [name for name, value in class_attributes.items() if not callable(value) and not name.startswith('__') and not name.startswith('_')]
    
    return attribute_names


# Function to get column names of a table
def get_table_columns(table):
    """Retrieve column names of a specified table."""
    inspector = inspect(db.engine)
    columns = [column['name'] for column in inspector.get_columns(table)]
    return columns


@app.route("/google_signup", methods=["POST","GET"])
def google_signup():

    return render_template('google_signup.html')

#google login
@app.route("/google_login", methods=["POST","GET"])
def google_login():

    # print("DEBUG CREDITENTAILS: ",appConfig.get("OAUTH2_CLIENT_ID"),' ',appConfig.get("OAUTH2_CLIENT_SECRET"))

    return oauth.fearegistra.authorize_redirect(redirect_uri=url_for("google_signin",_external=True))


#login redirect
@app.route("/google_signin", methods=["POST","GET"])
def google_signin():

    token = oauth.fearegistra.authorize_access_token()

    session['user'] = token

    pretty=session.get("user")

    usr_info = pretty.get('userinfo')
    verified = usr_info.get("email_verified")
    usr_email = usr_info.get("email")
    usr_name=usr_info.get("name")
    usr_athash=usr_info.get("at_hash")

    if not verified:
        print("VERIFIED CHECK: ", verified)
        flash("Access Denied!, Your Email is not verified with Google")
        flash("Please, Set up your account manually")
        return redirect(url_for('sign_up'))
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    #Sign Up
    if not User.query.filter_by(email=usr_email).first():

        print("Email Not Found!, We will register")

        # context
        hashd_pwd = encry_pw.generate_password_hash(usr_athash).decode('utf-8')
        user1 = church_user(name=usr_name, email=usr_email, password=hashd_pwd,
                        confirm_password=hashd_pwd, image="default.jpg",timestamp=datetime.now(),verified=True)

        try:
            db.session.add(user1)
            db.session.commit()

            #Login user
            usr_obj = User.query.filter_by(email=usr_email).first()
            #Check if user have a church id
            if usr_obj.chrch_id:
                login_user(usr_obj)
            else:
                return redirect(url_for('select_church'))

            # if not current_user.church_local and not current_user.church_zone:
            #     return redirect(url_for('finish_signup'))
        
        except IntegrityError:
            db.session.rollback()  # Rollback the session on error
            return jsonify({"message": "Email already exists"}), 409
        
        except Exception as e:
                db.session.rollback()  # Rollback on any other error
                return jsonify({"message": "An error occurred", "error": str(e)}), 500
        
    else:
        user_login = User.query.filter_by(email=usr_email).first()

        if not user_login.verified:
            login_user(user_login)
            return redirect(url_for('verification'))

        if user_login.chrch_id:
            login_user(user_login)
            flash(f"Hey! {user_login.name.title()} You're Logged In!", "success")
            if user_login.role == "church_user":
                user = church_user.query.get(user_login.id)
                if not user.gender or not user.contacts or not user.address:
                        print(user.gender ,user.contacts, user.address)
                        return redirect(url_for('usr_finish_signup'))
            else:
                user = admin_user.query.get(user_login.id)
                if not user.gender or not user.contacts or not user.address:
                    return redirect(url_for('admin_finish_signup'))
        else:
            flash(f"Please Select Your Local Church", "success")
            login_user(user_login)
            return redirect(url_for('select_church'))

        req_page = request.args.get('next')
        return redirect(req_page) if req_page else redirect(url_for('home'))
    

    return redirect(url_for("home"))


####FEATURES

@app.route("/church_services_form", methods=["POST","GET"])
@login_required
def church_services_form():

    if not current_user.chrch_id:
        flash("Your Account has not been Mapped with any church account yet!")
        log_out()
        return redirect(url_for("home"))

    services_form = ChurchServicesForm()

    if request.method == "POST":
        services = church_services(chrch_id=current_user.chrch_id,title =services_form.title.data,
                day=services_form.day.data,start_time=services_form.start_time.data,end_time=services_form.end_time.data,timestamp = datetime.now(),usr_id=current_user.id)
        
        db.session.add(services)
        db.session.commit()
        flash("Submitted Successfully","success")

    return render_template("church_services_form.html",services_form=services_form)


@app.route("/church_services_edit", methods=["POST","GET"])
@login_required
def church_services_form_edit():

    service = church_services.query.filter_by(id=ser.loads(request.args.get('srvc'))['data']
                                               ,chrch_id=current_user.chrch_id).first()
    services_form = ChurchServicesForm(obj=service)

    if request.method == "POST":
        service.title=services_form.title.data
        service.day=services_form.day.data
        if services_form.start_time.data:
            service.start_time =services_form.start_time.data
        if services_form.end_time.data:
            service.end_time =services_form.end_time.data
        service.edited_by=current_user.id
        service.timestamp=datetime.now()

        db.session.commit()
        flash("Update Successfull",'success')

    return render_template("church_services_edit.html",services_form=services_form,service=service)


@app.route("/church_services", methods=["POST","GET"])
@login_required
def church_services_func():

    services = church_services.query.filter_by(chrch_id=current_user.chrch_id).all()

    return render_template("church_services.html",services=services)


@app.route("/members_stats", methods=["POST","GET"])
@login_required
def members_stats():
    
    members_stats = User.query.filter_by(chrch_id=current_user.chrch_id).all()
    males = User.query.filter_by(chrch_id=current_user.chrch_id,gender='Male').all()
    females = User.query.filter_by(chrch_id=current_user.chrch_id,gender='Female').all()
    own_bossess = User.query.filter_by(chrch_id=current_user.chrch_id,employ_status='Entreprenuer').all()
    youth = User.query.filter_by(chrch_id=current_user.chrch_id,age_group='Youth').all()
    fathers = User.query.filter_by(chrch_id=current_user.chrch_id,age_group='Fathers').all()
    mothers = User.query.filter_by(chrch_id=current_user.chrch_id,age_group='Mothers').all()
    children = User.query.filter_by(chrch_id=current_user.chrch_id,age_group='Children').all()
    no_job = User.query.filter_by(chrch_id=current_user.chrch_id,employ_status='Un-employed').all()
    single = User.query.filter_by(chrch_id=current_user.chrch_id,marital='Single').all()
    single_engaged = User.query.filter_by(chrch_id=current_user.chrch_id,marital='Single (Engaged)').all()
    married = User.query.filter_by(chrch_id=current_user.chrch_id,marital='Married').all()
    employed = User.query.filter_by(chrch_id=current_user.chrch_id,employ_status='Working').all()
    praise_team = User.query.filter_by(chrch_id=current_user.chrch_id,church_activity="Praise Team").all()
    ushers_team = User.query.filter_by(chrch_id=current_user.chrch_id,church_activity="Ushering").all()
    band = User.query.filter_by(chrch_id=current_user.chrch_id,church_activity="Band").all()
    cleaner = User.query.filter_by(chrch_id=current_user.chrch_id,church_activity="Cleaner").all()

    return render_template("members_stats.html",members_stats=members_stats,males=males,
                           females=females,own_bossess=own_bossess,praise_team=praise_team,ushers_team=ushers_team,band=band,
                           no_job=no_job,employed=employed,youth=youth,fathers=fathers,mothers=mothers,children=children,
                           single=single,single_engaged=single_engaged,married=married,cleaner=cleaner)


@app.route('/search', methods=['GET'])
def search_in_table():

    user_obj = User()

    search_value = request.args.get('value')
    table_name = "user"  # request.args.get('table_name')

    # Database connection parameters
    db_config = {
        'user': 'techtlnf_tmaz',#creds['user'],
        'password': creds['pdb'],
        'host': 'localhost',  # or your MySQL server address
        'database': 'techtlnf_all_churches'
    }

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Use parameters to avoid SQL injection
    query = f"SELECT * FROM `{table_name}` WHERE CONCAT(COALESCE(gender, ''), COALESCE(age_group, ''), COALESCE(marital, ''), COALESCE(qualifications, ''), COALESCE(church_activity, ''), COALESCE(employ_status, ''))  LIKE %s"
    cursor.execute(query, ('%' + search_value + '%',))
    rows = cursor.fetchall()

    # Print results for debugging
    for row in rows:
        print("Car Make: ", row)

    # Convert the results to a list of dictionaries (depending on your needs)
    results = [{'id':row[0], 'name': row[2], 'email': row[3], 'employ_status': row[12], 
             'country': row[21], 'branch': row[23], 'gender': row[27]} for row in rows]

    cursor.close()
    conn.close()

    return render_template('search_results.html', user_obj=user_obj, search_results=results,search_value=search_value)


@app.route("/pledges", methods=["POST","GET"])
@login_required
def all_pledges():
    days_left = 0

    pledges_pocket = open_pledges.query.filter_by(chrch_id=current_user.chrch_id,open=True).first()
    all_pledges = pledges.query.filter_by(chrch_id=current_user.chrch_id,open_pledge_id=pledges_pocket.id).all()
    

    
    if pledges_pocket:
        left = pledges_pocket.end_date - datetime.now().date()
        days_left = left.days
        
        if days_left >= 0:
            print("Days Left: ",days_left)
        else:
            print("Pledges are Closed")

        if days_left <= 0:
            pledges_pocket.open = False
            db.session.commit()


    return render_template("pledges.html",pledges=all_pledges,usr=User,pocket=pledges_pocket,days_left=days_left)


@app.route("/pledges_pockets", methods=["POST","GET"])
@login_required
def pledges_pockets():

    all_pockets = open_pledges.query.filter_by(chrch_id=current_user.chrch_id).all()
    months = {evt.start_date.strftime("%B") for evt in all_pockets}

    return render_template("pledges_pockets.html",pledges_pockets=all_pockets,months=months,usr=User)


@app.route("/open_pledges_form", methods=["POST","GET"])
@login_required
def open_pledges_form():

    if not current_user.chrch_id:
        flash("Your Account has not been Mapped with any church account yet!")
        log_out()
        return redirect(url_for("home"))

    open_pledges_form = OpenPledgesForm()
    pledges_pocket = open_pledges.query.filter_by(chrch_id=current_user.chrch_id,open=True).first()

    if request.method == "POST":
        pledges = open_pledges(
            chrch_id=current_user.chrch_id,title=open_pledges_form.title.data,usr_id=current_user.id,
            start_date=open_pledges_form.start_date.data,end_date=open_pledges_form.end_date.data,
            fundraising_amount=open_pledges_form.fundraising_amount.data,information=open_pledges_form.information.data,
            timestamp = datetime.now()
                )
        

            
        db.session.add(pledges)
        if not pledges_pocket:
            db.session.commit()
            flash("Pledge Pocket Opened Successfully","success")
            return redirect(url_for("pledges_pockets"))
        
        return jsonify({"Note":f"You have a Pledges Pocket Opened Already, {pledges_pocket.title}"})
        

    return render_template("open_pledges_form.html",open_pledges_form=open_pledges_form)


@app.route("/open_pledges_form_edit", methods=["POST","GET"])
@login_required
def open_pledges_form_edit():

    pledges = open_pledges.query.filter_by(id=ser.loads(request.args.get('pldgs'))['data']
                                               ,chrch_id=current_user.chrch_id).first()
    open_pledges_form = OpenPledgesForm(obj=pledges)

    if request.method == "POST":
        pledges.chrch_id=current_user.chrch_id
        pledges.title =open_pledges_form.title.data
        pledges.start_date=open_pledges_form.start_date.data
        pledges.end_date=open_pledges_form.end_date.data
        pledges.information=open_pledges_form.information.data
        pledges.fundraising_amount=open_pledges_form.fundraising_amount.data
        pledges.timestamp = datetime.now()
        pledges.edited_by = current_user.id


        db.session.commit()
        flash("Update Successfull",'success')

    return render_template("open_pledges_edit.html",pledges=pledges,open_pledges_form=open_pledges_form)


@app.route("/pledge_form", methods=["POST","GET"])
@login_required
def pledge_form():
    # days_left=0

    if not current_user.chrch_id:
        flash("Your Account has not been Mapped with any church account yet!")
        log_out()
        return redirect(url_for("home"))

    pledge_form = PledgesForm()
    pledges_pocket = open_pledges.query.filter_by(chrch_id=current_user.chrch_id,open=True).first()

    # if pledges_pocket:
    #     left = pledges_pocket.end_date - datetime.now().date()
    #     days_left = left.days

    #     if days_left <= 0:
    #         pledges_pocket.open = False
    #         db.session.commit()

    if request.method == "POST":
        pledge = pledges(chrch_id=current_user.chrch_id,open_pledge_id =pledges_pocket.id,
                         amount=pledge_form.amount.data, usr_id=current_user.id,timestamp=datetime.now())
        
        db.session.add(pledge)
        db.session.commit()
        flash("Submitted Successfully","success")

    return render_template("pledges_form.html",pledge_form=pledge_form,pocket=pledges_pocket,usr=admin_user)


@app.route("/calender_form", methods=["POST","GET"])
@login_required
def calender_form():

    if not current_user.chrch_id:
        flash("Your Account has not been Mapped with any church account yet!")
        log_out()
        return redirect(url_for("home"))
    
    calender_form = CalenderForm()

    if request.method == "POST":
        calender_obj = calender(chrch_id=current_user.chrch_id,title =calender_form.title.data,usr_id=current_user.id,
                start_date=calender_form.start_date.data,end_date=calender_form.end_date.data,registrations=calender_form.registrations.data,
                venue=calender_form.venue.data,timestamp=datetime.now())
        
        db.session.add(calender_obj)
        db.session.commit()
        flash("Church Event Posted Successfully","success")
        return redirect(url_for("calender"))

    return render_template("calender_form.html",calender_form=calender_form)


@app.route("/calender_form_edit", methods=["POST","GET"])
@login_required
def calender_form_edit():

    calender_obj = calender.query.filter_by(id=ser.loads(request.args.get('clndr'))['data']
                                               ,chrch_id=current_user.chrch_id).first()
    calender_form = CalenderForm(obj=calender_obj)

    if request.method == "POST":
        calender_obj.title=calender_form.title.data
        calender_obj.start_date=calender_form.start_date.data
        calender_obj.end_date=calender_form.end_date.data
        calender_obj.registrations=calender_form.registrations.data
        if calender_form.venue.data:
            calender_obj.venue=calender_form.venue.data
        calender_obj.edited_by=current_user.id

        db.session.commit()
        flash("Upadte Successfully","success")

    return render_template("calender_form_edit.html",calender_form=calender_form,calender_obj=calender_obj)


@app.route("/calender", methods=["POST","GET"])
@login_required
def church_calender():

    church_calender = calender.query.all()

    months = {evt.start_date.strftime("%B") for evt in church_calender}
    years = {evt.start_date.year for evt in church_calender}
    dt = datetime.now().date()

    return render_template("calender.html",church_calender=church_calender,months=months,years=years,dt=dt)


@app.route("/email_users", methods=["POST","GET"])
def email_users():
    
    

    if request.method == "GET" and current_user.role == 'admin_user':
        obj = request.args.get("obj")

        announcement_obj = announcements.query.filter_by(id=obj,chrch_id=current_user.chrch_id).first()

        print("*****DEBUG ANNOUNCE: ",announcement_obj.title)

        all_users = [user.email for user in User.query.filter_by(chrch=current_user.church).all()]

        # all_users = ["thabo.mmaziya@gmail.com","pro.dignitron@gmail.com"]

        print("CHECK EVENT: ",all_users)

        church = all_churches.query.get(current_user.chrch_id)

        usr = User.query.get(current_user.id)

        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] =  "pro.dignitron@gmail.com" #os.getenv("MAIL") #creds.get('email')
        app.config["MAIL_PASSWORD"] = os.getenv("PWD") #creds.get('gpass') 
        app.config["MAIL_DEFAULT_SENDER"] = "noreply@gmail.com"

        mail = Mail(app)

        html_content = f"""<html>
<head>
<style>
    body {{
        font-family: Arial, sans-serif;
        background-color: #f6f6f6;
        color: #333;
        padding: 20px;
    }}
    .container {{
        background-color: #ffffff;
        border-radius: 5px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }}
    h2,h3 {{
        color: #4CAF50;
    }}
    p,li{{font-weight:500;color:#707070 }}
    .footer {{
        margin-top: 20px;
        font-size: 0.9em;
        color: #777;
    }}
    span{{ font-weight:600;color:coral}}
</style>
</head>
<body>
<div class="container">
    <!---- <img style="" src="https://yt3.googleusercontent.com/ytc/AIdro_kWhxLUK_wGrRkKhCAr_L_oGH2T1c-HMvF8VW0odpZ80g=s160-c-k-c0x00ffffff-no-rj" /> ---->
    <h2>Dear {church.church_name} Member</h2>

    <p>{announcement_obj.info}</p>
    <p>email by: {usr.name}, {usr.committee_local_pos} - {usr.committee_local_group}</p>
    <br>
    <p class="footer">Church Announcements!</p>
</div>
</body>
</html>
"""

        # Create email message
    
        msg = Message(
            subject=announcement_obj.title,
            sender=app.config["MAIL_DEFAULT_SENDER"],
            recipients=[],  # Leave recipients empty if using BCC
            bcc=all_users,  # Add all users to BCC to hide recipient info
            html=html_content
        )

        try:
            mail.send(msg)
            flash(f'Emails Sent Successfully', 'success')
            return "Email Sent"
        except Exception as e:
            flash(f'Email not sent here', 'error')
            return "Only Admins Can Send Emails"


    return jsonify({"Success":"Email Sent"})

def populate_to_users(announcement_obj):
    
    all_users = [user.email for user in User.query.all()]

    print("CHECK EVENT: ",all_users)

    church = all_churches.query.get(current_user.chrch_id)

    usr = admin_user.query.get(current_user.id)

    def send_veri_mail():

        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] = creds.get('email')  # os.getenv("MAIL")
        app.config["MAIL_PASSWORD"] = creds.get('gpass') #os.getenv("PWD")
        app.config["MAIL_DEFAULT_SENDER"] = "noreply@gmail.com"

        mail = Mail(app)

        html_content = f"""<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f6f6f6;
            color: #333;
            padding: 20px;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        h2,h3 {{
            color: #4CAF50;
        }}
        p,li{{font-weight:500;color:#707070 }}
        .footer {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }}
        span{{ font-weight:600;color:coral}}
    </style>
</head>
<body>
    <div class="container">
        <img style="" src="https://yt3.googleusercontent.com/ytc/AIdro_kWhxLUK_wGrRkKhCAr_L_oGH2T1c-HMvF8VW0odpZ80g=s160-c-k-c0x00ffffff-no-rj" />
        <h2>Dear {church.church_name} Member</h2>

        <p>{announcement_obj.info.data}</p>
        <p>email by: {usr.name}, {usr.committee_local_pos} - {usr.committee_local_group}</p>
        <br>
        <p class="footer">Church Announcements!</p>
    </div>
</body>
</html>
"""

         # Create email message
        
        msg = Message(
            subject=announcement_obj.title.data,
            sender=app.config["MAIL_DEFAULT_SENDER"],
            recipients=[],  # Leave recipients empty if using BCC
            bcc=all_users,  # Add all users to BCC to hide recipient info
            html=html_content
        )

        try:
            mail.send(msg)
            flash(f'Emails Sent Successfully', 'success')
            return "Email Sent"
        except Exception as e:
            flash(f'Email not sent here', 'error')
            return "The mail was not sent"

    # try:
    send_veri_mail() 
    # except:


@app.route("/announcements", methods=["POST","GET"])
@login_required
def church_announcements():

    all_announcements = announcements.query.filter_by(chrch_id=current_user.chrch_id).all()
    church = all_churches.query.get(current_user.chrch_id)

    return render_template("church_announcements.html",announcements=all_announcements,church=church,usr=admin_user,
                           generate_whatsapp_link=generate_whatsapp_link)


userr = User
def generate_whatsapp_link(announce, user, church):
    text = None
    encoded_text = None
    try:
        # if userr.role == 'admin_user':
        if userr.query.get(announce.usr_id).committee_local_group:
            text = (
                f"\n*CHURCH ANNOUNCEMENT* \n"
                f"\n*{announce.title}* \n\n"
                f"{announce.info}\n\n"
                f"_By: {userr.query.get(announce.usr_id).name} - _"
                f"_{userr.query.get(announce.edited_by).committee_local_group}_ "
                f"_{userr.query.get(announce.edited_by).committee_local_pos}_\n\n"
                f"*{church.church_name}*\n"
                f"*Contancts:* {church.church_contacts}\n"
                f"*Email:* {church.church_email}\n\n\n"
                f"Shared from: CAMM Sys+\n"
                f"https://camm.churchregistry.org/announcements"
            )
        else:
            text = (
            f"\n*CHURCH ANNOUNCEMENT* \n"
            f"*\n{announce.title}* \n\n"
            f"{announce.info}\n\n"
            f"*{church.church_name}*\n"
            f"*Contancts:* {church.church_contacts}\n"
            f"*Email:* {church.church_email}\n\n\n"
            f"Shared from: CAMM Sys+\n"
            f"https://camm.churchregistry.org/church_announcements"
            )
        
        encoded_text = text.encode('utf-8')

        encoded_text = quote(encoded_text)

        return f"https://wa.me/?text={encoded_text}"
    except:
        return "None"


@app.route("/announcements_form", methods=["POST","GET"])
@login_required
def announcements_form():

    if not current_user.chrch_id:
        flash("Your Account has not been Mapped with any church account yet!")
        log_out()
        return redirect(url_for("home"))

    announcements_form = AnnouncementsForm()
    church = all_churches.query.get(current_user.chrch_id)
    if request.method == "POST":
        announcements_obj = announcements(chrch_id=current_user.chrch_id,usr_id=current_user.id,title=announcements_form.title.data
                ,info=announcements_form.info.data,timestamp = datetime.now(),directed_to=announcements_form.directed_to.data
                ) 
        db.session.add(announcements_obj)
        db.session.commit()

    if announcements_form.emails.data:
        populate_to_users(announcements_form)

    return render_template("announcements_form.html",announcements_form=announcements_form,church=church)


@app.route("/announcements_form_edit", methods=["POST","GET"])
@login_required
def announcements_form_edit():

    announcement = announcements.query.filter_by(chrch_id=current_user.chrch_id,id=ser.loads(request.args.get('anncmnt'))['data']).first()
    announcements_form = AnnouncementsForm(obj=announcement)

    if request.method == "POST":
        announcement.title=announcements_form.title.data
        announcement.info=request.form.get('info')
        announcement.edited_by=current_user.id
        announcement.directed_to=announcements_form.directed_to.data
        announcement.timestamp=datetime.now()
        
        db.session.commit()
        flash("Update was Successful!","success")
        return redirect(url_for("church_announcements"))

    return render_template("announcements_form_edit.html",announcements_form=announcements_form,announcement=announcement)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    with app.app_context():
       db.create_all()
       print("Updating Tables")
    #    generate_and_save_users()
    #    print("Generated and saved 30 random users to the database.")

    app.run(debug=True)

    # Generate and save random users to the database
    