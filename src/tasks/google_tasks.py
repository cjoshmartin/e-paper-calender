#!/usr/bin/python3 

from __future__ import print_function
import pickle
import os.path
import json
import hashlib
import tempfile
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


class DiscoveryCache: # https://github.com/googleapis/google-api-python-client/issues/325
    def filename(self, url):
        return os.path.join(
            tempfile.gettempdir(),
            'google_api_discovery_' + hashlib.md5(url.encode()).hexdigest())

    def get(self, url):
        try:
            with open(self.filename(url), 'rb') as f:
                return f.read().decode()
        except FileNotFoundError:
            return None

    def set(self, url, content):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(content.encode())
            f.flush()
            os.fsync(f)
        os.rename(f.name, self.filename(url))


def get_tasks():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    outbound_tasks = []
    creds = None
    current_path = os.path.dirname(os.path.abspath(__file__))
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    picked_token_path = current_path + '/token.pickle'
    print(picked_token_path)
    if os.path.exists(picked_token_path):
        with open(picked_token_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                current_path + '/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(picked_token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('tasks', 'v1', credentials=creds, cache=DiscoveryCache()) # https://github.com/googleapis/google-api-python-client/issues/325

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
