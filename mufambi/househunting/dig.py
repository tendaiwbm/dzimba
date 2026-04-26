import os
import time
import logging

logger = logging.getLogger("HH")

import requests as rq
import pandas as p

from .model import HouseHuntingModel as model
from .config import househuntingConfig as source
from ..utils import *

def extract_unique_ids(listings,id_column_name,url_column_name):
    def extract_id(listing,id_column_name,url_column_name):
        listing[id_column_name] = listing[url_column_name].split("/")[-2]
        return listing
    
    return map(lambda listing: extract_id(listing,id_column_name,url_column_name),listings)

def remove_url_domain(listings,url_column_name,domain):
    def remove_domain(listing,url_column_name,domain):
        listing[url_column_name] = listing[url_column_name].split(domain)[1]
        return listing

    return map(lambda listing: remove_domain(listing,url_column_name,domain),listings)

def parse_response(payload,id_column_name=model.id_,url_column_name=model.itemUrl,domain=source["domain"]):
    payload = extract_unique_ids(payload,id_column_name,url_column_name)
    payload = remove_url_domain(payload,url_column_name,domain)
    return list(payload)

def request(url,params):
    try:
        assert params["page"] == 1
    except:
        params["page"] = 1

    pageFound = True
    payload = []
    
    while pageFound:
        logger.info(f"Requesting resource {url} with data {repr(params)}")
        request = rq.post(url,data=params)

        response = request.json()
        pageFound = "posts" in response
        
        if not(pageFound): 
            logger.info(f"No results returned by {url} and data {repr(params)}")
            break

        payload += response["posts"]
        params["page"] += 1
    
    return payload

def pipeline():
    pipelineSetup = {
                      "request": {
                                   "function": request, 
                                   "args": [
                                             create_path([source["domain"],source["endpoint"]]),
                                             source["requestParams"]
                                           ]
                                 },
                      "parser": parse_response,
                      "directory": source["path"],
                      "file": source["localFileName"],
                      "model": model,
                      "source": source["name"],
                      "hostUrl": source["domain"],
                      "listingUrlColumn": model.itemUrl,
                      "filter": source["filters"],
                      "logger": logger
                    }

    worker = Pipeline(pipelineSetup)
    return worker.execute()
