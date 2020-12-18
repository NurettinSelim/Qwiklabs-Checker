import json
from datetime import datetime

from selenium import webdriver

PUBLIC_URL = "https://www.qwiklabs.com/public_profiles/5f07c478-8904-4da1-9085-deb34f29c9bd"

START_DATE = datetime.utcfromtimestamp(1607212800)
END_DATE = datetime.utcfromtimestamp(1612051200)

# --- UYARI --- #
# Adının sonunda boşluk olan badgeler
# Track 1: "Networking in the Google Cloud "

required_badges = {
    "track1": ["Google Cloud Essentials", "Baseline: Infrastructure", "Cloud Engineering", "Cloud Architecture",
               "Networking in the Google Cloud ", "Google Cloud's Operations Suite"],
    "track2": ["Baseline: Deploy & Develop", "Deploying Applications", "Websites and Web Applications",
               "Cloud Development"],
    "track3": ["BigQuery Basics for Data Analysts", "Data Catalog Fundamentals", "BigQuery for Marketing Analysts",
               "BigQuery for Data Warehousing", "Scientific Data Processing", "Data Engineering"],
    "track4": ["Baseline: Data, ML, AI", "Intro to ML: Language Processing", "Intro to ML: Image Processing",
               "Intermediate ML: TensorFlow on GCP", "Machine Learning APIs", "Advanced ML: ML Infrastructure"]
}

browser = webdriver.Chrome()
browser.get(PUBLIC_URL)

profile_badges = browser.find_elements_by_css_selector("ql-badge")

for badge in profile_badges:
    json_text = json.loads(badge.get_attribute("badge"))
    date = datetime.strptime(json_text["completedAt"], '%b %d, %Y')
    if START_DATE <= date <= END_DATE:
        for track_name in required_badges.keys():
            if json_text["title"] in required_badges[track_name]:
                required_badges[track_name].remove(json_text["title"])
    else:
        print(f"{json_text['title']} wrong date!")

print("--- Remaining Badges ---")
for track_name, track_list in required_badges.items():
    if len(track_list) == 0:
        print(f"{track_name.capitalize()} Complete!")
    else:
        print(f"{track_name.capitalize()}: {track_list}")
browser.close()

# Sample Dict
#     {'id': 601994,
#      'title': 'Cloud Development',
#      'imageSrc': 'https://cdn.qwiklabs.com/fII8%2FxfzHangA5YENIOXHD40ba6g2NjozlcjV9GoM0c%3D',
#      'badgeHref': None,
#      'url': 'https://www.qwiklabs.com/public_profiles/5f07c478-8904-4da1-9085-deb34f29c9bd/badges/601994',
#      'completedAt': 'Dec 17, 2020',
#      'twitterOptions': None,
#      'linkedInOptions': None}
