# EveHolder

[![EveGroup](https://circleci.com/gh/EveGroup/EveHolder.svg?style=svg)](https://app.circleci.com/pipelines/github/EveGroup/EveHolder)
[![codecov](https://codecov.io/gh/EveGroup/EveHolder/branch/master/graph/badge.svg?token=IYHFBSLOV7)](https://codecov.io/gh/EveGroup/EveHolder/)

This is the online event registration web application for ISP project. <br>
More information, visit our [Homepage](https://github.com/EveGroup/EveHolder/wiki)!

## Requirements

- Python3.6 or newer
- pip
- pipenv
- postgres 9.6.2 or newer

## Setup for EveHolder Web applications

Download the code from the git using `git clone`. Do the following step to using this application.

`python3` refers to the Python 3 command using in Linux and Mac system. For windows use `python` or `py`.

1. Check the python version are 3.6 or newer.

   ```bash
   python --version
   ```

2. Install `pipenv`

   ```bash
   python pip install pipenv
   ```

3. Install the requirements packages.

   ```bash
   pipenv install
   ```

4. In the project root directory/mysite, copy `sample.env` and change to `.env`(file name begin with "."). Then edit `.env` and set values of these variables as desired.

   ```env
   SECRET_KEY=any-random-string-will-work
   # set DEBUG to True for testing and local development
   DEBUG=False
   DATABASE_URL=psql://postgres:postgrespassword@127.0.0.1:port/database_name
   TIME_ZONE=Asia/Bangkok
   ```

   - At `DATABASE_URL` `postgrespassword` is password of your postgres that you create when you install the postgres program.

   - `port` is port of your postgres database port.

   - `database_name` is name of your databse that you create.

   For more information about `.env` find in [Django-environ](https://django-environ.readthedocs.io/en/latest/) document.

5. Activate the `pipenv`

   ```bash
   pipenv shell
   ```

6. Run migrations to initialize the database:

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

2. You should see this message printed from the terminal windows.

   ```bash
   System check identified no issues (0 silenced).
   November 20, 2020 - 03:03:29
   Django version 3.1.3, using settings 'mysite.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.
   ```

   If you get a message the message that the port is busy you can change port by specify port after the run command.

   ```bash
   python manage.py 8080
   ```

3. In web browser, paste the link: <http://127.0.0.1:8000/>

4. You can stop the python server by press CTRL-C in terminal that you run server. Then exit the `pipenv`

   ```bash
   exit
   ```

## Username and password of initial user

This is the sample accounts for login the web.

- For login as visitor: Username: `visitor1` password: `Hackpass`.
- For login as host: Username: `Host1` password: `Hackpass`.

## Links to docs

- [Requirements](https://github.com/EveGroup/EveHolder/wiki/Requirements)
- [Vision Statements](https://github.com/EveGroup/EveHolder/wiki/Vision-Statement)
- [Iteration 1 Plan](https://github.com/EveGroup/EveHolder/wiki/Iteration-1-Plan)
- [Iteration 2 Plan](https://github.com/EveGroup/EveHolder/wiki/Iteration-2-Plan)
- [Iteration 3 Plan](https://github.com/EveGroup/EveHolder/wiki/Iteration-3-Plan)
- [Iteration 4 Plan](https://github.com/EveGroup/EveHolder/wiki/Iteration-4-Plan)
- [Code Review Procedure](https://github.com/EveGroup/EveHolder/wiki/Code-Review-Procedure)
- [Code Review Checklist](https://github.com/EveGroup/EveHolder/wiki/Code-Review-checklist)
