import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define the Google Drive API scopes and service account file path
SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "credentials.json"

# Create credentials using the service account file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Build the Google Drive service
drive_service = build("drive", "v3", credentials=credentials)


def upload_file(file_path, parent_folder_id=None):
    """Upload a file to Google Drive and return its ID."""
    file_metadata = {
        "name": os.path.basename(file_path),
        "parents": [parent_folder_id] if parent_folder_id else [],
    }
    media = MediaFileUpload(file_path, resumable=True)
    uploaded_file = (
        drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    )

    print(f'Uploaded File ID: {uploaded_file["id"]}')
    return uploaded_file["id"]

def create_folder(folder_name, parent_folder_id=None):
    """Create a folder in Google Drive and return its ID."""
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_folder_id] if parent_folder_id else [],
    }

    created_folder = (
        drive_service.files().create(body=folder_metadata, fields="id").execute()
    )

    print(f'Created Folder ID: {created_folder["id"]}')
    return created_folder["id"]

if __name__ == '__main__':
    # Example usage:

    # Create a new folder
    upload_file("text.txt", "1TRExsANfqU6NW9-xS4JVM4DaH91fejdG")