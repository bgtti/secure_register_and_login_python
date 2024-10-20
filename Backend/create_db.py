from flask import current_app
import ast
import redis
from random import randint
from datetime import datetime, timezone
from app.config import ADMIN_ACCT
from app.extensions import db, flask_bcrypt
from app.models.user import User
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper
from app.utils.console_warning.print_warning import console_warn
import os
import shutil
import subprocess

# Data for Admin Account creation:
ADMIN_DATA = ast.literal_eval(ADMIN_ACCT)
ADMIN_NAME = ADMIN_DATA[0]
ADMIN_EMAIL = ADMIN_DATA[1]
ADMIN_PW = ADMIN_DATA[2]
ADMIN_ID = randint(3,300) # admin id will not be 1, but rather a random number

def create_super_admin_acct():
    """
    This function creates the super admin account.
    It is called in manage.py.
    """
    # Check if Super Admin exists in the database, if not, add it:
    super_admin_exists = db.session.query(User).first() is not None
    if not super_admin_exists:
        console_warn("Creating super admin user...", "CYAN")
        date = datetime.now(timezone.utc)
        salt = generate_salt()
        pepper = get_pepper(date)
        salted_password = salt + ADMIN_PW + pepper
        hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
        the_super_admin = User(
            id= ADMIN_ID,
            name=ADMIN_NAME, 
            email=ADMIN_EMAIL, 
            password=hashed_password, 
            salt=salt, 
            created_at=date
            )
        db.session.add(the_super_admin)
        the_super_admin.make_user_super_admin(ADMIN_PW)
        db.session.commit()
        console_warn("...super admin user successfully added!", "CYAN")

# Checking if Redis is running: this is important for flask session to work

def check_redis():
    """
    This function checks if Redis is running.
    -----------------------------------------
    In case it is not running, it will log the information to the terminal in red.
    In case it is running, the terminal log will be displayed in blue.
    """
    try:
        r = redis.Redis(host="localhost", port=6379, db=0)
        r.ping()  # Ping Redis to check if it's running
        console_warn("Redis checked: it is running!")
    except redis.ConnectionError:
        console_warn("Failed to connect to Redis:", "RED")
        console_warn("Flask session relies on Redis to authenticate users. The app may not function correctly.", "MAGENTA")

def create_ssl_certificate(update=False):
    """
    create_ssl_certificate(update:boolean) -> IO
    -----------------------------------------
    This function creates certificate and key files needed to run the app in HTTP.
    Accepts a boolean to "update" which specifies whether existing certificates should be re-generated. Setting to True will result in current certificate deletion.
    -----------------------------------------
    This function is useful in development to avoid session cookies being blocked by browsers due to strict third-party cookie policies.
    It creates a folder named "certificate" and self-creates an SSL certificate and key in it.
    """
    console_warn("Creating SSL certificate...", "CYAN")
    failure_message = "Could not self-generate SLL certificate. Browsers may block session cookies. Solution: you can manually upload the files to the certificate folder."
    # Path to the certificate folder
    try:
        if not os.path.exists(os.path.join(os.getcwd(), "ssl_certificate")):
            # If it doesn't exist, create the folder
            os.makedirs(os.path.join(os.getcwd(), "ssl_certificate"))
            console_warn(f"...certificate directory created at {os.path.join(os.getcwd(), "ssl_certificate")}...", "CYAN")
        else:
            cert_dir = os.path.join(os.getcwd(), "ssl_certificate")

        if os.path.exists(cert_dir) and os.listdir(cert_dir):
            # If the folder exists and is not empty, delete its contents
            if update is True:
                console_warn(f"...updating certificates...", "CYAN")
                for filename in os.listdir(cert_dir):
                    file_path = os.path.join(cert_dir, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Remove file or symbolic link
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Remove directory
            else:
                console_warn(f"...content already available in certificate folder, skipping SSL certificate creation.", "CYAN")
                return

    except Exception as e: 
        console_warn(f"...directory creation failed. Error:{e}", "CYAN")
        console_warn(f"{failure_message}", "RED")
        return 

    try:
        # Generate the SSL certificate and key files
        cert_file = os.path.join(cert_dir, "cert.pem")
        key_file = os.path.join(cert_dir, "key.pem")

        openssl_path = r"C:\Program Files\OpenSSL-Win64\bin\openssl.exe"  # Adjust based on your installation
        #openssl_path = "openssl"  # Try to uncomment this if the above does not work

        subprocess.run([
            openssl_path, "req", "-x509", "-newkey", "rsa:4096",
            "-keyout", key_file, "-out", cert_file,
            "-days", "365", "-nodes",
            "-subj", "/CN=localhost"
        ], check=True)
        console_warn(f"...self-signed certificate generated!", "CYAN")
        return cert_file, key_file
    except subprocess.CalledProcessError as e:
        console_warn(f"...Failed to generate certificate. OpenSSL error: {e.stderr.decode()}", "RED")
    except Exception as e:
        console_warn(f"...Error encountered: {e}", "CYAN")
    console_warn(f"...Unable to execute OpenSSL. Possible cause: OpenSSL not installed or not in Path", "CYAN")
    console_warn(f"{failure_message}", "RED")
    return 