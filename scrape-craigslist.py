import argparse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import json
from datetime import datetime
import os

# Set up command line arguments for location etc.
parser = argparse.ArgumentParser(description="Scrape craiglist listings")
parser.add_argument("--location", "-l", help="craigslist location subdomain to search through")
parser.add_argument("--output", "-o", help="output directory to write results to")
parser.add_argument("--categories", "-c", 
                    help="categories to search through (leave blank to search all categories except bar, zip, and waa)", 
                    nargs="+", default=[])
args = parser.parse_args()


# Hardcoded "for sale" categories
cl_categories = {
    "ata": "antiques",
    "ppa": "appliances",
    "ara": "arts+crafts",
    "sna": "atvs/utv/sno",
    "pta": "auto parts",
    "ava": "aviation",
    "baa": "baby+kids",
    # "bar": "barter",
    "haa": "beauty+hlth",
    "bip": "bike parts",
    "bia": "bikes",
    "bpa": "boat parts",
    "boo": "boats",
    "bka": "books",
    "bfa": "business",
    "cta": "cars+trucks",
    "ema": "cds/dvd/vhs",
    "moa": "cell phones",
    "cla": "clothes+acc",
    "cba": "collectibles",
    "syp": "computer parts",
    "sya": "computers",
    "ela": "electronics",
    "gra": "farm+garden",
    # "zip": "free",
    "fua": "furniture",
    "gms": "garage sale",
    "foa": "general",
    "hva": "heavy equip",
    "hsa": "household",
    "jwa": "jewelry",
    "maa": "materials",
    "mpa": "motorcycle parts",
    "mca": "motorcycles",
    "msa": "music instr",
    "pha": "photo+video",
    "rva": "rvs+camp",
    "sga": "sporting",
    "tia": "tickets",
    "tla": "tools",
    "taa": "toys+games",
    "vga": "video gaming",
    # "waa": "wanted",
    "wta": "wheels+tires",
}

# Set up fake user agent
ua = UserAgent()
req_header = {"User-Agent":str(ua.chrome)}

# I love this little function that I keep reusing
def progress_bar(percent, task_name, bar_length=20, max_fill=60):
    arrow = "█" * int(percent/100 * bar_length - 1)
    spaces = " " * (bar_length - len(arrow))
    loading_bar = f"\r{task_name} [{arrow}{spaces}] {percent:.2f}%"
    fill = " " * (max_fill - len(loading_bar))
    ending = '\n' if percent == 100 else '\r'
    print(f"{loading_bar}{fill}", end=ending)

def scrape_category(code, area):
    url = f"https://{area}.craigslist.org/search/see/{code}"
    html = requests.get(url, headers=req_header)
    soup = BeautifulSoup(html.text, "html.parser")
    data = soup.find("script", {"id": "ld_searchpage_results"})
    data = json.loads(data.contents[0])["itemListElement"]

    listings = [{
        "name": d["item"]["name"],
        "image": d["item"]["image"],
        "price": d["item"]["offers"]["price"],
        "location" : d["item"]["offers"]["availableAtOrFrom"]["address"]
    } for d in data]

    return(listings)

if __name__ == "__main__":
    cats_to_scrape = args.categories if len(args.categories) > 0 else cl_categories.keys()
    date = datetime.now().strftime("%Y-%m-%d") # for output folder name
    subdir = f"{args.location}_{date}"
    if not os.path.exists(f"{args.output}/{subdir}"):
        os.makedirs(f"{args.output}/{subdir}")
    else:
        print(f"Output directory {args.output}/{subdir} already exists. Exiting...")
        exit()

    n_listings = 0
    for i, cat in enumerate(cats_to_scrape):
        progress_bar((i+1)/len(cats_to_scrape)*100, f"Scraping {cl_categories[cat]}")
        listings = scrape_category(cat, args.location)
        n_listings += len(listings)
        with open(f"{args.output}/{subdir}/{cat}.json", "w") as f:
            json.dump(listings, f)

    print(f"Found {n_listings} listings at {args.location}.craigslist.org on {date}")
    