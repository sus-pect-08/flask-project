
from flask import Blueprint, render_template
import calendar
from datetime import date

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendar')
@calendar_bp.route('/calendar/<int:year>/<int:month>')
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
