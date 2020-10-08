# hands-on-scripts
Scripts to setup and work with Hands-On Exercises for SQ Trainings. 

At the moment, the create_users.py module allows you to:

* Create any desired number of new SonarQube users in a target SonarQube instance. 
* Deactivate users matching the pattern "user_x" (where x is a number) on a target SonarQube instance

Users will be created with a random password of 6 characters, and a login matching the pattern *user_X* where X is a number. After the users are created, a new Google Spreadsheet will be created on your Google Drive account containing the list of user credentials. For this to work, **it is required that you obtain a client_secret.json file from myself and put it on your project root folder**. 

To see the full usage documentation, run: `python3 create_users.py --help`
