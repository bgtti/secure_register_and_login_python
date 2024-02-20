# secure_register_and_login_python
Flask-React template for secure registration and login of users

This project is under construction, please come back later...

Design for inspiration: https://en.99designs.ch/profiles/kukuhaldy/designs/1290791

## How this template attempts to comply with OWASP top 10

Link: https://wiki.owasp.org/index.php/Top_10_2013-Top_10

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

testing: https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=184s

bleach: https://pypi.org/project/bleach/

check-sheet: https://go.snyk.io/rs/677-THP-415/images/Python_Cheatsheet_whitepaper.pdf

https://snyk.io/plans/

https://www.cloudflare.com/en-gb/learning/security/threats/owasp-top-10/


implementing session:
https://www.youtube.com/watch?v=sBw0O5YTT4Q

testing in flask:
https://www.youtube.com/watch?v=RLKW7ZMJOf4&t=184s

important: https://stackoverflow.com/a/24689738

third-party-cookie issue localhost: https://web.dev/articles/how-to-use-local-https