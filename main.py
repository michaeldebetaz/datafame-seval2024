from pathlib import Path
import json


INPUT_DIR = Path("input")

if __name__ == "__main__":
    transcript_filepath = INPUT_DIR / "transcript.json"

    with open(transcript_filepath, "r") as file:
        transcript = json.load(file)

    text: str = "<p>"
    for item in transcript:
        start_seconds: float = item["start"] / 100
        minutes = int(start_seconds // 60)
        seconds = int(start_seconds % 60)
        start_minutes: str = f"{minutes}:{seconds:02d}"
        inner_text: str = item["text"].strip()

        text += f'<span class="timestamp" data-timestamp="{start_seconds}">{start_minutes}</span>\u0020{inner_text}\u0020'

    text += "</p>"

    result = {
        "text": text,
        "media": "Philosophie  La grandeur de Socrate Jeanne Hersch.mp3",
        "media-time": 1293.548147,
    }

    with open("output.otr", "w") as file:
        json.dump(result, file, indent=4)
