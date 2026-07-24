from pathlib import Path
import requests

BASE_URL = "https://huggingface.co/Akshakio123/smart-farmer-assets/resolve/main"

FILES = {
    "database/agriculture.db": "database/agriculture.db",
    "ml/model/random_forest.pkl": "random_forest.pkl",
    "ml/model/label_encoders.pkl": "label_encoders.pkl",
    "ml/model/feature_columns.pkl": "feature_columns.pkl",
}

for local_path, remote_file in FILES.items():

    path = Path(local_path)

    if path.exists():
        continue

    path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {remote_file}...")

    url = f"{BASE_URL}/{remote_file}"

    r = requests.get(url, stream=True)

    r.raise_for_status()

    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

print("Assets Ready")