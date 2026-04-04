import os
import time
import random
import pandas as p
from curl_cffi.requests import Session
from bs4 import BeautifulSoup as BTSP
from bs4.element import NavigableString 

from .model import ParariusModel as model
from .config import parariusConfig as source
from ..utils import *

def parse_node(node):
    return {
             "_id": "-".join(node["item"]["@id"].split("/")[-3:-1]),
             "url": node["item"]["url"].split("https://www.pararius.nl")[1]
           }

def html_innertext_to_json(html):
    from json import loads

    try:
        jsonFromText = loads(html.text)
        assert all(key in jsonFromText for key in ['@context', '@graph'])

        dataContainer = jsonFromText["@graph"][1]
        assert int(dataContainer["offers"]["offerCount"]) > 0

        data = dataContainer["mainEntity"]["itemListElement"]
        assert len(data) > 0

        return map(parse_node,data)
    except:
        return

def request(url):
    payload = []
    
    session = Session()
    response = session.get(url,impersonate="chrome120").text
    dom = BTSP(response,"html.parser")

    noResultsFoundContainer = dom.find_all(attrs={"class": "no-search-results"})

    if noResultsFoundContainer: 
        return payload

    try:
        dataContainer = dom.find_all(attrs={"type": "application/ld+json"})
        assert len(dataContainer) == 1
        dom = dataContainer[0]
    except:
        return payload

    listings = html_innertext_to_json(dom)
    if listings:
        payload = listings
    
    time.sleep(2)
   
    return payload

def parse_response(payload):
    listings = filter(lambda response: bool(response),payload)
    return [listing for subList in listings for listing in subList]

def apply_filters(base_url,filters):
    assert all(filterGroup in filters for filterGroup in ["city","rentalPrice","datePosted","minNumberOfBedrooms"])
    
    cities = [city.lower().replace(" ","-") for city in filters["city"]]
    filterUrls = map(lambda city: create_path([base_url,city]), cities)
    
    filterUrls = map(lambda url: create_path([url,filters["minNumberOfBedrooms"]]),filterUrls)

    priceRange = [str(price) for price in filters["rentalPrice"].values()]
    priceRange = "-".join(priceRange)
    filterUrls = map(lambda url: create_path([url,priceRange]),filterUrls)
    
    filterUrls = map(lambda url: create_path([url,filters["datePosted"]]),filterUrls)

    return list(filterUrls)

def request_geographies(base_url,filters):
    urls = apply_filters(base_url,filters)
    listings = list(map(lambda url: request(url), urls))
    return listings

def pipeline():
    pipelineSetup = {
                      "request": {
                                   "function": request_geographies,
                                   "args": [
                                             create_path([source["domain"],source["endpoint"]]),
                                             source["filters"]
                                           ]
                                 },
                      "parser": parse_response,
                      "directory": source["path"],
                      "file": source["localFileName"],
                      "model": model,
                      "source": source["name"],
                      "hostUrl": source["domain"],
                      "listingUrlColumn": model.itemUrl,
                      "filter": None
                    }

    worker = Pipeline(pipelineSetup)
    return worker.execute()

