#!/usr/bin/env python3
"""
Complete YouTube AI Automation System
Generates, creates thumbnails, and uploads videos
"""

import os
import sys
import schedule
import time
from datetime import datetime
from loguru import logger
from dotenv import load_dotenv

from src.content_generator import YouTubeContentGenerator, YouTubeVideo
from src.thumbnail_generator import ThumbnailGenerator
from src.youtube_uploader import YouTubeUploader

load_dotenv()


class YouTubeAutomation:
    """Main automation orchestrator"""

    def __init__(self):
        self.content_gen = YouTubeContentGenerator(niche="AI & Technology")
        self.thumbnail_gen = ThumbnailGenerator()
        self.uploader = YouTubeUploader()

        logger.info("YouTube Automation System initialized")

    def run_weekly_workflow(self, topic: str = None):
        """
        Complete weekly workflow:
        1. Generate video plan
        2. Save script
        3. Generate thumbnail
        4. Upload to YouTube (or save for manual recording)
        """
        logger.info("=" * 50)
        logger.info("Starting weekly YouTube workflow...")

        # Step 1: Generate content
        logger.info("Step 1: Generating video plan with AI...")
        video = self.content_gen.generate_video_plan(topic)

        # Step 2: Save script
        logger.info("Step 2: Saving script...")
        script_path = self.content_gen.save_script(video)

        # Step 3: Generate thumbnail
        logger.info("Step 3: Generating thumbnail...")
        thumbnail_path = self.thumbnail_gen.generate_thumbnail(
            video.thumbnail_prompt, video.title
        )

        # Step 4: Print summary
        print("\n" + "=" * 60)
        print("✅ WEEKLY VIDEO GENERATED!")
        print("=" * 60)
        print(f"📹 TITLE: {video.title}")
        print(f"📝 TOPIC: {video.topic}")
        print(f"⏱️  LENGTH: {video.suggested_length}")
        print(f"📂 SCRIPT: {script_path}")
        print(f"🖼️ THUMBNAIL: {thumbnail_path}")
        print(f"🏷️  TAGS: {', '.join(video.tags)}")
        print("=" * 60)

        # Step 5: Upload if video file exists
        video_file = self._check_video_file(video.title)
        if video_file:
            logger.info("Step 5: Uploading to YouTube...")
            video_id = self.uploader.upload_video(
                video_path=video_file,
                title=video.title,
                description=video.description,
                tags=video.tags,
                thumbnail_path=thumbnail_path,
                privacy_status="unlisted"  # Change to "public" when ready
            )

            if video_id:
                logger.success(f"Video live at: https://youtu.be/{video_id}")
            else:
                logger.warning("Upload failed - check video file")
        else:
            logger.info("No video file found. Ready for manual recording.")
            logger.info(f"Script ready: {script_path}")

        return video

    def _check_video_file(self, title: str) -> str:
        """Check if video file already exists"""
        video_dir = "outputs/videos"
        if not os.path.exists(video_dir):
            return None

        for file in os.listdir(video_dir):
            if title[:30] in file and file.endswith(('.mp4', '.mov')):
                return os.path.join(video_dir, file)
        return None

    def start_scheduler(self):
        """Start weekly scheduling"""
        # Schedule weekly on Monday at 9 AM
        schedule.every().monday.at("09:00").do(self.run_weekly_workflow)

        logger.info("Scheduler started. Running weekly on Monday at 9:00 AM")

        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║     🤖 YouTube AI Automation System               ║
    ║     Powered by GPT-4o + Zapier + Python          ║
    ║     Version 2.0                                   ║
    ╚═══════════════════════════════════════════════════╝
    """)

    automation = YouTubeAutomation()

    # Run once for testing
    if "--test" in sys.argv:
        automation.run_weekly_workflow()
    else:
        automation.start_scheduler()


if __name__ == "__main__":
    main()