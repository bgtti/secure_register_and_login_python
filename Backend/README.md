# Secure Register and Login: Backend template


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

# why flas bcript: https://flask-bcrypt.readthedocs.io/en/1.0.1/

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
