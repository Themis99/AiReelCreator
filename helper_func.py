# ============================================================
# IMPORTS
# ============================================================
import os
import json
import re


import textwrap

def extract_json(text: str) -> dict:
    cleaned = re.sub(r"```(?:json)?", "", text).strip()
    return json.loads(cleaned)

def get_mp4_files(folder_path: str) -> list[str]:
    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(".mp4")
    ]

def wrap_text(text, max_chars=30):
    return "\n".join(
        textwrap.wrap(
            text,
            width=max_chars,
            break_long_words=False,
            break_on_hyphens=False,
        )
    )


def get_text_duration(char_len):
    if char_len <= 52:
        return 3.5
    elif char_len <= 100:
            return 4.5
    elif char_len <= 200:
        return 7.5
    else:
        return 9.5

def normalize_captions(data) -> list[dict[str, str]]:
    normalized = []

    if not isinstance(data, dict):
        return normalized

    captions = data.get("captions")
    if not isinstance(captions, list):
        return normalized

    for caption in captions:
        if not isinstance(caption, dict):
            continue

        pages_raw = caption.get("pages")
        if not isinstance(pages_raw, dict):
            continue

        pages: dict[str, str] = {}

        for k, v in pages_raw.items():
            if isinstance(k, str) and k.lower().startswith("page"):
                pages[k.lower()] = str(v).strip()

        if not pages:
            continue

        def page_index(item: tuple[str, str]) -> int:
            key = item[0]
            try:
                return int(key.replace("page", ""))
            except ValueError:
                return 0

        pages_sorted = dict(sorted(pages.items(), key=page_index))
        normalized.append(pages_sorted)

    return normalized

