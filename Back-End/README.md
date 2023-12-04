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

</details>

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