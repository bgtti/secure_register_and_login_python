# Secure Register and Login: Backend template

## Features
User accounts implemented with SQLite, cookies and Flask-Login
Passwords hashed with bcrypt
CSRF protection with Flask-CSRF ----(?)
Email with Flask-Mail
Login/logout/forgot password workflow
Basic HTML Email templates  ----(?)
testing with pytest

## Installation

<details>
   <summary>1. Clone this repository</summary>

> \
> More information on how to clone this repository available at https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
> Use the main branch, which is intended for local development. 
> <br/><br/>

</details>

<details>
   <summary>2. Create a virtual environment</summary>

> \
>
> ```pwsh
> python -m venv env
> ```
>
> Then activate the environment with the following command:
>
> ```pwsh
> .\env\Scripts\activate
> ```
If you are using MacOS: you might want to replace "python" with "python3" when creating a virtual envinronment. 
If you are using windows: you may encounter an error that "running scripts is disabled on this system". In this case, you can run the following command before activating the environment:

```pwsh
Set-ExecutionPolicy Unrestricted -Scope Process
```
More information on how to set up a virtual envinronment on Windows and MacOS on [Python.org ](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#:~:text=To%20create%20a%20virtual%20environment,virtualenv%20in%20the%20below%20commands.&text=The%20second%20argument%20is%20the,project%20and%20call%20it%20env%20).

When you are done with this project, to deactivate the virtual environment, enter the following command:

```pwsh
deactivate
```


> <br/><br/>
</details>

<details>
   <summary>3. Install dependencies</summary>

> \
>
> ```pwsh
> pip install -r requirements.txt
> ```
>
> If you make changes to the project, you can always update the requirements with:
>
> ```pwsh
> pip freeze > requirements.txt
> ```
>
>Or:
> ```pwsh
> python -m pip freeze > requirements.txt
> ```
>
> <br/><br/>

</details>

<details>
   <summary>4. Add an .env file</summary>

> \
>
> Create a .env file inside the Back-End folder and add the following information:
> SECRET_KEY = "your_password"
> JWT_SECRET_KEY = "your_password"
> PEPPER = '["str1", "str2", "str3", "str4", "str5", "str6"]'
> 
> Replace "your_password" with a password of your choice.
> Replace "str1"... with random strings that are 1 to 4 characters long
>
> <br/><br/>

</details>

<details>
   <summary>5. Run the app</summary>

> \
>
> ```pwsh
> python manage.py run
> ```
>
> <br/><br/>

</details>

<details>
   <summary>If you encounter any issues...</summary>

> \
>
> from flask import Flask: where flask is underlined and the error is: "Import "flask" could not be resolved from source".
> This is an issue with the python interpreter that can be easily resolved.
> Check out this answer on [StackOverflow ](https://stackoverflow.com/questions/65694813/import-flask-could-not-be-resolved-from-source-pylance#:~:text=This%20happens%20when%20the%20Python,in%20the%20venv%2Fbin%20directory)
>
> <br/><br/>
>
> Cleaning __pycache__ files: 
> ```pwsh
> Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
> ```
>

</details>

## Docker: redis
You can install redis or install docker and start a redis container.
On Windows, I recommend installing docker: https://docs.docker.com/get-docker/

Then run the following command start a redis via docker:

```pwsh
docker run -p 6379:6379 -it redis/redis-stack:latest

```
This is necessary to use flask-session.
More information flask-session: https://flask-session.readthedocs.io/en/latest/interfaces.html
More information: https://github.com/redis/redis-py


## Running tests
Pytest was used for unit testing.
To run the tests use the following command in the terminal:
```pwsh
pytest
```

testing examples: https://testdriven.io/blog/flask-pytest/

## Pytho quick fuction testing
https://www.online-python.com/

# why flask bcript: https://flask-bcrypt.readthedocs.io/en/1.0.1/

# Password handling
link: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

save tree to text file: tree /f > tree.txt

# prefixing db keys with _:
https://realpython.com/python-double-underscore/#:~:text=In%20general%2C%20you%20should%20use,strict%20rule%20that%20Python%20enforces.

# NEXT STEPS:
https://stackoverflow.com/questions/3759981/get-ip-address-of-visitors-using-flask-for-python
https://flask-limiter.readthedocs.io/en/stable/
https://www.silvaneves.org/deleting-old-items-in-sqlalchemy
https://security.stackexchange.com/questions/222815/should-i-hash-session-ids-before-storing-the-session-contents#:~:text=Regardless%20of%20how%20often%20the,to%20prevent%20session%20fixation%20attacks.

# error that happens when using the program at midnight:
PermissionError: [WinError 32] The process cannot access the file because it is being used by another process: '...\\Backend\\app\\system_logs\\log.txt' -> '...\\Backend\\app\\system_logs\\log.txt.2024-01-09'

This error occurs when the logging system attempts to rotate the log file, but it's unable to do so because another process (possibly your application or some other process) is still holding a reference to the file.

//setting log delay to True now. consider using a library like loguru

//uuid issue: https://www.toomanyafterthoughts.com/uuids-are-bad-for-database-index-performance-uuid7/
// another point of view for uuid: https://betterprogramming.pub/why-i-like-using-uuids-on-database-tables-ccab8c350f8a

# setting up gmail:
Password needs to be app password, not the usual account password
2-factor must be enabled for this: https://support.google.com/mail/answer/185833?hl=en

# https:
It is possible (and probable) that the browser blocks session cookies due to strict thrid-party cooky policy. This will make requests to the server fail.
Make sure you allow third-party cookies for https://127.0.0.1:5000/ (or whichever other port you are runnning this application from). Sometimes this can be done by acessing the address, then clicking to bypass blocking of unsecure sites. 

A folder called ssl_certificate is included along with files that got uploaded to Github. These files will probably not be accepted by your browser, which may still flag the source as unsecure.

If you delete the ssl_certificate folder, the app will re-create it and will try to generate SSL certificate to run HTTPS. Should it fail (which it probably will), this is what can be done:
1) Fix the code and/or install OpenSSL so that the certificate is generated; or
2) Manually place a certificate in the correct folder
3) Run it HTTP (recommended)

