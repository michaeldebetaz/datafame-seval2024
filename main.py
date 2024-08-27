from pathlib import Path
import json

INPUT_DIR = Path("input")

if __name__ == "__main__":
    transcript_filepath = INPUT_DIR / "transcript.json"
    

    with open(transcript_filepath, "r") as file:
        transcript = json.load(file)
        
    print(transcript[0])
    for item in transcript:
        print(item["text"])
        print(item["start"])
        print(item["end"])
