from flask import Flask,render_template,url_for,redirect,request,flash,jsonify,session,send_file,Blueprint
from flask_login import login_user, LoginManager,current_user,logout_user, login_required

from models import *



financials_bp = Blueprint('financial_reports', __name__)