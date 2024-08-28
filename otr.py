from pathlib import Path
import json
import deepl

INPUT_DIR = Path("input")
STARTING_TAG = "<p>"
ENDING_TAG = "</p>"

AUTH_KEY = "c84b5469-07bf-42b7-92ca-3b347b10978f:fx"


def to_html(start_seconds: float, start_minutes: str, text: str) -> str:
    return f'<span class="timestamp" data-timestamp="{start_seconds}">{start_minutes}</span>\u0020{text}\u0020'


if __name__ == "__main__":
    transcript_filepath = INPUT_DIR / "transcript.json"

    with open(transcript_filepath, "r") as file:
        transcript = json.load(file)

    translator = deepl.Translator(AUTH_KEY)

    text_fr: str = STARTING_TAG
    text_en: str = STARTING_TAG

    for item in transcript:
        start_seconds: float = item["start"] / 100

        minutes = int(start_seconds // 60)
        seconds = int(start_seconds % 60)
        start_minutes: str = f"{minutes}:{seconds:02d}"

        inner_text_fr: str = item["text"].strip()
        text_fr += to_html(start_seconds, start_minutes, inner_text_fr)

        inner_text_en = translator.translate_text(
            inner_text_fr, source_lang="FR", target_lang="EN-GB"
        )
        text_en += to_html(start_seconds, start_minutes, str(inner_text_en))

    text_fr += ENDING_TAG
    text_en += ENDING_TAG

    result_fr = {
        "text": text_fr,
        "media": "Philosophie  La grandeur de Socrate Jeanne Hersch.mp3",
        "media-time": 1293.548147,
    }

    result_en = {
        "text": text_en,
        "media": "Philosophie  La grandeur de Socrate Jeanne Hersch.mp3",
        "media-time": 1293.548147,
    }

    with open("output-fr.otr", "w") as file:
        json.dump(result_fr, file, indent=4)

    with open("output-en.otr", "w") as file:
        json.dump(result_en, file, indent=4)
