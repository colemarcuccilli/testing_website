from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import csv
import os
from flaskapp import database

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'fallback-secret-key'

class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    home_address = StringField('Home Address', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth', validators=[DataRequired()])
    mobile_phone = StringField('Mobile Phone', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired()])
    start_time = StringField('Start Time', validators=[DataRequired()])
    end_time = StringField('End Time', validators=[DataRequired()])
    invitation_text = TextAreaField('Invitation Text', validators=[DataRequired()])
    image_path = StringField('Image Path', validators=[DataRequired()])
    max_attendees = StringField('Maximum Attendees', validators=[DataRequired()])
    planner_name = StringField('Planner Name', validators=[DataRequired()])
    rental_items = TextAreaField('Rental Items', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Submit')

class VenueForm(FlaskForm):
    name = StringField('Venue Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    contact_phone = StringField('Contact Phone', validators=[DataRequired()])
    rental_fee = StringField('Rental Fee', validators=[DataRequired()])
    max_attendees = StringField('Maximum Attendees', validators=[DataRequired()])
    submit = SubmitField('Submit')
    reset = SubmitField('Reset')

def check_person(name, home_address, email, date_of_birth, mobile_phone):
    error=""
    msg=[]
    if not name:
        msg.append("name is missing")
    if len(name) > 20:
        msg.append("name is too long")
    if not home_address:
        msg.append("date is missing")
    if not email:
        msg.append("email is missing")
    if not date_of_birth:
        msg.append("date of birth is missing")
    if not mobile_phone:
        msg.append("mobile phone is missing")
    return error


def check_event(name, date, venue, start_time, end_time, invitation_text, image_path, max_attendees, planner_name, rental_items, notes):
    error=""
    msg=[]
    if not name:
        msg.append("name is missing")
    if len(name) > 20:
        msg.append("name is too long")
    if not date:
        msg.append("date is missing")
    if not venue:
        msg.append("venue is missing")
    if not start_time:
        msg.append("start time is missing")
    if not end_time:
        msg.append("end time is missing")
    if not invitation_text:
        msg.append("invitation text is missing")
    if not image_path:
        msg.append("image path is missing")
    if not max_attendees:
        msg.append("attendees max is missing")
    if not planner_name:
        msg.append("planner name is missing")
    if not rental_items:
        msg.append("rental items are missing")
    if not notes:
        msg.append("notes are missing")
    
    return error

def check_venue(name, address, contact_phone, rental_fee, max_attendees):
    error=""
    msg=[]
    if not name:
        msg.append("name is missing")
    if not address:
        msg.append("address is missing")
    if not contact_phone:
        msg.append("contact number is missing")
    if not rental_fee:
        msg.append("rental fee is missing")
    if not max_attendees:
        msg.append("attendees max is missing")
    return error

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/events/")
@app.route("/events/<event_id>")
def events(event_id=None):
    events_list = database.get_events()  # Use database.get_events
    if event_id:
        event = database.get_event(event_id)
        venue_name = database.get_venue_name(event_id)
        host_details = database.get_host_details(event_id)
        planner_details = database.get_planner_details(event_id)
        return render_template("event.html", event=event, venue_name=venue_name, host_details=host_details, planner_details=planner_details)

    return render_template("events.html", events=events_list)

@app.route("/events/add", methods=['GET', 'POST'])
def add_event(event_id=None):
    form = EventForm()
    if form.validate_on_submit():
        name = form.name.data
        date = form.date.data
        venue = form.venue.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        invitation_text = form.invitation_text.data
        image_path = form.image_path.data
        max_attendees = form.max_attendees.data
        planner_name = form.planner_name.data
        rental_items = form.rental_items.data
        notes = form.notes.data
        error = check_event(name, date, venue, start_time, end_time, invitation_text, image_path, max_attendees, planner_name, rental_items, notes)
        if error:
            event=database.get_event()
            return render_template('event_form.html', name=name, date=date, venue=venue, start_time=start_time, end_time=end_time, invitation_text=invitation_text, image_path=image_path, max_attendees=max_attendees, planner_name=planner_name, rental_items=rental_items, notes=notes)
        database.add_event(name, date, venue, start_time, end_time, invitation_text, image_path, max_attendees, planner_name, rental_items, notes)  # Use database function
        return redirect(url_for('events', event_id=event_id, form=form))
    else:
        event=database.get_event(event_id)
        return render_template("people_form.html", event=event, form=form)

@app.route("/events/<event_id>/edit", methods=['GET', 'POST'])
def edit_event(event_id):
    event = database.get_event_by_name(event_id)  # Use database function
    if event is None:
        flash(f"No event with id {event_id} was found.", "error")
        return redirect(url_for('events'))

    form = EventForm(obj=event)
    if form.validate_on_submit():
        updated_event = {
            'name': form.name.data,
            'date': form.date.data,
            'venue': form.venue.data,
            'start_time': form.start_time.data,
            'end_time': form.end_time.data,
            'invitation_text': form.invitation_text.data,
            'image_path': form.image_path.data,
            'max_attendees': form.max_attendees.data,
            'planner_name': form.planner_name.data,
            'rental_items': form.rental_items.data,
            'notes': form.notes.data
        }
        database.update_event(event_id, updated_event)  # Use database function
        return redirect(url_for('events', event_id=event_id))

    return render_template("event_form.html", form=form, event_id=event_id)

@app.route("/events/<event_id>/delete", methods=['POST'])
def delete_event(event_id):
    event = database.get_event_by_name(event_id)  # Use database function
    if event is None:
        flash(f"No event with id {event_id} was found.", "error")
        return redirect(url_for('events'))

    database.delete_event(event_id)  # Use database function
    flash("Event deleted successfully.", "success")
    return redirect(url_for('events'))

@app.route("/venues/")
def venues():
    venues_list = database.get_venues()  # Use database function
    return render_template("venues.html", venues=venues_list)

@app.route("/people/")
def people():
    people_list = database.get_people()  # Use database function
    return render_template("people.html", people=people_list)

@app.route("/venues/add", methods=['GET', 'POST'])
def add_venue(venue_id=None):
    form = VenueForm()
    if form.validate_on_submit():
        name = form.name.data
        address = form.address.data
        contact_phone = form.contact_phone.data
        rental_fee = form.rental_fee.data
        max_attendees = form.max_attendees.data
        error=check_venue(name, address, contact_phone, rental_fee, max_attendees)
        if error:
            venue=database.get_venues()
            return render_template('venue_form.html', name=name, address=address, contact_phone=contact_phone, rental_fee=rental_fee, max_attendees=max_attendees)
        database.add_venue(name, address, contact_phone, rental_fee, max_attendees)  # Use database function
        return redirect(url_for('venues', venue_id=venue_id))
    else:
        venue=database.get_venues()
        return render_template("venue_form.html", venues=venues, form=form)

@app.route("/people/add", methods=['GET', 'POST'])
def add_person(person_id=None):
    form = PersonForm()
    if form.validate_on_submit():
        
        name = form.name.data,
        home_address = form.home_address.data,
        email = form.email.data,
        date_of_birth = form.date_of_birth.data,
        mobile_phone = form.mobile_phone.data
        error=check_person(name, home_address, email, date_of_birth, mobile_phone)
        if error:
            person=database.get_people()
            return render_template('people_form.html', name=name, home_address=home_address, email=email, date_of_birth=date_of_birth, mobile_phone=mobile_phone)
        database.add_person(name, home_address, email, date_of_birth, mobile_phone)  # Use database function
        return redirect(url_for('people', person_id=person_id))
    else:
        person=database.get_people()
        return render_template("people_form.html", person=person, form=form)


if __name__ == "__main__":
    app.run(debug=True)
