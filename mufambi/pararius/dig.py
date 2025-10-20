import os
import time
import requests as rq
import pandas as p
from bs4 import BeautifulSoup as BTSP
from bs4.element import NavigableString 

from .model import ParariusModel as model
from .config import parariusConfig as source
from .config import geographies
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

def list_item_to_json(list_item):
    aTag = list_item.find_all(attrs={"class": "listing-search-item__link listing-search-item__link--depiction"})[0]

    return {
            "url": aTag.attrs["href"],
            "_id": aTag.attrs["href"].split("/")[-2]
           }

def request(url,params):
    pageFound = True
    payload = []
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64;x64;rv131.0) Gecko/20100101 Firefox/131.0"}
    while pageFound:
        page = "-".join(["page",str(params["page"])])
        encodedUrl = create_path([url,page])
    
        request = rq.get(encodedUrl)
        try:
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
            dom = dom.find_all(attrs={"class": "search-list"})
            assert len(dom) == 1
            
            dom = dom[0].find_all(attrs={"class": "search-list__item search-list__item--listing"})
        except:
            pageFound = False

        dom = map(list_item_to_json,dom)
        dom = filter(lambda listing: listing != None, dom)
        payload += dom
       
        time.sleep(3)

        params["page"] += 1
        
    return payload

def request_geographies(params,urls):
    listings = [request(url,params) for url in urls]
    listings = filter(lambda response: bool(response),listings)
    return [listing for subList in listings for listing in subList]

def encode_subgeo_name(name,value):
    value = value.replace(" ","-").lower()
    return "-".join([name,value])

def encode_subgeo_names(subgeo):
    subgeoName, subgeoValues = subgeo
    return map(lambda value: encode_subgeo_name(subgeoName,value),subgeoValues)

def construct_paths_per_geography(geography):
    geo = geography[0].replace(" ","-").lower()
    encodedNames = list(list(map(encode_subgeo_names,geography[1].items()))[0])
    geoPaths = map(lambda name: create_path([geo,name]),encodedNames)
    return list(geoPaths)

def construct_geo_urls(domain,endpoint,geographies):
    geoPaths = list(map(construct_paths_per_geography,geographies.items()))
    geoPaths =  [path for geo in geoPaths for path in geo]
    return list(map(lambda geoPath: create_path([domain,endpoint,geoPath]),geoPaths))

def apply_filters(urls,filters):
    if "rentalPrice" in filters:
        priceRange = [str(price) for price in filters["rentalPrice"].values()]
        priceRange = "-".join(priceRange) 
        urls = map(lambda url: create_path([url,priceRange]),urls)

    if "datePosted" in filters:
        urls = map(lambda url: create_path([url,filters["datePosted"]]),urls)

    return list(urls)

def validate(data,model):
    validatedData = model.validate(data)
    return dict_rows_to_df(validatedData)

def pipeline():
    geoUrls = construct_geo_urls(source["domain"],source["endpoint"],geographies)
    geoUrls = apply_filters(geoUrls,source["filters"])
    responses = request_geographies(source["requestParams"],geoUrls)
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

