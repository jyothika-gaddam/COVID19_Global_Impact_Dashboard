from pathlib import Path
from urllib.request import urlretrieve

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

url = (
    "https://covid.ourworldindata.org/data/"
    "owid-covid-data.csv"
)

output_file = DATA_DIR / "owid-covid-data.csv"

try:
    print("Downloading official COVID-19 data...")
    urlretrieve(url, output_file)
    print(f"Download completed: {output_file}")

except Exception as error:
    print("Download failed.")
    print("Please check your internet connection and try again.")
    print(f"Details: {error}")