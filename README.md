# EveHolder

[![EveGroup](https://circleci.com/gh/EveGroup/EveHolder.svg?style=svg)](https://app.circleci.com/pipelines/github/EveGroup/EveHolder)
[![codecov](https://codecov.io/gh/EveGroup/EveHolder/branch/master/graph/badge.svg?token=IYHFBSLOV7)](https://codecov.io/gh/EveGroup/EveHolder/)

This is the online event registration web application for ISP project. <br>
More information, visit our [Homepage](https://github.com/EveGroup/EveHolder/wiki)!

## Requirements

- Python3.6 or Python3.7
- pip
- pipenv
- postgreSQL 9.6.2 or newer [optional]

Note:

- If you use Python3.8, it'll occur the error.  
  Read here how to fix: [issues #84](https://github.com/EveGroup/EveHolder/issues/84).

- [Download PostgreSQL Database](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) (Recommend:
  Postgre12)

## Setup for EveHolder Web application

Download the code from git using `git clone`. Do the following step to use this application.

`python3` refers to the Python 3 command using in Linux and Mac system. For window use `python` or `py`.

1. Check python version (it should be 3.6 or 3.7).

   ```bash
   python --version
   ```

2. Install `pipenv`

   ```bash
   pip install pipenv
   ```

3. Install all required packages.

   ```bash
   pipenv install -r requirements.txt
   ```

4. In the project root directory/mysite, copy `sample.env` and change to `.env`(file name begin with "."). Then
   edit `.env` and set values of these variables as desired.

   ```env
   SECRET_KEY=any-random-string-will-work
   # set DEBUG to True for testing and local development
   DEBUG=False

   # If you use postgreSQL you need the DATABASE_URL in .env
   DATABASE_URL=psql://postgres:postgrespassword@127.0.0.1:port/database_name

   TIME_ZONE=Asia/Bangkok
   ```

   **Not use postgreSQL:**

   You don't have to use `DATABASE_URL` and use the default setting instead,  
   which means you will use **sqlite3** database instead of **PostgreSQL**.

   **Use postgreSQL:**

    - At `DATABASE_URL`

        - `postgrespassword` is a password of your postgreSQL that you created when you install the postgreSQL program.

        - `port` is a port of your postgreSQL database port.

        - `database_name` is the name of your database that you created.

   For more information about `.env`, see more at [Django-environ](https://django-environ.readthedocs.io/en/latest/).

5. Activate `pipenv`

   ```bash
   pipenv shell
   ```

6. Initialize database:

   ```bash
   python manage.py makemigrations
   python manage.py makemigrations eve_holder
   python manage.py migrate
   ```

7. Import data

   ```bash
   python manage.py group
   python manage.py loaddata auth_users
   ```

8. Exit the `pipenv`

   ```bash
   exit
   ```

## Running the application

1. Start the server int the `pipenv`

   ```bash
   pipenv shell
   python manage.py runserver
   ```

   This starts the web server at port 8000.

2. You should see this messages printed from the terminal.

   ```bash
   System check identified no issues (0 silenced).
   November 20, 2020 - 03:03:29
   Django version 3.1.3, using settings 'mysite.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.
   ```

   If you get a message about the port is busy, you can change port by specify a port after run command.

   ```bash
   python manage.py 8080
   ```

3. In web browser, paste the link: <http://127.0.0.1:8000/>

4. You can stop the python server by press CTRL-C in terminal that you run server. Then exit the `pipenv`

   ```bash
   exit
   ```

## Installation Problem

- Problem with pipenv when using Python3.8 or/and macOS  
  Follow this instruction: [issues #84](https://github.com/EveGroup/EveHolder/issues/84)

## Username and password of initial user

This is the sample accounts for the login to the application.

- For the login as visitor: Username: `visitor1` password: `Hackpass`.
- For the login as host: Username: `Host1` password: `Hackpass`.

## Team Members

|   Name    |    Lastname     |                   Github                    |
| :-------: | :-------------: | :-----------------------------------------: |
| Kongtapp  | Veerawattananun |  [KongtappV](https://github.com/KongtappV)  |
|  Metaras  |  Charoenseang   |    [metaras](https://github.com/metaras)    |
| Pattarin  |  Wongwaipanich  |  [pattarinn](https://github.com/pattarinn)  |
| Vichisorn |   Wejsupakul    | [james31366](https://github.com/james31366) |

## Links to docs

- [Requirements](https://github.com/EveGroup/EveHolder/wiki/Requirements)
- [Vision Statements](https://github.com/EveGroup/EveHolder/wiki/Vision-Statement)
- [Iteration 1 Plan](https://github.com/EveGroup/EveHolder/wiki/Iteration-1-Plan)
    - [Project board](https://github.com/EveGroup/EveHolder/projects/2)
- [Iteration 2 Plan](https://github.com/EveGroup/EveHolder/wiki/Iteration-2-Plan)
    - [Project board](https://github.com/EveGroup/EveHolder/projects/3)
- [Iteration 3 Plan](https://github.com/EveGroup/EveHolder/wiki/Iteration-3-Plan)
    - [Project board](https://github.com/EveGroup/EveHolder/projects/4)
- [Iteration 4 Plan](https://github.com/EveGroup/EveHolder/wiki/Iteration-4-Plan)
    - [Project board](https://github.com/EveGroup/EveHolder/projects/5)
- [Iteration 5 Plan](https://github.com/EveGroup/EveHolder/wiki/Iteration-5-Plan)
    - [Project board](https://github.com/EveGroup/EveHolder/projects/6)
- [Iteration 6 Plan](https://github.com/EveGroup/EveHolder/wiki/Iteration-6-Plan)
    - [Project board](https://github.com/EveGroup/EveHolder/projects/7)
- [Iteration 7 Plan](https://github.com/EveGroup/EveHolder/wiki/Iteration-7-Plan)
    - [Project board](https://github.com/EveGroup/EveHolder/projects/8)
- [Code Review Procedure](https://github.com/EveGroup/EveHolder/wiki/Code-Review-Procedure)
- [Code Review Checklist](https://github.com/EveGroup/EveHolder/wiki/Code-Review-checklist)
- [Presentation slide](https://docs.google.com/presentation/d/1SJUa7aaOuGhnvCN3nhPSgHTk1zMABUyi4yAbcUXGlzU/edit?usp=sharing)
