import os
import redis
import shutil
import subprocess
from datetime import datetime, timezone
from utils.print_to_terminal import print_to_terminal
from config.values import SUPER_USER
from seeds.seed_all import seed_database
from app.extensions import db, flask_bcrypt
from app.models.user import User
from app.utils.salt_and_pepper.helpers import generate_salt, get_pepper

# TODO: make ssl cert creation not necessary

# Creating Super Admin Account
def create_super_admin_acct():
    """
    This function creates the super admin account.
    It is called in manage.py.
    """
    # Check if Super Admin exists in the database, if not, add it:
    super_admin_exists = db.session.query(User).first() is not None
    if not super_admin_exists:
        print_to_terminal("Creating super admin user...", "CYAN")
        date = datetime.now(timezone.utc)
        salt = generate_salt()
        pepper = get_pepper(date)
        salted_password = salt + SUPER_USER["password"] + pepper
        hashed_password = flask_bcrypt.generate_password_hash(salted_password).decode('utf-8')
        the_super_admin = User(
            name=SUPER_USER["name"], 
            email=SUPER_USER["email"], 
            password=hashed_password, 
            salt=salt, 
            created_at=date
            )
        db.session.add(the_super_admin)
        the_super_admin.make_user_super_admin(SUPER_USER["password"])
        db.session.commit()
        print_to_terminal("...super admin user successfully added!", "CYAN")

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
    except redis.ConnectionError:
        print_to_terminal("Failed to connect to Redis:", "RED")
        print_to_terminal("Flask session relies on Redis to authenticate users. The app may not function correctly.", "MAGENTA")

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
    failure_message = "Could not self-generate SLL certificate. Browsers may block session cookies. Solution: you can manually upload the files to the certificate folder."
    # Path to the certificate folder
    try:
        if not os.path.exists(os.path.join(os.getcwd(), "certs")):
            print_to_terminal("Creating certs directory...", "CYAN")
            # If it doesn't exist, create the folder
            os.makedirs(os.path.join(os.getcwd(), "certs"))
            print_to_terminal(f"...certificate directory created at {os.path.join(os.getcwd(), "certs")}...", "CYAN")
        else:
            cert_dir = os.path.join(os.getcwd(), "certs")

        if os.path.exists(cert_dir) and os.listdir(cert_dir):
            # If the folder exists and is not empty, delete its contents
            if update is True:
                print_to_terminal(f"...updating certificates...", "CYAN")
                for filename in os.listdir(cert_dir):
                    file_path = os.path.join(cert_dir, filename)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Remove file or symbolic link
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Remove directory
            else:
                return

    except Exception as e: 
        print_to_terminal(f"...directory creation failed. Error:{e}", "CYAN")
        print_to_terminal(f"{failure_message}", "RED")
        return 

    try:
        print_to_terminal("Creating SSL certificate...", "CYAN")
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
        print_to_terminal(f"...self-signed certificate generated!", "CYAN")
        return cert_file, key_file
    except subprocess.CalledProcessError as e:
        print_to_terminal(f"...Failed to generate certificate. OpenSSL error: {e.stderr.decode()}", "RED")
    except Exception as e:
        print_to_terminal(f"...Error encountered: {e}", "CYAN")
    print_to_terminal(f"...Unable to execute OpenSSL. Possible cause: OpenSSL not installed or not in Path", "CYAN")
    print_to_terminal(f"{failure_message}", "RED")
    return 

def initial_setup(environment):
    """
    initial_setup(environment: str) -> None
    ----------------------------------------

    Pass the environment to initial_setup (exemple: "development" or "production") for the script to run accordingly.

    The function will create the super admin account. In case this app is not running in production, the script will also seed the database, check whether redis is running, and create ssl certificates if needed.

    This function should be called only once: in *manage.py* after the app has been created and the db has been initiated.
    """
    create_super_admin_acct()
    if environment != "production":
        seed_database()
        check_redis()
        create_ssl_certificate()
