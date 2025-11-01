import os
import time
import requests as rq
import pandas as p

from bs4 import BeautifulSoup as BTSP
from bs4.element import NavigableString

from .model import HouseHuntingModel as model
from .config import rentalRotterdamConfig as source
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

def extract_unique_ids(listings,id_column_name,url_column_name):
    def extract_id(listing,id_column_name,url_column_name):
        listing[id_column_name] = listing[url_column_name].split("/")[-2]
        return listing
    
    return list(map(lambda listing: extract_id(listing,id_column_name,url_column_name),listings))

def dom_articles_to_json(dom):
    def dom_article_to_json(article):
        listingData = article.find_all(attrs={"class": "object__data"})[0]
        price = listingData.find_all(attrs={"class": "price"})[0].text.replace("€","").strip().split(",")[0]
        

        '''
        return {
                 "_id": 1,
                 "url": 1,
                 "price": int(price) if "." not in price else int(float(price)*1000),
                 "city": 1,
                 "energyLabel": 1
               }
        '''

    dom = BTSP(dom,"html.parser").find_all("article")
    return list(map(dom_article_to_json,dom))

def request(url,params,id_column_name,url_column_name,domain):
    try:
        assert params["skip"] == 0
    except:
        params["skip"] = 0

    pageFound = True
    payload = []
    while pageFound:
        request = rq.post(url,data=params)
        
        try:    assert request.status_code == 200
        except: break
        
        response = request.text
        pageFound = "Geen objecten gevonden" not in str(response)
        
        if not(pageFound): break

        payload += [dom_articles_to_json(response)]
        params["skip"] += params["take"]
    
    return payload

def validate(data,model):
    validatedData = model.validate(data)
    return dict_rows_to_df(validatedData)

def apply_filters(data,filters,model):
    print(f"Number of listings before filtering:\t{len(data)}")
    message = "Number of listings after applying a filter on '{}':\t{}"

    if "city" in filters:
        data = data[data[model.city].isin(filters["city"])]
        print(message.format("city",len(data)))
    
    return data

def pipeline():
    url = create_path([source["domain"],source["endpoint"]])
    response = request(url,source["requestParams"],model.id_,model.itemUrl,source["domain"])
    exit()
    currentListings = validate(response,model)
    filteredListings = apply_filters(currentListings,source["filters"],model)
    knownListings = get_create_local_copy(source["path"],source["localFileName"],filteredListings)
    newListings = extract_new_listings(knownListings,filteredListings,model.id_)
    
    try:
        assert newListings is not None
    except:
        return False
    
    knownListings = update_known_listings(knownListings,newListings)
    save_known_listings(knownListings,source["path"],source["localFileName"])
    
    return { source["name"]: newListings, "domain": source["domain"], "endpoint": model.itemUrl }
