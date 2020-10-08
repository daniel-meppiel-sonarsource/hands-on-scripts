
import os
import argparse
from create_users import create_users, deactivate_users
from gsheets import GSheetsService

if __name__ == "__main__":
    parser = argparse.ArgumentParser("hands-on-user-creation")
    parser.add_argument("--delete", help='Will delete all hands-on exercise related users on the SonarQube server.', action='store_true')
    parser.add_argument("--num", help='Number of users to create when --delete flag is not present. Default value is 30.', type=int, action='store', default=30)
    parser.add_argument("--title", help='Name of the new Google Spreadsheet that will be created and written with the newly created user credentials, when the --delete flag is not present. Default is "Hands-On Exercises User List"', action='store', default='Hands-On Exercises User List')
    args = parser.parse_args()

    if not args.delete:
        print('Creating {} new SonarQube users...'.format(args.num))
        users = create_users(args.num)

        gsheetService = GSheetsService()
        print('Creating a new Google Spreadsheet titled {}...'.format(args.title))
        gsheetService.create(args.title)
        print('Writting user credential list to the new Google Spreadsheet...')
        gsheetService.write_users(users)
        print('EXECUTION SUCCESS')
    else:
        print('Deactivating all users with a login matching pattern "user_X"...')
        deactivate_users(args.num)