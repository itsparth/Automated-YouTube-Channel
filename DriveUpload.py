from __future__ import print_function

import io

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'


def main():
    """Shows basic usage of the Drive v3 API.

    Prints the names and ids of the first 10 files the user has access to.
    """
    store = oauth_file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


def callback(request_id, response, exception):
    if exception:
        # Handle error
        print(exception)
    else:
        print("Permission Id: %s" % response.get('id'))


def uploadFile(filepath, filename):

    store = oauth_file.Storage('token.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))


    metadata = {'name' : filename}
    print("Uploading %s to Google Drive..." %filename)
    res = service.files().create(body=metadata, media_body=filepath, fields='id, webViewLink').execute()

    if res:
        print('Uploaded "%s"' % (filename))
        id =  res.get('id')

        user_permission = {
            'type': 'anyone',
            'role': 'reader',
            'allowFileDiscovery': 'false'
        }

        service.permissions().create(fileId=id,body=user_permission,fields='id').execute()

        return res.get('webViewLink')

def get_file_name(id):
    store = oauth_file.Storage('token.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    request = service.files().get(fileId=id, fields='name').execute()
    return request.get('name')

if __name__ == '__main__':
    get_file_name('0B9bpsTYXP4ceUEgzVHVQLWFDd2s')
