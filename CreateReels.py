# ============================================================
# IMPORTS
# ============================================================
from helper_func import get_text_duration,wrap_text
from pathlib import Path


from moviepy import (

    VideoFileClip,

    CompositeVideoClip,

    TextClip,

    vfx
)

from datetime import datetime

import textwrap


def create_reels(text_list,TEMPLATE_PATH,FONT_PATH,SAVE_FILE,REEL_NAME):


    template_clip = VideoFileClip(str(TEMPLATE_PATH))

    text_lens = [len(t) for t in text_list]

    padding_x = 120
    W, H = template_clip.size

    list_clips = []




    timings = []
    START = 2.5
    FINAL_END = 0

    for char_len in text_lens:
        text_dur = get_text_duration(char_len)
        END = START + text_dur
        timings.append((START, END))
        START = END + 0.5
        FINAL_END = END

    FINAL_END += 1.5

    for text, (start, end) in zip(text_list, timings):
        clip = (
            TextClip(
                font=str(FONT_PATH),
                text=wrap_text(text),
                font_size=65,
                color="darkblue",
                method="label",
                size=(W - 2 * padding_x, H),
                margin=(120, 0),  # 👈 (horizontal, vertical)
                text_align="center",
                horizontal_align="center",
                vertical_align="center",
            )
                .with_position(("center", 0))
                .with_start(start)
                .with_end(end)
                .with_effects([vfx.CrossFadeIn(0.5)])
                .with_effects([vfx.CrossFadeOut(0.5)])

        )

        list_clips.append(clip)

    template_clip = template_clip.with_start(0).with_end(FINAL_END)

    final_clip = CompositeVideoClip(
        [template_clip] + list_clips,
        size=template_clip.size
    ).with_duration(FINAL_END)

    date_str = datetime.now().strftime("%Y-%m-%d")

    save_dir = Path(SAVE_FILE)              # works if SAVE_FILE is str OR Path
    save_dir.mkdir(parents=True, exist_ok=True)

    out_path = save_dir / f"{REEL_NAME}-{date_str}.mp4"

    final_clip.write_videofile(
        str(out_path),
        codec="libx264",
        audio_codec="aac"
    )