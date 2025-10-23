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
from ..mail import prepare_data, send_email
from ..writers import write_json
from ..readers import read_json

def find_new_listing_ids(old,new,unique_id_column):
    updatedSet = p.CategoricalIndex(new[unique_id_column])
    previousSet = p.CategoricalIndex(old[unique_id_column])
    return updatedSet.difference(previousSet)

def extract_new_listings(old,new,unique_id_column):
    if isinstance(old,type(None)): return new

    newListingIds = find_new_listing_ids(old,new,unique_id_column)
    
    if newListingIds.empty: 
        return
   
    newListings = new[new[unique_id_column].isin(newListingIds)]

    return newListings

def update_known_listings(old,new):
    if isinstance(old,type(None)): return new

    return p.concat([old,new])

def save_known_listings(listings,path,filename):
    write_json(listings,create_path([path,filename]))     

def dict_rows_to_df(dict_rows):
    return p.DataFrame(dict_rows)

def get_create_local_copy(path,filename,data):
    filepath = create_path([path,filename])
    
    if filename in os.listdir(path):
        return dict_rows_to_df(read_json(filepath))
    else:
        write_json(data,filepath)

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

def request_geographies(params,urls):
    listings = map(lambda url: request(url,params), urls)
    listings = filter(lambda response: bool(response),listings)
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

def validate(data,model):
    validatedData = model.validate(data)
    return dict_rows_to_df(validatedData)

def pipeline():
    baseUrl = create_path([source["domain"],source["endpoint"]])
    filterUrls = apply_filters(baseUrl,source["filters"])
    responses = request_geographies(source["requestParams"],filterUrls)
    
    if not responses:
        return False

    filteredListings = validate(responses,model)
    knownListings = get_create_local_copy(source["path"],source["localFileName"],filteredListings)
    newListings = extract_new_listings(knownListings,filteredListings,model.id_)
    
    try:
        assert newListings is not None
    except:
        return False

    knownListings = update_known_listings(knownListings,newListings)
    save_known_listings(knownListings,source["path"],source["localFileName"])
    
    return { source["name"]: newListings, "domain": source["domain"], "endpoint": model.itemUrl }