1)
Make sure you have OpenSSL inatalled. If you dont, install it.
I got the installation link from this site: https://slproweb.com/products/Win32OpenSSL.html
There is an installation guide for windows here: https://www.xolphin.com/support/OpenSSL/OpenSSL_-_Installation_under_Windows
You can copy the path to your openssl.exe file and paste it in create_ssl_certificate(update=False), replacing the current "openssl_path" variable.
Run the code again. If it still doesn't work, try openssl_path = "openssl". If that doesn't solve the problem then consider another option.
2)
Add a certificate named "cert.pem" and a key named "key.pem" to the ssl_certificate folder manually. 
3)
Just run the code as HTTP. This will happen automatically, but if it does, don't forget to change the API route in the React frontend as well. https://127.0.0.1:5000/ to http://127.0.0.1:5000/ (or whichever port you are runnning this application from). Also here, you may have to the browser third-party-cookie thing as well, an perhaps change a thing or two in the Config file regarding session cookies.


# design choices:
ORM: portability = SQL-Alchemy due to it's support of major relational database engines (SQLite, MySQL, Postgres), ease of use, flask-integration. Performance penalty vs using ODM is negligible. pg60 Flask Web Dev book)

flask-- designed to be extended. some important functionality need external packages, giving freedom of choice on what to use. Example: user authentication and database.

files containing routes or view functions are named 'routes.py' instead of 'views.py' to emphasize the routing aspect, since no specific page is rendered (react takes care of FE, no web templates)

# folder structure
app/__init__ contains the factory function that creates the application (create_app) and is invoked in manage.py.

manage.py is the application script


# resources
PEP257: docstrings at https://peps.python.org/pep-0257/
PEP8: python conventions at https://peps.python.org/pep-0008/



# Auth

OWASP recommendation-based.

## Registration
- Required: Username, Email, Password
- "Users should be permitted to use their email address as a username, provided the email is verified during signup."
- "Additionally, they should have the option to choose a username other than an email address. "




# Email change
Using OWASP's recommendation for "DOES NOT HAVE Multifactor Authentication Enabled":
-Process to be explained to user in advance
-New email given
-Password will be requested
-New email will be temporarily stored
-Route possibilities: 1. Fail: User said email address change was not requested. 2. Fail: New email address not confirmed. 3. Admin made aware of the 2 fails, 4. Success
-Two emails are sent: to old and new email addresses

## TODO Auth:

Email validation:
Notoriosly difficult to validate with regex.

Testing guessable user accounts
Available at: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/04-Testing_for_Account_Enumeration_and_Guessable_User_Account

Email change:
Using OWASP's recommendation for the flow of changing a register user's email address.
Available at: https://owasp.org/www-community/pages/controls/Changing_Registered_Email_Address_For_An_Account

Testing for Weak Password Change or Reset Functionalities
Available at: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/09-Testing_for_Weak_Password_Change_or_Reset_Functionalities


TEST:
(source: owasp: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html#email-address-validation) 
- confirm that registration email does not contain dangerous characters (such as backticks, single or double quotes, or null bytes).
- The domain part contains only letters, numbers, hyphens (-) and periods (.).
- The email address is a reasonable length: he local part (before the @) should be no more than 63 characters., The total length should be no more than 254 characters.
- he links that are sent to users to prove ownership [of email] should be At least 32 characters long., time limited and using a good source of randomness (example: "secrets()): https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html#secure-random-number-generation


Implement:
For example, it would generally not be appropriate to notify a user that there had been an attempt to login to their account with an incorrect password. However, if there had been a login with the correct password, but which had then failed the subsequent MFA check, the user should be notified so that they can change their password. Subsequently, should the user request multiple password resets from different devices or IP addresses, it may be appropriate to prevent further access to the account pending further user verification processes.

Details related to current or recent logins should also be made visible to the user. For example, when they login to the application, the date, time and location of their previous login attempt could be displayed to them. Additionally, if the application supports concurrent sessions, the user should be able to view a list of all active sessions, and to terminate any other sessions that are not legitimate.
For credential stuffig prevention
available at:
https://cheatsheetseries.owasp.org/cheatsheets/Credential_Stuffing_Prevention_Cheat_Sheet.html