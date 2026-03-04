import os
import time
import random
import requests as rq
import pandas as p
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

def request(url,params):
    pageFound = True
    payload = []
    
    userAgents = [
                   "Mozilla/5.0 (Windows NT 10.0; Win64;x64;rv131.0) Gecko/20100101 Firefox/131.0",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
                   "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
                 ]
    
    while pageFound:
        page = "-".join(["page",str(params["page"])])
        encodedUrl = create_path([url,page])
    
        request = rq.get(encodedUrl,headers={"User-Agent": random.choice(userAgents), "Host": "www.pararius.nl"})
        try:
            # use @graph[offers][offerCount] as termination condition
            # refactor to attempt termination after parsing dom
            assert len(request.history) == 1
            assert request.history[0].status_code == 301
            print("history check success")
        except:
            print("history check failure") 
            break

        response = request.text
        dom = BTSP(response,"html.parser")
        pageNotFoundContainer = dom.find_all(attrs={"class": "page__notifications"})[0].find_all(attrs={"class": "notification__title"})

        if pageNotFoundContainer: 
            break
        
        try:
            dataContainer = dom.find_all(attrs={"type": "application/ld+json"})
            assert len(dataContainer) == 1
            dom = dataContainer[0]
        except:
            break

        listings = html_innertext_to_json(dom)
        if listings:
            payload += listings
        
        time.sleep(3)
       
        params["page"] += 1
        
    return payload

def parse_response(payload):
    listings = filter(lambda response: bool(response),payload)
    return [listing for subList in listings for listing in subList]

def apply_filters(base_url,filters):
    assert all(filterGroup in filters for filterGroup in ["city","rentalPrice","datePosted"])
    
    cities = [city.lower().replace(" ","-") for city in filters["city"]]
    random.shuffle(cities)
    filterUrls = map(lambda city: create_path([base_url,city]), cities)

    priceRange = [str(price) for price in filters["rentalPrice"].values()]
    priceRange = "-".join(priceRange)
    filterUrls = map(lambda url: create_path([url,priceRange]),filterUrls)
    
    filterUrls = map(lambda url: create_path([url,filters["datePosted"]]),filterUrls)

    return list(filterUrls)

def request_geographies(params,base_url,filters):
    urls = apply_filters(base_url,filters)
    listings = list(map(lambda url: request(url,params), urls))
    return listings

def pipeline():
    pipelineSetup = {
                      "request": {
                                   "function": request_geographies,
                                   "args": [
                                             source["requestParams"],
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

