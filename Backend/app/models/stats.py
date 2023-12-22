from app.extensions import db
from flask_login import UserMixin
from datetime import datetime
from uuid import uuid4

# helpers:
def get_year():
    return datetime.now().year

def get_month():
    return datetime.now().month

def get_week_num():
    return datetime.date(datetime.utcnow()).isocalendar()[1]

# example: when new user registers:
# 1) check is YearStats.this_year exists for = datetime.now().year
#    a) --> if it does not exist, create column. Then, also create MonthStats belonging to this year and WeekStats belong to this year/month
#    b) --> if it exists, check if MonthStats.this_month exists within this year for = datetime.now().month
#      b.1) if MonthStats.this_month for this year does not exist, then create it and create MonthStats belonging to this month
#      b.2) if MonthStats.this_month for this year exists, then check if it has a WeekStats = datetime.date(datetime.utcnow()).isocalendar()[1]
#          b.2a) if WeekStats = datetime.date(datetime.utcnow()).isocalendar()[1] belonging to this year/month does not exist, create it
# 2) call new_registration in this week's WeekStats. New registrations in year and month stats should also be updated

class BaseStats(UserMixin, db.Model):
    __abstract__ = True
    _this_year = db.Column(db.Integer, nullable=False, default=get_year)
    _new_registrations = db.Column(db.Integer, nullable=False, default=0)
    _new_deregistrations = db.Column(db.Integer, nullable=False, default=0)

    @property
    def this_year(self):
        return self._this_year
    
    @property
    def new_registrations(self):
        return self._new_registrations
    
    @property
    def new_deregistrations(self):
        return self._new_deregistrations
    
    def net_new_users(self):
        return self._new_registrations - self._new_deregistrations

class YearStats(BaseStats):
    __tablename__ = "year_stats"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    _monthly_stats = db.relationship('MonthStats', backref='year_stats', lazy='dynamic', cascade='all, delete-orphan')
    _weekly_stats = db.relationship('WeekStats', backref='year_stats', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Year Stats {self._this_year}: + {self._new_registrations} - {self._new_deregistrations} registered users>"


class MonthStats(BaseStats):
    __tablename__ = "month_stats"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    _this_month = db.Column(db.Integer, nullable=False, default=get_month)
    _weekly_stats = db.relationship('WeekStats', backref='year_stats', lazy='dynamic', cascade='all, delete-orphan')
    _year_stats_id = db.Column(db.Integer, db.ForeignKey('year_stats.id'))
    
    def __repr__(self):
        return f"<Month Stats {self._this_month}: + {self._new_registrations} - {self._new_deregistrations} registered users>"

    @property
    def this_month(self):
        return self._this_month

class WeekStats(BaseStats):
    __tablename__ = "week_stats"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    _this_month = db.Column(db.Integer, nullable=False, default=get_month)
    _this_week = db.Column(db.Integer, nullable=False, default=get_week_num)
    _year_stats_id = db.Column(db.Integer, db.ForeignKey('year_stats.id'))
    _month_stats_id = db.Column(db.Integer, db.ForeignKey('month_stats.id'))
    
    def __repr__(self):
        return f"<Week Stats {self._this_week}: + {self._new_registrations} - {self._new_deregistrations} registered users>"

    @property
    def this_month(self):
        return self._this_month
    
    @property
    def this_week(self):
        return self._this_week
    
    def update_month_and_year_stats(self, registration=True):
        if registration:
            self.month_stats_id._new_registrations += 1
            self.year_stats_id._new_registrations += 1
        else:
            self.month_stats_id._new_deregistrations += 1
            self.year_stats_id._new_deregistrations += 1
        db.session.commit()
    
    def new_registration(self):
        self._registered_this_week += 1
        self.update_month_and_year_stats(registration=True)
    
    def new_deregistration(self):
        self._deregistered_this_week += 1
        self.update_month_and_year_stats(registration=False)