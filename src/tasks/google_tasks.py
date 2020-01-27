#!/usr/bin/python3 

from __future__ import print_function
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']


def task_reducer(task:dict):
    if len(task['title']) < 1:
        return None

    reduced_task = {
                'id': task['id'],
                'updated': task['updated'],
                'title': task['title'],
            }

    if 'parent' in task:
        reduced_task['parent'] = task['parent']

    if 'notes' in task:
        reduced_task['body'] = task['notes']

    if 'due' in task:
        # "2020-01-26T16:58:14.000Z"
        # reduced_task['due'] = task['due']

        _due_list = str(task['due']).split('-')
        year = int(_due_list[0])
        month = int(_due_list[1])
        day = int(_due_list[2].split('T')[0])
        _day_in_current_year = datetime.date(year, month, day).strftime('%j')  # [0,365]
        due_date = int(_day_in_current_year) + (int(year) * 365)

        reduced_task['due-meta'] = {
                'year': year,
                'month': month,
                'day': day
                }
        reduced_task['due'] = due_date

    return reduced_task


def get_tasks():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    outbound_tasks = []
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('tasks', 'v1', credentials=creds)

    # Call the Tasks API
    tasks = service.tasks().list(tasklist='@default').execute()

    for task in tasks['items']:
        reduced = task_reducer(task)
        if reduced is not None:
            outbound_tasks.append(reduced)
    
    return outbound_tasks


def main():
    tasks = get_tasks()
    
    print(json.dumps(tasks, indent=4, separators=(',', ': ')))


if __name__ == '__main__':

    main()
