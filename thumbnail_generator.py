"""
AI Thumbnail Generator using DALL-E 3
Creates clickable YouTube thumbnails
"""

import os
import requests
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from loguru import logger
import openai


class ThumbnailGenerator:
    """Generate YouTube thumbnails using DALL-E 3 + enhancements"""

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_thumbnail(self, prompt: str, title: str) -> Optional[str]:
        """
        Generate thumbnail image from prompt

        Args:
            prompt: DALL-E prompt (from AI)
            title: Video title (for text overlay)

        Returns:
            Path to generated thumbnail
        """
        try:
            # Generate image with DALL-E 3
            response = openai.Image.create(
                model="dall-e-3",
                prompt=f"{prompt} Make it vibrant, high-contrast, YouTube thumbnail style. 16:9 aspect ratio.",
                size="1792x1024",  # 16:9 ratio
                quality="hd",
                n=1
            )

            image_url = response.data[0].url

            # Download image
            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))

            # Add text overlay (title)
            img = self._add_text_overlay(img, title)

            # Save thumbnail
            output_path = f"outputs/thumbnails/{title[:50]}.png"
            os.makedirs("outputs/thumbnails", exist_ok=True)
            img.save(output_path)

            logger.success(f"Generated thumbnail: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Thumbnail generation failed: {str(e)}")
            return None

    def _add_text_overlay(self, image: Image.Image, title: str) -> Image.Image:
        """Add text overlay to thumbnail"""
        # Create a copy for editing
        img = image.copy()
        draw = ImageDraw.Draw(img)

        # Try to load a bold font, fall back to default
        try:
            font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            font = ImageFont.truetype(font_path, 60)
        except:
            font = ImageFont.load_default()

        # Calculate text position (bottom third)
        img_width, img_height = img.size
        text_position = (50, img_height - 200)

        # Add semi-transparent background for text
        text_bbox = draw.textbbox(text_position, title[:60], font=font)
        draw.rectangle(text_bbox, fill=(0, 0, 0, 128))

        # Draw text
        draw.text(text_position, title[:60], fill=(255, 255, 255), font=font)

        return img