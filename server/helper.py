from pydantic import BaseSettings
from datetime import datetime, timezone, timedelta
import os
import json

from functools import wraps
from flask import request

# Load settings from .env file
class Settings(BaseSettings):
    SERVER_URL:str
    FLASK_SECRET_KEY:str
    ENVIRONMENT:str

    class Config:
        env_file = ".env"

settings = Settings()

########################################
# For now, load in the data from JSONs #
########################################

listings_dir = "./prices/seattle_2023-10-04/"
listings = {}
for f in os.listdir(listings_dir):
    if f.endswith(".json"):
        with open(listings_dir + f, "r") as json_file:
            data = json.load(json_file)
            listings[f.split(".")[0]] = data

# It's also nice to have the names of each category
CL_CATEGORY_NAMES = {
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

###########################
# Helper functions below! #
###########################

# This is to log server errors
def log_error(error_msg, path="./server/logs/errors"):
    # Save this to an output log file
    time = datetime.now(timezone.utc)
    filename = f"{path}/{time.strftime('%Y%m%d-%H%M%S')}.txt"
    try:
        with open(filename, "w") as f:
            f.write(error_msg)
    except:
        print("Couldn't write to log file!")