import os
import time
import requests as rq
import pandas as p
from bs4 import BeautifulSoup as BTSP
from bs4.element import NavigableString 

from .model import RAANLModel as model
from .config import raanlConfig as source
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

def remove_from_list(item,list_object):
    while item in list_object:
        list_object.remove(item)

    return list_object

def convert_price_to_int(price):
    assert isinstance(price,str)
    if "." in price:
        price = float(price) * 1000
    
    return int(price)

def dom_article_to_json(article):
    try:
        assert article.contents[0] == "\n" and len(article.contents) == 2 
    except:
        return

    childElements = article.contents[1].contents
    childElements = remove_from_list("\n",childElements)
    
    if len(childElements) != 3: return
    
    childElementWithAvailability = childElements[0]
    try:
        assert not(childElementWithAvailability.find_all(attrs={"class": "object_status rented"}))
    except: 
        return
    
    childElementWithData = childElements[-1].contents
    childElementWithData = remove_from_list("\n",childElementWithData)
    energyLabelContainer = childElementWithAvailability.find_all(attrs={"class": "object_energyclass object_energyclass-a"})

    return {
            "_id": childElementWithData[0].find_all("a")[-1].attrs["data-property-id"],
            "price": convert_price_to_int(childElementWithData[-1].find_all("span")[0].contents[0].split(",")[0].split(" ")[-1]),
            "city": childElementWithData[1].contents[1].find_all("span")[-1].text,
            "url": childElementWithData[1].contents[1].attrs["href"].split("?")[0],
            "energyLabel": energyLabelContainer[0].text.strip() if energyLabelContainer else None 
           }

def request(url,params):
    try:
        assert params["skip"] == 0
    except:
        params["skip"] = 0

    pageFound = True
    payload = []
    while pageFound:
        queryString = "=".join(["skip",str(params["skip"])])
        encodedUrl = "?".join([url,queryString])
        request = rq.get(encodedUrl)
        response = request.text
        
        dom = BTSP(response,"html.parser")
        
        try:
            dom = dom.find_all(attrs={"class": ["object_list row"]})[0].find_all("article")
        except:
            pageFound = False
        
        if not(pageFound): break

        dom = map(dom_article_to_json,dom)
        dom = filter(lambda listing: listing != None, dom)

        time.sleep(3)

        payload += dom
        params["skip"] += 12

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


def pipeline():
    url = create_path([source["domain"],source["endpoint"]])
    response = request(url,source["requestParams"])
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
