# TikTok Scraper

Tiktok Scraper is a bot built with selenium that scrapes info from Tiktok Ads.

## Installation

Use the package manager [pip](https://pypi.org/project/pip/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

Tiktok Scraper takes as input a list of filters to filter the Tiktok Ads.

```bash
usage: run.py [-h] [--teardown] region industry objective likes resource period

Tiktok Ads Scraper
Developed by Ghassan El Bounni -> (Github: ghassan-bounni)

positional arguments:
  region
  industry
  objective
  likes
  resource
  period

optional arguments:
  -h, --help  show this help message and exit
  --teardown  Teardown the browser after scraping
```

### Example Run

```bash
python run.py Australia "Sports & Outdoor" Conversions "Top 61~80%" "20-30s" "Last 7 days"
```

### Output

* ads.json - a json file with all info about the filtered ads
* videos - a folder that contains the installed tiktok videos
