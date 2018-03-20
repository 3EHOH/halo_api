# halo_api

This project is a simple Flask API backend, with a Postgres database, and a React frontend.

**Main functionality:** 

It has two API methods: “get” and “set”.  The method “get” takes a “key” argument and returns the current value associated 
with the key, if it exists.  The method “set” takes two arguments, a “key” and a “value”, and sets the value of “key” to 
the specified value.  The data is persisted to Postgres using sqlalchemy.

**Security:**

A user is able to sign up, log in, and log out.  While logged in, they are only be able to interact with and modify keys 
they have created. Logged out users are not able to set or get any data.

This feature was implemented using JwT tokens.

**Setup:**
- ensure that Python3, pip3, Flask, and Postgresql are installed in the local environment
- clone this repo
- cd `halo_project`
- Export the following environment variables:
    ```
    export APP_SETTINGS="development"
    export DATABASE_URL="postgresql://localhost/halo_api"
    
    ```
- Install required Python packages: `pip3 install -r requirements.txt`
- Create the database: `createdb halo_api`
- Initialize, migrate, and upgrade the database:
    ```
    $ python3 manage.py db init
    $ python3 manage.py db migrate
    $ python3 manage.py db upgrade
    
    ```
- Run the application: `flask run`
- The application will run at `http://localhost:5000/`
- The frontend interface will be accessible via `http://localhost:5000/home`

**To Do:**
- Because of the set time-box of "several hours", there is more work that could be done. 
- Add additional API functionality. Currently, all we have is "get" and "post". An enhancement would be to allow users to
"put" and "delete" their key-value pairs.
- Make the frontend more scalable and more visually pleasing. As is, all the React components for signing up, logging in,
logging out, setting and getting key-value pairs is all in a single file. They should be split up into individual component
files, and the display should only render one form component at a time. Further, success or error messages should be 
displayed in the UI. 