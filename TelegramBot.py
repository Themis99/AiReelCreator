import os
from dotenv import load_dotenv
from telegram import Bot
import shutil
from typing import List, Optional
import asyncio
from pathlib import Path

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_CHAT_ID = os.getenv("TELEGRAM_GROUP_CHAT_ID")
TOPIC_ID = os.getenv("TOPIC_ID")
BASE_DIR = Path(__file__).resolve().parent





UPLOADED_DIR = BASE_DIR / "uploaded"


def send_videos_to_telegram(video_paths: List[str], caption: Optional[str] = None):

    async def _send():
        bot = Bot(token=TELEGRAM_BOT_TOKEN)

        # Ensure destination folder exists
        os.makedirs(UPLOADED_DIR, exist_ok=True)

        for video_path in video_paths:
            try:
                with open(video_path, "rb") as video_file:
                    await bot.send_video(
                        chat_id=TELEGRAM_GROUP_CHAT_ID,
                        message_thread_id=TOPIC_ID,
                        video=video_file,
                        caption=caption,
                        supports_streaming=True
                    )

                # Move file AFTER successful send
                destination_path = os.path.join(
                    UPLOADED_DIR,
                    os.path.basename(video_path)
                )

                shutil.move(video_path, destination_path)
                print(f"Moved to uploaded: {destination_path}")

                await asyncio.sleep(2)  # rate-limit safe

            except Exception as e:
                print(f"Failed to send {video_path}: {e}")

    asyncio.run(_send())