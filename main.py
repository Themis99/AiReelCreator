# ============================================================
# IMPORTS
# ============================================================
import os

from dotenv import load_dotenv
from pathlib import Path
from GenerateCaptions import generate_captions
from CreateReels import create_reels
from helper_func import extract_json,normalize_captions,get_mp4_files
from TelegramBot import send_videos_to_telegram
import json
import random

if __name__ == "__main__":

    load_dotenv()
    BASE_DIR = Path(__file__).resolve().parent
    os.environ["GOOGLE_API_USE_REST"] = "true"

    LLM = "gemini-2.5-pro"

    FONT_PATH = BASE_DIR / "Fonds/OpenSans-Bold.ttf"
    TEMPLATE_VIDEO_PATH = BASE_DIR / "template_safedge.mp4"
    SAVE_FILE = BASE_DIR / "reelFiles"
    SAVE_FILE.mkdir(parents=True, exist_ok=True)


    PLAN_WEIGHTS: dict[str, int] = {
        "Ισόβια ασφάλιση ζωής": 8,
        "Ασφάλεια ζωής ορισμένης διάρκειας": 4,
        "Πρόσκαιρη ασφάλιση μειούμενου κεφαλαίου": 3,
        "FULL PROTECTION": 7,
        "Full Life Plan": 9,
        "Full Capital": 6,
        "Προγράμματα κατοικίας": 5
    }

    # -------------------------------
    # LOAD PROGRAMS
    # -------------------------------
    with open("product_types.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    programs = data["insurancePrograms"]  # <-- IMPORTANT

    # -------------------------------
    # BUILD WEIGHTS LIST (SAFE)
    # -------------------------------
    weights_list: list[float] = []

    for program in programs:
        name = program["name"]
        weight = PLAN_WEIGHTS.get(name)

        if weight is None:
            raise ValueError(f"Missing weight for program: {name}")

        weights_list.append(float(weight))

    # -------------------------------
    # RANDOM WEIGHTED CHOICE
    # -------------------------------
    chosen_program = random.choices(
        programs,
        weights=weights_list,
        k=1
    )[0]

    print("Chosen program:", chosen_program["name"])

    # Build file path
    CAPTIONS_DIR = "db_captions_examples"

    program_name = chosen_program["name"]
    filename = f"{program_name}.txt"
    file_path = os.path.join(CAPTIONS_DIR, filename)

    # Load text file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            examples_text = f.read()

        #print("\nLoaded text:")
        print(examples_text)

    except FileNotFoundError:
        print(f"⚠️ File not found: {file_path}")

    print("Generating captions...")
    raw = generate_captions(LLM,examples_text,chosen_program)
    data = extract_json(raw)
    normalized = normalize_captions(data)


    print("create reels...")
    reel_counter = 0
    for reel_captions in normalized:
        reel_name = f"reel{reel_counter}"
        create_reels(reel_captions.values(),TEMPLATE_VIDEO_PATH,FONT_PATH,SAVE_FILE,reel_name)
        reel_counter +=1

    print("sending to telegram...")
    reel_files = get_mp4_files(str(SAVE_FILE))
    send_videos_to_telegram(reel_files)

    print("DONE ✅")
