from app.extensions import db
from flask_login import UserMixin
from datetime import datetime
from hashlib import sha256
from uuid import uuid4
import warnings
import logging

"""
NOTE ABOUT STATS

Statistics rely on 2 database tables: user and visitor stats, and the analytics of this content is shown to admin only.

Statistics to analyse site visitors and users to understand base group geolocation, devices used, and referrer sites are important for admins to adapt their content and measure the reach and success of their apps. At the same time, respecting user's privacy and data is very important.

No third-party analytics solution was used to make sure users' behaviour is not monitored or tracked.
The stats module aims to offer enough information for analysis while not storing information that can be used to distinguish or trace the individual's identity.

What is measured:
- General geographical location (why? example: to determine where your server should be located)
- Size of the device used (why? example: to decide whether to invest more in usability for mobile devices)
- Referrer site (why? example: to understand if your ad campaign is working)
- Unique visitors (why? example: to understand if your reach is growing)
- Registration (signups)/ Deregistration (account deletion) (why? example: measure conversion or churn rate)

How is it measured:
The most precise would be to use geolocation - that needs user's express permission and many are scared to give it.
The two other options are cookies and ip addresses:
- Cookies have received a bad reputation as many in the web used them to track online behaviour accross sites and gather personal information - which lead to users often blocking or deleting them.  
- IP addresses may suffer from the lack of accuracy, and will likely not yield the exact location (especially when in a public network or using VPNs). 
Balacing pros and cons, the decision was to use IP addresses (especially due to simplicity) to provide insights on geolocation and unique visitors. Admins should keep in mind the data will not be the most accurate (not only regarding geolocation, but also unique visitors, since two visitors using the same IP address may be counted as 1, added to the fact only anonymized IPs are stored - which reduces accuracy further). All in all, there is no perfect solution, but the data collected should yield a decent base for analysis.
"""

# helpers:
def get_year():
    return datetime.now().year

def get_month():
    return datetime.now().month

def get_week_num():
    return datetime.date(datetime.utcnow()).isocalendar()[1]

# UserStats is meant to help the admin to measure user growth and understand where their users are based.
# Care was taken not to include a datestamp, so that location information is not linked to a single user.
# new_user is 1 for a new signup and -1 for a new account deletion

class UserStats(UserMixin, db.Model):
    """
    For use in signup and account deletion only.
    (routes in the "account" module)
    --------------------------------------------
    Example usage for signup:
    new_signup = UserStats(new_user=1,country="Brazil")
    
    Example usage for account deletion:
    new_deletion = UserStats(new_user=-1,country="Germany")
    """
    __tablename__ = "user_stats"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    _year = db.Column(db.Integer, nullable=False, default=get_year)
    _month = db.Column(db.Integer, nullable=False, default=get_month)
    _week = db.Column(db.Integer, nullable=False, default=get_week_num)
    _new_user = db.Column(db.Integer, nullable=False, default=0)
    _country = db.Column(db.String(90), nullable=True)

    def __init__(self, new_user, country, **kwargs):
        self._new_user = new_user
        self._country = country
    
    def __repr__(self):
        return f"<User stats: {self._new_user} from {self._country} in {self._year} week {self._week}>"
    @property
    def year(self):
        return self._year
    
    @property
    def month(self):
        return self._month
    
    @property
    def week(self):
        return self._week
    
    @property
    def new_user(self):
        return self._new_user
    
    @property
    def country(self):
        return self._country


class VisitorStats(UserMixin, db.Model):
    """
    Used to measure general page hits.
    Site visitors get a session cookie that allows 
    page views to be grouped in 1 session.
    (routes in the "stats" module)
    -------------------------------------------------
    Important note:
    Check ip and anonymize it before adding them here.
    Ips will automatically be hashed before stored.
    -------------------------------------------------
    Example usage:

    from app.utils.ip_utils.ip_anonymization import anonymize_ip
    anonymized_ip = anonymize_ip(client_ip)

    new_page_hit = VisitorStats(
            ip_address=anonymized_ip, 
            continent="Europe",
            country="Switzerland",
            country_code="CH",
            city="Cham",
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
            os="Android",
            screen_size=(375 × 812),
            referrer="https://example.com/page?q=123",
            page_accessed="home",
            session_visit = uuid4().hex
    )
    
    """
    __tablename__ = "visitor_stats"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    _ip_address = db.Column(db.String(250), nullable=True)
    _continent = db.Column(db.String(25), nullable=True)
    _country = db.Column(db.String(90), nullable=True)
    _country_code = db.Column(db.String(3), nullable=True)
    _city = db.Column(db.String(180), nullable=True)
    _user_agent = db.Column(db.String(250), nullable=True)
    _screen_size = db.Column(db.String(15), nullable=True)
    _referrer = db.Column(db.String(100), nullable=True)
    _page_accessed = db.Column(db.String(50), nullable=True)
    _session_visit = db.Column(db.String(32), nullable=True, default="")
    _date_accessed = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, ip_address, continent, country, country_code, city, user_agent, screen_size , referrer, page_accessed, session_visit, **kwargs):
        self._ip_address = self.check_and_hash_ip(ip_address)
        self._continent = continent
        self._country = country
        self._country_code = country_code
        self._city = city
        self._user_agent = user_agent
        self._screen_size = screen_size
        self._referrer = referrer
        self._page_accessed = page_accessed
        self._session_visit = session_visit
    
    def __repr__(self):
        return f"<Visitor Stats {self._ip_address}>"
    
    @property
    def ip_address(self):
        return self._ip_address
    
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
    
    @property
    def user_agent(self):
        return self._user_agent
    
    @property
    def screen_size(self):
        return self._screen_size
    
    @property
    def referrer(self):
        return self._referrer
    
    @property
    def page_accessed(self):
        return self._page_accessed
    
    @property
    def session_visit(self):
        return self._session_visit
    
    @property
    def date_accessed(self):
        return self._date_accessed
    
    def check_and_hash_ip(self, ip_address):
        # check if ip is not None or empty before performing operation:
        if ip_address and ip_address !="":
            try:
                hash_ip = sha256(ip_address.encode('utf-8')).hexdigest()
                return hash_ip
            except Exception as e:
                logging.info(f"Failed to hash ip before db storage. Error: {str(e)}")
        return ip_address 

