import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from tqdm import tqdm

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Function to authenticate and create a Google Drive service instance
def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    return service

# Function to upload a single file with progress bar
def upload_file_with_progress(service, file_path, folder_id=None):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    media = MediaFileUpload(file_path, resumable=True)
    
    request = service.files().create(
        media_body=media,
        body={
            'name': file_name,
            'parents': [folder_id] if folder_id else []
        }
    )
    
    progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress_bar.update(status.resumable_progress - progress_bar.n)
    progress_bar.close()

    print(f"File '{file_name}' uploaded successfully.")

# Function to upload multiple files in a directory
def upload_directory(service, directory_path, folder_id=None):
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            upload_file_with_progress(service, file_path, folder_id)

# Main function to demonstrate the upload process
def main():
    service = authenticate()
    # Example: Upload a single file
    # upload_file_with_progress(service, 'path/to/file.txt', 'your_folder_id_here')

    # Example: Upload all files in a directory
    upload_directory(service, 'path/to/directory', 'your_folder_id_here')

if __name__ == '__main__':
    main()
