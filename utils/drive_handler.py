"""
Google Drive handler for the WhatsApp Image Sender application.
"""
import os
import io
from datetime import datetime
from typing import Dict, List, Any, Optional
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'credentials/credentials.json'
TOKEN_FILE = 'credentials/token.json'

class DriveHandler:
    """Handler for Google Drive operations."""
    
    @staticmethod
    def _get_credentials() -> Optional[Credentials]:
        """Get or refresh credentials."""
        creds = None
        
        # Check if token.json exists
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        # If no valid credentials available, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    st.error("credentials.json not found. Please follow the setup instructions.")
                    st.markdown("""
                    ### Setup Instructions:
                    1. Go to [Google Cloud Console](https://console.cloud.google.com)
                    2. Create a new project or select existing one
                    3. Enable the Google Drive API
                    4. Create OAuth 2.0 credentials
                    5. Download the credentials and save as `credentials/credentials.json`
                    """)
                    return None
                
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        return creds

    @staticmethod
    def _get_or_create_folder(service, folder_type: str) -> str:
        """Get or create a folder in Google Drive."""
        # Search for existing folder
        query = f"name='{folder_type}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, spaces='drive', fields='files(id)').execute()
        items = results.get('files', [])
        
        if items:
            return items[0]['id']
        
        # Create new folder
        folder_metadata = {
            'name': folder_type,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        return folder.get('id')

    @staticmethod
    def upload_to_drive(file_data: bytes, folder_type: str, filename: str) -> Dict[str, Any]:
        """Upload a file to Google Drive."""
        try:
            creds = DriveHandler._get_credentials()
            if not creds:
                return None
            
            service = build('drive', 'v3', credentials=creds)
            
            # Get or create folder
            folder_id = DriveHandler._get_or_create_folder(service, folder_type)
            
            # Prepare file metadata
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_metadata = {
                'name': f"{timestamp}_{filename}",
                'parents': [folder_id]
            }
            
            # Upload file
            media = MediaIoBaseUpload(
                io.BytesIO(file_data),
                mimetype='image/jpeg',
                resumable=True
            )
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, size, createdTime, webViewLink'
            ).execute()
            
            return {
                'id': file.get('id'),
                'name': file.get('name'),
                'size': file.get('size'),
                'createdTime': file.get('createdTime'),
                'url': file.get('webViewLink'),
                'folder_type': folder_type
            }
        
        except Exception as e:
            st.error(f"Error uploading to Drive: {str(e)}")
            return None

    @staticmethod
    def list_drive_images(folder_type: str) -> List[Dict[str, Any]]:
        """List images from a specific folder in Google Drive."""
        try:
            creds = DriveHandler._get_credentials()
            if not creds:
                return []
            
            service = build('drive', 'v3', credentials=creds)
            
            # Get folder ID
            folder_id = DriveHandler._get_or_create_folder(service, folder_type)
            
            # Search for images in folder
            query = f"'{folder_id}' in parents and trashed=false"
            results = service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, size, createdTime, webViewLink)',
                orderBy='createdTime desc'
            ).execute()
            
            files = results.get('files', [])
            return [{
                'id': file.get('id'),
                'name': file.get('name'),
                'size': file.get('size'),
                'createdTime': file.get('createdTime'),
                'url': file.get('webViewLink'),
                'folder_type': folder_type
            } for file in files]
        
        except Exception as e:
            st.error(f"Error listing Drive images: {str(e)}")
            return []

    @staticmethod
    def delete_from_drive(file_id: str) -> bool:
        """Delete a file from Google Drive."""
        try:
            creds = DriveHandler._get_credentials()
            if not creds:
                return False
            
            service = build('drive', 'v3', credentials=creds)
            service.files().delete(fileId=file_id).execute()
            return True
        
        except Exception as e:
            st.error(f"Error deleting from Drive: {str(e)}")
            return False 