import time
import requests as rq
import pandas as p
from bs4 import BeautifulSoup as BTSP
from bs4.element import NavigableString 

from .model import RAANLModel as model
from .config import raanlConfig as source
from ..utils import *

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

        time.sleep(1)

        payload += dom
        params["skip"] += 12

    return payload
    
def parse_response(payload):
    dom = map(dom_article_to_json,payload)
    dom = filter(lambda listing: listing != None, dom)
    return list(dom)

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
                      "filter": source["filters"]
                    }

    worker = Pipeline(pipelineSetup)
    return worker.execute()
