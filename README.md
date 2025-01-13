<div align="center">
  <br>
  <h1><b>Oops... Project not ready!</b></h1>
  <strong>This is still a work in progress</strong>
  <strong>Please come back later!</strong>
</div>
<br>
<br>
<hr>
<hr>
<div align="center">
  <p><b>...</b></p>
</div>
<hr>
<hr>
<br>
<div align="center">
  <br>
  <h2><b>Project brainstorming bellow</b></h2>
  <strong>Warning: messy read.me ahead...</strong>
</div>
<br>
<hr>
<hr>
<br>

<div align="center">
  <br>
  <h1><b>secure_register_and_login_python</b></h1>
  <strong>Flask-React software template for user registration and admin portal</strong>
</div>
<br>

## Table of Contents

- [Overview](#overview)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [Objectives](#objectives)
- [Features](#features)
    - [Features table](#features-table)
    - [Todo list](#todo-list)
- [About](#about)
    - [Recommended Resources](#recomended-resources)
    - [Sources used](#sources-used)

## Overview
This app can be used as a template for React/Flask softwares that require the following features:
- Base webpage with:
    - Homepage
    - Contact page
    - Signup/Login pages for users
    - User dashboard
    - User settings (with options for account management and recovery)
- Authentication features such as:
    - Account registration and deletion
    - Credential changes (password and email)
    - Account recovery (resetting passwords, changing emails)
    - Safety features: account verification and multi-factor authentication
    - Password and OTP login options
- Admin portal including
    - Admin dashboard
    - User management
    - Admin account management
    - Contact form management

The project contains two base folders:
- **Backend**: contains the Flask application that manages server, cookies, email templates, and routes
- **Frontend**: containing the React app that manages client routes

### Backend
The Flask application makes use of:
- SQLAlchemy ORM to interact with SQLite
- Flask-Limiter adds rate limiting to the routes
- Flask-Mail is used to facilitate email sending
- Flask-Login manages user sessions
- Redis used for session storage
- Json Schema is used to check data consistency and validity
- Pytest was chosen for testing

...and other useful extensions to Flask.

It relies on server-side cookies to ease authentication, and has custom decorators for easy data validation and resource authorization.

When running the project for the first time, the database will be created and seeded to enable the testing of core functionalities. A super admin should also be created.


### Frontend
The react app uses:
- Redux to manage storage
- React router to manage paths and navigation

No CSS library is used, a CSS reset file was created, and only basic styling was applied. This way, it can be easily adapted to use whichever CSS framework is prefered for your project.

The application communicates with the backend through api handlers, separating api calls from the UI.

### Objectives
The main objective of this project is to be a safe base template to be used to quickly build a proof of concept software project - to reduce the time to market and development of basic features required by many projects out there.

Whenever possible, [OWASP (Open Source Foundation for Application Security)](https://owasp.org/) guides were used when developing the project and follow best practices, especially when auth features were being designed.


## Features

The frontend features can be summarized under the following categories:
- Website pages: are unprotected and could be accessed by any person. Example: Home page, contact page, error page.
- User pages: are protected, and only registered users have access. Example: Dashboard, Account settings.
- Admin pages: are the admin dashboard, and only admin users are authorized access. Admins can see and manage users, see incomming messages from the contact form and respond to them, and have basic information about usage.

### Features Table

<table style="border-collapse:separate;">
    <tr>
    <th style="background: #344955; border-radius:20px; border: 5px solid transparent"><small><b>Feature</b></small></th>
    <th style="background: #344955; border-radius:20px"><small><b>Functionality</b></small></th>
    <th style="background: #344955; border-radius:20px"><small><b>Status</b></small></th>
    <th style="background: #344955; border-radius:20px"><small><b>Notes</b></small></th>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent"><small><b>Website pages</b></small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>⤵</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>⤵</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>⤵</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>Page: Home</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>small adjustments needed</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>Page: Signup</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>Page: Login</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center"></td>
    <td style="background: #344955; border-radius:20px"><small> ↪ login using OTP</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center"></td>
    <td style="background: #344955; border-radius:20px"><small> ↪ login using password</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center"></td>
    <td style="background: #344955; border-radius:20px"><small> ↪ login using MFA</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>Page: Contact</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center"></td>
    <td style="background: #344955; border-radius:20px"><small> ↪ contact form</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>small adjustments needed</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>Page: Reset password</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>Page: Error</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent"><small><b>User pages</b></small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>⤵</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>⤵</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>⤵</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>Page: Dashboard</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>Settings</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
   <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center"></td>
    <td style="background: #344955; border-radius:20px"><small> ↪ Credential change (name/email/password)</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center"></td>
    <td style="background: #344955; border-radius:20px"><small> ↪ Account verification</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center"></td>
    <td style="background: #344955; border-radius:20px"><small> ↪ Recovery email settings</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center"></td>
    <td style="background: #344955; border-radius:20px"><small> ↪ Multi-factor Auth enabling</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center"></td>
    <td style="background: #344955; border-radius:20px"><small> ↪ Account deletion</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center"></td>
    <td style="background: #344955; border-radius:20px"><small> ↪ Account preferences: Mailing list sbscription</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center"></td>
    <td style="background: #344955; border-radius:20px"><small> ↪ Account preferences: Night mode</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>CSS adaptation required</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center"></td>
    <td style="background: #344955; border-radius:20px"><small>↪ Account activity: view activity logs</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center; color: red;"><small>✘</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>missing</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>Page: Messages</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center; color: red;"><small>✘</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>missing: should view support messages</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>Log out</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent"><small><b>Admin pages</b></small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>⤵</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>⤵</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>⤵</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>users overview (table)</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>view user info</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>view user activity logs</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>test again</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>view user messages</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center; color: red;"><small>✘</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>only placeholder page</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>delete user</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>make sure admins cant be deleted</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>block user</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>make sure admins cant be blocked</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>make user admin</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>flag user</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small>-</small></td>
  </tr>
  <tr>
    <td style="background: #344955; border-radius:20px; border: 5px solid transparent; text-align: center">↪</td>
    <td style="background: #344955; border-radius:20px"><small>messages</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center;"><small>✔</small></td>
    <td style="background: #344955; border-radius:20px; text-align: center"><small></small></td>
  </tr>
</table>

### TODO list

#### Backend
→ Unit and functional testing<br>
→ Cleaning up and improving Config files<br>
→ Certificates and HTTPS usage proper configuration<br>
→ User roles should be placed in a db table and proper access management introduced<br>

#### Frontend
→ Messages table - pagination and filter improvement<br>
→ Jest testing implementation<br>

#### Both
→ Improved messaging and customer support functionality<br>
→ User activity logs and history<br>


## About
This template was idealized while the author was taking the course [CS50's Introduction to Cybersecurity](https://pll.harvard.edu/course/cs50s-introduction-cybersecurity) from Hardvard University offered through [EdX](https://www.edx.org/learn/cybersecurity/harvard-university-cs50-s-introduction-to-cybersecurity). The idea was to translate the course teachings to code, and make use of best practices. 

The author tried her best to follow [OWASP (Open Source Foundation for Application Security)](https://owasp.org/) recommendations when developing this project whenever possible. OWASP publishes yearly the Top 10 Web Appication Security Risks which should be the start of a process of acknowledging security risks and implementing necessary processes to write better and more secure code. The organization also offers numerous guidelines and information sheets of various topics to educate developers and guide them to build better software.

**No guarantees** are made as to the functioning, quality, or security of it's app and code by the author. You are welcome to use this template as you see fit - at your own risk.

### Recomended resources
- [OWASP's top 10] (https://wiki.owasp.org/index.php/Top_10_2013-Top_10)
- [Cloudfare article](https://www.cloudflare.com/en-gb/learning/security/threats/owasp-top-10/) about OWASP top 10

How to...
- Testing in flask youtube video from [Pretty Printed](https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=184s)
- Implement sessions youtube video from [DevGuyAhnaf](https://www.youtube.com/watch?v=sBw0O5YTT4Q)

Useful to know...
- Access-Control-Allow-Credentials header / CORS from a [Stackflow answer](https://stackoverflow.com/a/24689738)
- Using HTTPS for local development is an article from [Maud Nalpas in web.dev](https://web.dev/articles/how-to-use-local-https) talking about third-party cookies and local host issues

Great cheat-sheets...
- VS Code users will find this ["Keyboard reference sheet"](https://code.visualstudio.com/docs/getstarted/tips-and-tricks) useful

### Sources used
- This app's UI's design was inspired by [kukuhaldy in 99designs](https://en.99designs.ch/profiles/kukuhaldy/designs/1290791)


<br>
<hr>
Messy part ahead
<hr>
<br>




### Conventions & stuff to keep in mind while developing:
→ Seed: Seeding in the context of web development and databases refers to the process of populating a database with initial data. Used for initial setup, make testing easier, and demo purposes<br>
→ User Roles: e.g., "admin," "user," "guest."<br>
→ worker.py file: comonly used for background tasks such as backups, cleanups, notifications, sumarizing logs 

check out:
https://github.com/realpython/flask-by-example/blob/master/config.py




## How this template attempts to comply with OWASP top 10


### 1. Injection
Injection attacks can be prevented by validating and/or sanitizing user-submitted data. SQL injection attack prevention includes sanitizing string inputs.

To check for type and length of value JSON Schema is being used. No raw SQL queries were performed, and SQLAlchemy was chosen as an ORM that offers some protection against SQL injections (SQLAlchemy parametizes input data under the hood).

Example:

```python 
name = json_data["name"]
user_exists = User.query.filter_by(_email=email).first() is not None
```

The filter_by method should automatically escape and sanitize the input. 

Sources to check out:
https://www.educative.io/answers/how-to-sanitize-user-input-in-python (html escaping)
https://www.scaler.com/topics/escape-string-python/

"Bleach is an allowed-list-based HTML sanitizing library that escapes or strips markup and attributes."
bleach: https://pypi.org/project/bleach/



### 2. Broken authentication
Implemented:
- rate-limiting

not implemented:
-two-factor auth

### 3. Sensitive data exposure
Implemented:
- encryption of password
- no feedback given when log-in fails, or password reset (should not be possible for FE to see whether user is actually registered)

### 4. XSS Cross-site scripting
.... not allowing users to post links?
sanitizing user input..

### 5. Missing Function Level access control
Checking access rights in BE function and not only FE.

### 6. Security logging and monitoring failures
Logging of key actions:
- auditable events: logins, failed logins
- warnings and errors
Monitoring for suspiscious activity:
- flagging user with multiple attempted logins..?
- unusual traffic...? odd traffic origin..?
- allow user reporting of unusual behaviour...?
- appropriate alerting threshholds...?

Check the following:
"Penetration testing and scans by dynamic application security testing (DAST) tools (such as OWASP ZAP) do not trigger alerts.

The application cannot detect, escalate, or alert for active attacks in real-time or near real-time."
Source: https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/
How to use ZAP: https://www.youtube.com/watch?v=QJ5u_dHwoAk

## Other safety or best practices features
### 1. Battling bot traffic
Abusive bots can slow down a website and higher hosting costs by consuming server badwidth and resources. 
What was implemented:
- Honey trap

What was not implemented, but could help here as well:
- CAPTCHA

## Check out: useful links

Python security best practices:
check-sheet: https://go.snyk.io/rs/677-THP-415/images/Python_Cheatsheet_whitepaper.pdf

Code checker:
https://snyk.io/plans/



