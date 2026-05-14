"""
AI-Powered YouTube Content Generator
Creates scripts, titles, descriptions, and thumbnails
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

import openai
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


@dataclass
class YouTubeVideo:
    """Complete video data structure"""
    title: str
    topic: str
    description: str
    script: str
    tags: List[str]
    thumbnail_prompt: str
    key_points: List[str]
    suggested_length: str
    seo_keywords: List[str]
    created_at: datetime = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now()


class YouTubeContentGenerator:
    """
    AI Content Generator for YouTube videos
    Uses GPT-4o for script and content creation
    """

    def __init__(self, niche: str = "AI & Technology"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.niche = niche
        self.model = "gpt-4o"  # as shown in your Zapier screenshot

        logger.info(f"YouTube Content Generator initialized for niche: {niche}")

    def generate_video_plan(self, topic: Optional[str] = None) -> YouTubeVideo:
        """
        Generate complete video plan using AI

        Args:
            topic: Specific topic (if None, AI suggests trending topic)

        Returns:
            YouTubeVideo object with all content
        """
        if not topic:
            topic = self._get_trending_topic()

        prompt = self._build_video_prompt(topic)

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )

            content = json.loads(response.choices[0].message.content)

            video = YouTubeVideo(
                title=content["video_title"],
                topic=topic,
                description=content["video_description"],
                script=self._format_script(content["script_outline"]),
                tags=content["tags"],
                thumbnail_prompt=content["thumbnail_prompt"],
                key_points=content["key_points"],
                suggested_length=content["suggested_length"],
                seo_keywords=content["seo_keywords"]
            )

            logger.success(f"Generated video plan: {video.title}")
            return video

        except Exception as e:
            logger.error(f"Failed to generate content: {str(e)}")
            raise

    def _system_prompt(self) -> str:
        return """
        You are an expert YouTube content creator with 5+ years of experience.
        Your videos get 100k+ views because you understand:
        - Retention strategies (hook within 30 seconds)
        - SEO optimization (keywords in first 200 characters)
        - Audience psychology (pain points → solutions)

        Always return valid JSON. Never include markdown formatting in output.
        """

    def _build_video_prompt(self, topic: str) -> str:
        return f"""
        Create a YouTube video plan for this topic: "{topic}"

        Channel niche: {self.niche}
        Target audience: Tech enthusiasts, developers, AI learners

        Requirements:
        1. Title must be under 70 characters
        2. Hook must grab attention in first 5 seconds
        3. Script should be conversational, not lecture
        4. Include 2-3 specific examples or demos

        Return valid JSON with this exact structure:
        {{
            "video_title": "string",
            "video_description": "3-4 sentences with keywords and CTA",
            "script_outline": {{
                "hook_0_30s": "Attention grabber",
                "intro_30_90s": "Problem statement + what they'll learn",
                "main_content": "Step-by-step explanation with examples",
                "conclusion": "Summary + call-to-action"
            }},
            "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
            "thumbnail_prompt": "Detailed prompt for DALL-E 3",
            "key_points": ["point1", "point2", "point3"],
            "suggested_length": "8-12 minutes",
            "seo_keywords": ["kw1", "kw2", "kw3"]
        }}
        """

    def _get_trending_topic(self) -> str:
        """Get trending topic using AI"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Suggest 5 trending AI/tech topics for YouTube. Return as JSON array."},
                {"role": "user", "content": f"My niche is {self.niche}. What's trending this week?"}
            ]
        )
        topics = json.loads(response.choices[0].message.content)
        return topics[0] if topics else "Latest AI Tools 2026"

    def _format_script(self, script_outline: Dict) -> str:
        """Format script outline into readable script"""
        script = f"""
# HOOK (0-30 seconds)
{script_outline['hook_0_30s']}

# INTRO (30-90 seconds)
{script_outline['intro_30_90s']}

# MAIN CONTENT
{script_outline['main_content']}

# CONCLUSION
{script_outline['conclusion']}

---
💡 BONUS TIP: Add screen recordings or demos where applicable
📢 CTA: Like, subscribe, and comment your thoughts!
        """
        return script.strip()

    def save_script(self, video: YouTubeVideo, output_dir: str = "outputs/scripts"):
        """Save script to markdown file"""
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{video.created_at.strftime('%Y%m%d')}_{video.title[:50]}.md"
        filepath = os.path.join(output_dir, filename)

        content = f"""# {video.title}

**Topic:** {video.topic}
**Length:** {video.suggested_length}
**Created:** {video.created_at}

## Script

{video.script}

## Description

{video.description}

## Tags
{', '.join(video.tags)}

## SEO Keywords
{', '.join(video.seo_keywords)}

## Key Points
{chr(10).join(f'- {point}' for point in video.key_points)}

## Thumbnail Prompt
{video.thumbnail_prompt}
"""
        with open(filepath, 'w') as f:
            f.write(content)

        logger.info(f"Saved script to {filepath}")
        return filepath
