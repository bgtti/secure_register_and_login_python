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
    # _weekly_stats = db.relationship('WeekStats', backref='year_stats', lazy='dynamic', cascade='all, delete-orphan')
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
    # _month_stats_id = db.Column(db.Integer, db.ForeignKey('month_stats.id'))
    
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
            # self.month_stats_id._new_registrations += 1
            self.year_stats_id._new_registrations += 1
            # find month and update registration....
            # self.year_stats_id._monthly_stats._new_registrations += 1
        else:
            # self.month_stats_id._new_deregistrations += 1
            self.year_stats_id._new_deregistrations += 1
            # find month and update deregistration....
            #self.year_stats_id._monthly_stats._new_deregistrations += 1
        db.session.commit()
    
    def new_registration(self):
        self._registered_this_week += 1
        self.update_month_and_year_stats(registration=True)
    
    def new_deregistration(self):
        self._deregistered_this_week += 1
        self.update_month_and_year_stats(registration=False)


#####################################################################
"""
Statistics to analyse site visitors and users to understand base group geolocation, devices used, and referrer sites. This is important for admins to adapt their content and measure the reach and success of their apps. At the same time, respecting user's privacy and data is very important.

This is the reason no third-party solution was used here, and a lot of care was taken to develop a way of keeping statistics and user data separated, and keeping enough information to be able to analyze site usage while not monitoring the users.

What is measured:
- General geographical location (why? example: to determine where your server should be located)
- Size of the device used (why? example: to decide whether to invest more in usability for mobile devices)
- Referrer site (why? example: to understand if your ad campaign is working)
- Unique visitors (why? example: to understand if your reach is growing)
- Registration (signups)/ Deregistration (account deletion) (why? example: measure conversion or churn rate)

How is it measured:
The most precise would be to use geolocation - that needs user's express permission and many are scared to give it.
The two other options are cookies and ip addresses. Cookies have received a bad reputation, and are widely being blocked and deleted. IP addresses may suffer from the lack of accuracy, and will likely not yield the exact location (especially when in a public network or using VPNs). Balacing pros and cons, the decision was to us IP addresses (especially due to simplicity) to provide insights on geolocation and unique visitors. Admins should keep in mind the data will not be the most accurate.

IP addresses are anonymized before being stored. This reduces the accuracy of geolocation and unique visitors, but no personal identifiable information is truly stored.
"""

class VisitorStats(UserMixin, db.Model):
    __tablename__ = "visitor_stats"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    _ip_address = db.Column(db.String(250), nullable=True)
    _continent = db.Column(db.String(25), nullable=True)
    _country = db.Column(db.String(90), nullable=True)
    _country_code = db.Column(db.String(3), nullable=True)
    _city = db.Column(db.String(180), nullable=True)
    _user_agent = db.Column(db.String(200), nullable=True)
    _os = db.Column(db.String(50), nullable=True)
    _screen_size = db.Column(db.String(15), nullable=True)
    _referrer = db.Column(db.String(100), nullable=True)
    _page_accessed = db.Column(db.String(50), nullable=True)
    _session_visit = db.Column(db.String(32), nullable=True, default="")
    _date_accessed = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, ip_address, continent, country, country_code, city, user_agent, os, screen_size , referrer, page_accessed, session_visit, **kwargs):
        self._ip_address = ip_address
        self._continent = continent
        self._country = country
        self._country_code = country_code
        self._city = city
        self._user_agent = user_agent
        self._os = os
        self._screen_size = screen_size
        self._referrer = referrer
        self._page_accessed = page_accessed
        self._session_visit = session_visit
    
    def __repr__(self):
        return f"<Visitor Stats {self._ip_address}>"
    
    @property
    def continent(self):
        return self._continent
    
    @property
    def country(self):
        return self._country
    
    @property
    def country_code(self):
        return self._country_code
    
    @property
    def city(self):
        return self._city