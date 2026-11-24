from flask import Blueprint, render_template, redirect, url_for, request, flash
import calendar
from datetime import date
from flask_login import logout_user, login_required, current_user
from models.conn import db
from models.model.room import Room
from models.model.roomReservation import RoomReservation

calendar_bp = Blueprint('calendar', __name__)


#Gestione visulizzazione del calendario

@calendar_bp.route('/calendar')
@calendar_bp.route('/calendar/<int:year>/<int:month>')
@login_required
def show_calendar(year=None, month=None):

    today = date.today()

    if year is None or month is None:
        year = today.year
        month = today.month

    cal = calendar.Calendar(firstweekday=0)

    weeks = cal.monthdayscalendar(year, month)

    month_name = calendar.month_name[month]

    prev_month = month - 1
    prev_year = year

    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    next_month = month + 1
    next_year = year

    if next_month == 13:
        next_month = 1
        next_year += 1

    return render_template(
        'dashboard/calendar.html',
        weeks=weeks,
        month_name=month_name,
        year=year,
        month=month,
        today=today,
        prev_month=prev_month,
        prev_year=prev_year,
        next_month=next_month,
        next_year=next_year
    )

#Aggiunta di un Attività

@calendar_bp.route('/activity/create', methods=['GET', 'POST'])
@login_required
def create_activity():
    """Route for creating a new activity/reservation."""

    rooms = Room.query.all()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        room_id = request.form.get('room_id', '').strip()

        # Validate required fields
        if not name or not room_id:
            flash('All fields are required!', 'danger')
            return render_template(
                'dashboard/create_activity.html',
                rooms=rooms
            )

        # Validate room ID
        try:
            room_id = int(room_id)
        except (ValueError, TypeError):
            flash('Please select a valid room.', 'danger')
            return render_template(
                'dashboard/create_activity.html',
                rooms=rooms
            )

        # Check if the selected room exists
        room = Room.query.get(room_id)

        if not room:
            flash('The selected room does not exist.', 'danger')
            return render_template(
                'dashboard/create_activity.html',
                rooms=rooms
            )

        new_reservation = RoomReservation(
            name=name,
            room_id=room_id,
            user_id=current_user.id
        )

        try:
            db.session.add(new_reservation)
            db.session.commit()

            flash('Activity created successfully!', 'success')

            return redirect(url_for('calendar.show_calendar'))

        except Exception:
            db.session.rollback()
            flash(
                'An error occurred while creating the activity.',
                'danger'
            )

    return render_template(
        'dashboard/create_activity.html',
        rooms=rooms
    )
