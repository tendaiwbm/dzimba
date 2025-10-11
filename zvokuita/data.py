import os
import json
import requests as rq
import pandas as p
import polars as bear
from writers import write_json
import mail

def find_new_listing_ids(old,new,unique_id_column):
    updatedSet = p.CategoricalIndex(new[unique_id_column])
    previousSet = p.CategoricalIndex(old[unique_id_column])
    return updatedSet.difference(previousSet)

def extract_new_listings(old,new,unique_id_column):
    newListingIds = find_new_listing_ids(old,new,unique_id_column)
    newListings = new[new[unique_id_column].isin(newListingIds)]
    return newListings

def update_known_listings(old,new):
    return p.concat([old,new])

def save_known_listings(listings,path,filename):
    write_json(listings,create_filepath(path,filename))     

def create_filepath(path,filename):
    return "/".join([path,filename])

def dict_rows_to_df(dict_rows):
    return p.DataFrame(dict_rows)

def get_create_local_copy(path,filename,data):
    filepath = create_filepath(path,filename)
    
    if filename in os.listdir(path):
        mode = "r"
    else:
        mode = "w"
    
    with open(filepath,mode) as f:
        if mode == "w":
            jsonData = data.to_dict(orient="records")
            json.dump(jsonData,f)
            return 
        return dict_rows_to_df(json.load(f))

def request(url):
    return rq.get(url).json()

def validate(data,model):
    validatedData = model.validate(data)
    return dict_rows_to_df(validatedData)

def create_url(domain,endpoint):
    return "/".join([domain,endpoint])

def pipeline(source):
    url = create_url(source["domain"],source["endpoint"])
    response = request(url)
    updatedListings = validate(response,source["model"])
    knownListings = get_create_local_copy(source["path"],source["localFileName"],updatedListings)
    newListings = extract_new_listings(knownListings,updatedListings,source["model"].id_)
    knownListings = update_known_listings(knownListings,newListings)
    save_known_listings(knownListings,source["path"],source["localFileName"])
    payload = mail.prepare_data(newListings,source["domain"],source["model"].itemUrl)
    mail.send_email(source["name"],payload)

