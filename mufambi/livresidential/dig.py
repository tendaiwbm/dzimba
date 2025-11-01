import os
import time
import json
import requests as rq
import pandas as p

from bs4 import BeautifulSoup as BTSP

from .model import LIVResidentialModel as model
from .config import LivResidentialConfig as source
from ..utils import *
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

def parse_response(payload):
    def parse_listing(listing):
        listing = listing["_formatted"]
        return {
                 "_id": "-".join([listing["address_1"].replace(",","").replace(" ","-").lower(),listing["id"]]),
                 "url": create_path([listing["slug_city"],listing["slug_neighborhood"],listing["slug_street"]])
               }

    return list(map(parse_listing,payload))

def request(url,params,headers):

    request = rq.post(url,data=json.dumps(params),headers=headers)
        
    try:    assert request.status_code == 200
    except: return payload
        
    response = request.json()
    assert "hits" in response
    
    return response["hits"]

def validate(data,model):
    validatedData = model.validate(data)
    return dict_rows_to_df(validatedData)

def pipeline():
    url = source["dataUrl"]
    payload = request(url,source["requestParams"],source["headers"])
    response = parse_response(payload)
    currentListings = validate(response,model)
    knownListings = get_create_local_copy(source["path"],source["localFileName"],currentListings)
    newListings = extract_new_listings(knownListings,currentListings,model.id_)
    
    try:
        assert newListings is not None
    except:
        return False
    
    knownListings = update_known_listings(knownListings,newListings)
    save_known_listings(knownListings,source["path"],source["localFileName"])
    
    return { source["name"]: newListings, "domain": source["domain"], "endpoint": model.itemUrl }
