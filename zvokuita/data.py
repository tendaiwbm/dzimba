import os
import json
import requests as rq
import pandas as p
from writers import write_json
import mail

def find_new_listing_ids(old,new,unique_id_column):
    updatedSet = p.CategoricalIndex(new[unique_id_column])
    previousSet = p.CategoricalIndex(old[unique_id_column])
    return updatedSet.difference(previousSet)

def extract_new_listings(old,new,unique_id_column):
    if isinstance(old,type(None)): return new

    newListingIds = find_new_listing_ids(old,new,unique_id_column)
    
    if newListingIds.empty: 
        exit("No new listings matching search criteria found.")
   
    newListings = new[new[unique_id_column].isin(newListingIds)]

    return newListings

def update_known_listings(old,new):
    if isinstance(old,type(None)): return new

    return p.concat([old,new])

def save_known_listings(listings,path,filename):
    write_json(listings,create_path([path,filename]))     

def create_path(parts):
    return "/".join(parts)

def dict_rows_to_df(dict_rows):
    return p.DataFrame(dict_rows)

def get_create_local_copy(path,filename,data):
    filepath = create_path([path,filename])
    
    if filename in os.listdir(path):
        mode = "r"
        with open(filepath,mode) as f:
            return dict_rows_to_df(json.load(f))
    else:
        mode = "w"
        write_json(data,filepath)

def request(url):
    return rq.get(url).json()

def validate(data,model):
    validatedData = model.validate(data)
    return dict_rows_to_df(validatedData)

def apply_filters(data,filters,model):
    print(f"Number of listings before filtering:\t{len(data)}")
    message = "Number of listings after applying a filter on '{}':\t{}"

    if "city" in filters:
        data = data[data[model.city].isin(filters["city"])]
        print(message.format("city",len(data)))
    
    if "isForRental" in filters:
        data = data[data[model.forRental]]
        print(message.format("isForRentalPrice",len(data)))
        
        if "rentalStatusNL" in filters:
            data = data[data[model.status] == filters["rentalStatusNL"]]
            print(message.format("rentalStatusNL",len(data)))

        if "rentalStatusEN" in filters:
            data = data[data[model.statusEN] == filters["rentalStatusEN"]]
            print(message.format("rentalStatusEN",len(data)))
        
        if "rentalPrice" in filters:
            data = data.loc[(data[model.rentalPrice] >= filters["rentalPrice"]["min"]) & 
                            (data[model.rentalPrice] <= filters["rentalPrice"]["max"])]
            print(message.format("rentalPrice",len(data)))
     
    if "energyLabel" in filters:
        try: 
            assert model.energyLabel in data.columns
            data = data[data[model.energyLabel].isin(filters["energyLabel"])]
            print(message.format("energyLabel",len(data)))
        except:
            pass
            
    return data


def pipeline(source):
    url = create_path([source["domain"],source["endpoint"]])
    response = request(url)
    currentListings = validate(response,source["model"])
    currentListings = apply_filters(currentListings,source["filters"],source["model"])
    knownListings = get_create_local_copy(source["path"],source["localFileName"],currentListings)
    newListings = extract_new_listings(knownListings,currentListings,source["model"].id_)
    knownListings = update_known_listings(knownListings,newListings)
    save_known_listings(knownListings,source["path"],source["localFileName"])
    payload = mail.prepare_data(newListings,source["domain"],source["model"].itemUrl)
    mail.send_email(source["name"],payload)

