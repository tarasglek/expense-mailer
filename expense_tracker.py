# import os
# dir_path = os.path.dirname(os.path.realpath(__file__))
# import sys
# sys.path.append(os.path.join(dir_path, 'lib'))

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from apiclient.discovery import build
import mimetypes
import io
from googleapiclient.http import MediaIoBaseUpload
SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
    ]
SERVICE_ACCOUNT_FILE = 'client_secret.json'

def next_available_row(worksheet):
    str_list = filter(None, worksheet.col_values(1))  # fastest
    return str(len(str_list)+1)

def add_entry(sheet_link, links, row):
    documents = " ".join(map(lambda x: "HYPERLINK(\"{}\", \"{}\")".format(links[x], x), links.keys()))
    if len(documents):
        documents = '=' + documents
    row['documents'] = documents
    # use creds to create a client to interact with the Google Drive API

    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    # sheet = client.open("house expenses").sheet1
    worksheet = client.open_by_url(sheet_link).sheet1
    col_mapping = {}
    first_row = worksheet.row_values(1)
    print(worksheet.row_values(1))
    for i in range(0, len(first_row)):
        col_mapping[first_row[i]] = i
    # Extract and print all of the values
    next_row = next_available_row(worksheet)
    # Select a range
    last_chr = chr(ord('A') + len(first_row) - 1)
    cell_list = worksheet.range('A{}:{}{}'.format(next_row, last_chr, next_row))
    print(row)
    for key in row.keys():
        cell_list[col_mapping[key]].value = row[key]
    worksheet.update_cells(cell_list, value_input_option='USER_ENTERED')

def drive():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service

def ls():
    drive_service = drive()
    # Call the Drive v3 API
    page_token = None
    ret = []
    while True:
        response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            print 'Found file: %s (%s)' % (file.get('name'), file.get('id'))
            ret.append((file.get('name'), file.get('id')))
            # prefix = file.get('name')
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return ret
"""
GOogle drive api requires having a filename one can stream from..app engine doesn't have access to files
based on example 5 in https://www.programcreek.com/python/example/103498/googleapiclient.http.MediaIoBaseUpload
list files is useful to figure out files shared with me..to get the id
"""
def upload_file(parent_id, name, content):
    fd = io.BytesIO(content)
    mime_type = mimetypes.guess_type(name)
    if mime_type[0] is None:
        mime_type = "application/octet-stream"
    media_body = MediaIoBaseUpload(fd, mimetype=mime_type,
     chunksize=256*1024, resumable=True)
    body = {
            'name': name,
            'mimeType': mime_type,
            'parents': [parent_id],
        }
    print(body)
    file_data = drive().files().create(
            body=body,
            media_body=media_body).execute()
    print(file_data)
    return "https://drive.google.com/file/d/" + file_data['id']