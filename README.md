# 🎬 YouTube AI Automation System

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991.svg)](https://openai.com)
[![Zapier](https://img.shields.io/badge/Zapier-Automation-FF4A00.svg)](https://zapier.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **Complete AI-powered YouTube content creation pipeline** - from idea generation to video upload

##  Overview

This system automates your entire YouTube content workflow using:
- **Zapier** for schedule-triggered content generation
- **GPT-4o** for scripts, titles, descriptions, and thumbnails
- **Python** for advanced automation and YouTube API integration

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Script Generation** | Full video scripts with hooks, intros, and conclusions |
| 🎨 **Thumbnail Creation** | DALL-E 3 generated thumbnails with text overlay |
| 📝 **SEO Optimization** | Keywords, tags, and descriptions auto-generated |
| ⏰ **Weekly Scheduling** | Automated weekly content calendar |
| 📤 **YouTube Upload** | Direct API upload with metadata |
| 📊 **Analytics** | Performance tracking and optimization |

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────────────┐
│ WEEKLY AUTOMATION FLOW │
├─────────────────────────────────────────────────────────────────┤
│ │
│ Zapier Schedule ──► GPT-4o ──► Script ──┬──► Python Uploader │
│ (Every Monday) Generates Save │ │
│ │ ├──► Thumbnail Gen │
│ │ │ │
│ ▼ └──► YouTube API │
│ Google Docs │
│ (Backup) │
└─────────────────────────────────────────────────────────────────┘

text

## 📋 Prerequisites

- Python 3.9+
- OpenAI API key
- YouTube API credentials
- Zapier account (free tier works)
- Google Cloud project (for YouTube API)

## 🛠️ Installation

1. Clone Repository
```bash
git clone https://github.com/sarahsair25/youtube-ai-automation.git
cd youtube-ai-automation

2. Install Dependencies
bash
pip install -r requirements.txt

3. Set Up Environment Variables
bash
cp .env.example .env
# Edit .env with your API keys

4. Configure YouTube API
bash
# Enable YouTube Data API v3 in Google Cloud Console
# Download credentials.json to project root
python -c "from src.youtube_uploader import YouTubeUploader; YouTubeUploader()"
# Follow OAuth flow

5. Set Up Zapier (Optional)
Use the template below or import the provided Zap template.

📖 Usage
Quick Start
python
from src.content_generator import YouTubeContentGenerator
from src.thumbnail_generator import ThumbnailGenerator

# Generate video plan
generator = YouTubeContentGenerator()
video = generator.generate_video_plan("How to use LangChain for RAG")

# Save script
generator.save_script(video)

# Generate thumbnail
thumb_gen = ThumbnailGenerator()
thumb_gen.generate_thumbnail(video.thumbnail_prompt, video.title)
Full Automation
bash
# Run weekly workflow
python main.py

# Test run (no scheduling)
python main.py --test
Zapier Configuration (Based on Your Setup)

Step 1: Trigger
App: Schedule by Zapier
Event: Every Week
Day/Time: Monday, 9:00 AM

Step 2: AI Action
App: AI by Zapier
Provider: OpenAI
Model: GPT-4o
Prompt: (see config/zapier_prompt.txt)

Step 3: Google Docs
Create document with generated script

Step 4: Webhook (to Python backend)
Send data to your Python server

📁 Project Structure
text
youtube-ai-automation/
├── src/
│   ├── content_generator.py   # GPT-4o script generation
│   ├── thumbnail_generator.py # DALL-E thumbnails
│   ├── youtube_uploader.py    # YouTube API upload
│   └── scheduler.py           # Weekly scheduling
├── config/
│   ├── config.yaml            # App configuration
│   └── zapier_prompt.txt      # Zapier prompt template
├── outputs/
│   ├── scripts/               # Generated scripts
│   ├── thumbnails/            # Generated thumbnails
│   └── videos/                # Video files (manual/recorded)
├── main.py                    # Entry point
├── requirements.txt
├── .env.example
└── README.md
🎯 Example Output
Generated Script Snippet
markdown
# HOOK (0-30 seconds)
"Most developers are using LangChain WRONG. Here's the right way..."

# INTRO (30-90 seconds)
"By the end of this video, you'll know how to build production-ready RAG pipelines that actually work."

# MAIN CONTENT
1. Understanding the architecture
2. Setting up your first chain
3. Adding memory and tools
4. Production best practices
Sample Prompt from Zapier
json
{
  "video_title": "LangChain RAG: From Zero to Production in 10 Minutes",
  "topic_theme": "Building production RAG systems with LangChain",
  "video_description": "Learn how to build production-ready RAG pipelines...",
  "tags": ["LangChain", "RAG", "LLM", "Python", "AI Tutorial"],
  "thumbnail_prompt": "A developer standing in front of flowing data streams..."
}

📊 Cost Breakdown
Service	Monthly Cost	Notes
OpenAI GPT-4o	$10-20	Script generation (4-8 videos)
DALL-E 3	$5-10	Thumbnails (4-8 images)
Zapier	$0-20	Free tier: 100 tasks/month
YouTube API	Free	Quota: 10,000 units/day
Total	$15-50	For 4-8 videos/month

🚀 Advanced Features
Custom Voiceover with ElevenLabs
python
from elevenlabs import generate, save

audio = generate(
    text=video.script,
    voice="Adam",
    model="eleven_monolingual_v1"
)
save(audio, "voiceover.mp3")
Automatic Captions
python
# Generate subtitles using Whisper
import whisper
model = whisper.load_model("base")
result = model.transcribe("video.mp4")
# Save as .srt file

### Troubleshooting
Issue	Solution
- YouTube upload fails:	Check OAuth token expiry
- GPT-4o rate limits:	Add exponential backoff
- Thumbnail generation	:Verify DALL-E prompt length
- Zapier webhook timeout	Use polling instead

🤝 Contributing

1.Fork the repository
2.Create feature branch
3.Commit changes
4. Push to branch
5.Open Pull Request

📄 License
MIT License - see LICENSE file

🙏 Acknowledgments

- OpenAI for GPT-4o and DALL-E 3

- Zapier for automation platform

- Google for YouTube API

