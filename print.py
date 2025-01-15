
from flask import Flask,render_template,url_for,redirect,request,flash,jsonify,session,send_file,Blueprint
from flask_login import login_user, LoginManager,current_user,logout_user, login_required

from models import *



print_bp = Blueprint('print', __name__)


@print_bp.route("/print_stats", methods=["POST","GET"])
@login_required
def print_stats():
    from app import stats

    tr_data = ["Year","Members","Males","Females","Fathers","Mothers","Youth","Children","Married","Single","Single(Engaged)","Employed","Self-Employed"
               "Unemployed","Praise Team","Ushers","Band","Cleaners"]
    
    members_stats,males,females,own_bossess,youth,fathers,mothers,children,no_job,single,single_engaged,married,employed,praise_team,ushers_team,band,cleaner = stats()

    return render_template("print_stats.html",members_stats=members_stats,males=males,
                           females=females,own_bossess=own_bossess,praise_team=praise_team,ushers_team=ushers_team,band=band,
                           no_job=no_job,employed=employed,youth=youth,fathers=fathers,mothers=mothers,children=children,
                           single=single,single_engaged=single_engaged,married=married,cleaner=cleaner,tr_data=tr_data)


def generate_report_data():

    offering=[]
    off_months=None
    

    tr_data = ["Date","Freewill","Tithes","Building","Outreach"]
    filter_item = request.args.get("fltr")
    insp_offerings = offerings.query.filter_by(chrch_id=current_user.chrch_id).all()

    if insp_offerings:
        off_months = { obj.timestamp.strftime("%B") for obj in  insp_offerings}

    if filter_item:
        offering = [ obj for obj in offerings.query.filter_by(chrch_id=current_user.chrch_id).all() if obj.timestamp.strftime("%B") == filter_item ]
    else:
        offering = [ obj for obj in offerings.query.filter_by(chrch_id=current_user.chrch_id).all() if obj.timestamp.strftime("%B") == datetime.now().strftime("%B") ]


    freewill_ttl = sum([float(freewl.freewill) for freewl in offering if freewl.freewill is not None])
    tithes_ttl = sum([float(tths.tithes) for tths in offering if tths.tithes is not None])
    building_ttl = sum([float(blng.building) for blng in offering if blng.building is not None])
    outreach_ttl = sum([0, 0])  # Assuming outreach_ttl is always [0, 0]
    all_total = freewill_ttl + tithes_ttl + building_ttl + outreach_ttl


    return offering, tr_data, off_months, freewill_ttl, tithes_ttl, building_ttl , outreach_ttl, all_total


@print_bp.route('/offering_report',methods=["POST","GET"])
@login_required
def offering_printv():
    
    offering, tr_data, off_months,  freewill_ttl, tithes_ttl, building_ttl, outreach_ttl, all_total = generate_report_data()

    print("Checks Months: ",off_months,tr_data)

    return render_template("report.html", offering=offering,tr_data=tr_data,off_months=off_months,
                           freewill_ttl=freewill_ttl,tithes_ttl=tithes_ttl,building_ttl =building_ttl,outreach_ttl=outreach_ttl,
                           all_total=all_total)


@print_bp.route('/offering_justprint')
@login_required
def offering_justprint():

    offering, tr_data, off_months,  freewill_ttl, tithes_ttl, building_ttl, outreach_ttl, all_total = generate_report_data()

    return render_template("just_print_off.html", offering=offering,tr_data=tr_data,off_months=off_months,
                           freewill_ttl=freewill_ttl,tithes_ttl=tithes_ttl,building_ttl =building_ttl,outreach_ttl=outreach_ttl,
                           all_total=all_total)


@print_bp.route('/print_pledges')
@login_required
def print_pledges():

    tr_data = ["Date","Name", "Pledge Amount", "Paid"]

    all_pledges = pledges.query.filter_by(chrch_id=current_user.chrch_id).all()
    pledge_pocket = open_pledges.query.filter_by(chrch_id=current_user.chrch_id,open=True).first()

    print("PLEDGE: ", pledge_pocket)

    total = sum([total.amount for total in all_pledges if total.open_pledge_id == pledge_pocket.id])

    return render_template("print_pledges.html",all_pledges=all_pledges,tr_data=tr_data,usr=User,total=total,pledge_pocket=pledge_pocket)


@print_bp.route('/print_announcement')
@login_required
def print_announcement():
   announcement=None
   announce_item = request.args.get("item")

   all_announce = announcements.query.filter_by(chrch_id=current_user.chrch_id).all()

   if announce_item:
        announcement = announcements.query.filter_by(chrch_id=current_user.chrch_id,title=announce_item).first()
   else:
       announcement = announcements.query.filter_by(chrch_id=current_user.chrch_id).order_by(announcements.timestamp.desc()).first()

   return render_template("print_announce.html",announcement=announcement,usr=admin_user,all_announce=all_announce)


@print_bp.route('/calender_report',methods=["POST","GET"])
@login_required
def calender_report():

    tr_data = ["Event","Date","End Date","Time","Days","Venue","Month"]
    
    calender_evnts = calender.query.filter_by(chrch_id=current_user.chrch_id).all() 

    for event in calender_evnts:
        if event.end_date:
            event.duration_days = (event.end_date - event.start_date).days + 1
        else:
            event.duration_days = None  # or some default value if end_date is not available

    return  render_template("print_calender.html", calender_evnts = calender_evnts,tr_data=tr_data)
