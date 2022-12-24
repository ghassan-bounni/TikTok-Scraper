from scraper import TiktokScraper
import os
import requests
import argparse

parser = argparse.ArgumentParser(
    description="Tiktok Ads Scraper\nDeveloped by Ghassan El Bounni -> (Github: ghassan-bounni)",
    formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--teardown", action="store_true",
                    help="Teardown the browser after scraping")

arg_list = ["Region", "Industry", "Objective", "Likes", "Resource", "Period"]
for arg in arg_list:
    parser.add_argument(arg.lower())

args = parser.parse_args()

# reqiered filters
filters = {
    "Region": args.region,
    "Industry": args.industry,
    "Objective": args.objective,
    "Likes": args.likes,
    "Resource": args.resource,
    "Period": args.period
}


def download_videos(download_links):
    os.mkdir("videos")
    for i, link in enumerate(download_links, start=1):
        print("downloading video", i)
        # create response object
        r = requests.get(link, stream=True)
        # download started
        with open(f"videos/video{i}.mp4", 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)


with TiktokScraper(teardown=args.teardown) as bot:
    bot.land_page()
    bot.filter_ads(filters)
    download_links = bot.get_ad_info(filters)
    download_videos(download_links)
