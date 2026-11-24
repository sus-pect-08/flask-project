from flask import Blueprint, render_template, redirect, url_for, request, flash
import calendar
from datetime import date
from flask_login import logout_user, login_required, current_user
from models.conn import db
from models.model.User import User
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
    rooms = Room.query.all()
    users = User.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        detail = request.form.get('detail')
        room_id = request.form.get('room_id')
        participant_ids = request.form.getlist('participant_ids')

        if not name or not room_id:
            flash('Name and Room are required!', 'danger')
            return render_template('dashboard/newActivity.html', rooms=rooms, users=users)

        try:
            new_reservation = RoomReservation(
                name=name,
                detail=detail,
                room_id=int(room_id),
                admin_id=current_user.id
            )

            if participant_ids:
                selected_users = User.query.filter(User.id.in_(participant_ids)).all()
                new_reservation.participants = selected_users

            db.session.add(new_reservation)
            db.session.commit()
            flash('Activity created successfully!', 'success')
            return redirect(url_for('calendar.show_calendar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating activity: {e}', 'danger')

    return render_template('dashboard/newActivity.html', rooms=rooms, users=users)