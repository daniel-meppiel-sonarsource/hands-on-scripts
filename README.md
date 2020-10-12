# hands-on-scripts
Scripts to setup and work with Hands-On Exercises for SQ Trainings. 

At the moment, the `main.py` module allows you to:

* Create any desired number of new SonarQube users in a target SonarQube instance. 
* Deactivate users matching the pattern *user_x* (where x is a number) on a target SonarQube instance

Users will be created with a random password of 6 characters, and a login matching the pattern *user_X* where X is a number. After the users are created, a new Google Spreadsheet will be created on your Google Drive account containing the list of user credentials. 

## Required Setup
The steps below need to be taken to make the script work:

* Make sure you install [Python 3.8+](https://www.python.org/downloads/), [Pip](https://pip.pypa.io/en/stable/installing/) and [Pipenv](https://pypi.org/project/pipenv/)
* Obtain the `client_secret.json` from this [restricted link](https://drive.google.com/file/d/1n3o7E-fBmo5ksMRaBVDBNQG3QQlgIGeo/view?usp=sharing) and put it on your project root folder. This will allow the program to generate Google Spreadsheets in your GDrive.
* Create a `.env` file in the project root folder, and add the following variables:

    ```
    SQ_URL=https://mysq.ngrok.io
    SQ_TOKEN=verysecureandencryptedtokenwithadminrights
    GROUP_NAME=training-users
    PASSWORD_LENGTH=6

* Install dependencies by running `pipenv install` on the root folder. 

And you are ready to go! 

    ```
    # Activate the pipenv environment
    pipenv shell
    # Get the docs
    python main.py --help
    # Create 20 users for your training session
    python main.py --num 20
    # Delete them
    python main.py --delete

