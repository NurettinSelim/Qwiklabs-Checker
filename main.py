import csv
import json
from datetime import datetime

from selenium import webdriver

RESPONSES_FILE = "form_responses.csv"
START_DATE = datetime.utcfromtimestamp(1607212800)
END_DATE = datetime.utcfromtimestamp(1612742399)

browser = webdriver.Chrome()
files = {"completed_2_track": open("results/completed_2_track.csv", "w+", encoding="utf8"),
         "completed_3_track": open("results/completed_3_track.csv", "w+", encoding="utf8"),
         "completed_4_track": open("results/completed_4_track.csv", "w+", encoding="utf8"),
         "url_incorrect": open("results/url_incorrect.csv", "w+", encoding="utf8"),
         }

with open(RESPONSES_FILE, encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            line_count += 1

            required_badges = {
                "track1": ["Google Cloud Essentials", "Baseline: Infrastructure", "Cloud Engineering",
                           "Cloud Architecture", "Networking in the Google Cloud ", "Google Cloud's Operations Suite"],
                "track2": ["Baseline: Deploy & Develop", "Deploying Applications", "Websites and Web Applications",
                           "Cloud Development"],
                "track3": ["BigQuery Basics for Data Analysts", "Data Catalog Fundamentals",
                           "BigQuery for Marketing Analysts", "BigQuery for Data Warehousing",
                           "Scientific Data Processing", "Data Engineering"],
                "track4": ["Baseline: Data, ML, AI", "Intro to ML: Language Processing",
                           "Intro to ML: Image Processing", "Intermediate ML: TensorFlow on GCP",
                           "Machine Learning APIs", "Advanced ML: ML Infrastructure"]
            }

            print("\n----------------------------------")
            print(f'{row[2]} {row[3]} {row[5]}')

            if "qwiklabs.com/public_profiles" in row[5]:
                browser.get(row[5])
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

                completed_track_counter = 0
                print("--- Remaining Badges ---")
                for track_name, track_list in required_badges.items():
                    if len(track_list) == 0:
                        completed_track_counter += 1
                        print(f"{track_name.capitalize()} Completed!")
                    else:
                        print(f"{track_name.capitalize()}: {track_list}")

                if completed_track_counter > 1:
                    files[f"completed_{completed_track_counter}_track"].write(",".join(row) + "\n")

            else:
                files["url_incorrect"].write(",".join(row) + "\n")
                print("PUBLIC PROFILE URL INCORRECT")

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
