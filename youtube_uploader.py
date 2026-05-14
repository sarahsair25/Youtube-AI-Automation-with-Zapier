"""
YouTube Video Uploader using YouTube Data API v3
Handles authentication and metadata upload
"""

import os
import json
from typing import Optional, List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from loguru import logger


class YouTubeUploader:
    """
    YouTube API client for video uploads
    Handles authentication, metadata, and thumbnails
    """

    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    def __init__(self, credentials_file: str = "credentials.json"):
        self.credentials_file = credentials_file
        self.youtube = self._authenticate()

    def _authenticate(self):
        """Authenticate with YouTube API"""
        creds = None
        token_file = "token.json"

        # Load existing token
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)

        # Refresh or create new token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(token_file, 'w') as token:
                token.write(creds.to_json())

        return build("youtube", "v3", credentials=creds)

    def upload_video(
            self,
            video_path: str,
            title: str,
            description: str,
            tags: List[str],
            category_id: str = "28",  # 28 = Science & Technology
            privacy_status: str = "unlisted",  # unlisted, private, public
            thumbnail_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Upload video to YouTube

        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID
            privacy_status: privacy status
            thumbnail_path: Path to thumbnail image

        Returns:
            Video ID if successful, None otherwise
        """
        try:
            # Prepare video metadata
            body = {
                "snippet": {
                    "title": title[:100],  # YouTube limits to 100 chars
                    "description": description[:5000],
                    "tags": tags[:15],  # Max 15 tags
                    "categoryId": category_id
                },
                "status": {
                    "privacyStatus": privacy_status,
                    "selfDeclaredMadeForKids": False
                }
            }

            # Upload video
            media = MediaFileUpload(
                video_path,
                chunksize=-1,
                resumable=True
            )

            logger.info(f"Uploading video: {title}")

            upload_request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = upload_request.execute()
            video_id = response["id"]

            logger.success(f"Video uploaded! ID: {video_id}")
            logger.info(f"URL: https://youtu.be/{video_id}")

            # Upload thumbnail if provided
            if thumbnail_path:
                self._upload_thumbnail(video_id, thumbnail_path)

            return video_id

        except Exception as e:
            logger.error(f"Upload failed: {str(e)}")
            return None

    def _upload_thumbnail(self, video_id: str, thumbnail_path: str):
        """Upload custom thumbnail"""
        try:
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
            logger.info("Thumbnail uploaded successfully")
        except Exception as e:
            logger.warning(f"Thumbnail upload failed: {str(e)}")