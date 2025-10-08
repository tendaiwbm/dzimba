import os
import json
import requests as rq
import polars as bear

def create_filepath(path,filename):
    return "/".join([path,filename])

def dict_rows_to_df(dict_rows):
    return bear.DataFrame(dict_rows,orient="row")

def get_create_local_copy(path,filename,data):
    filepath = create_filepath(path,filename)
    
    if filename in os.listdir(path):
        mode = "r"
    else:
        mode = "w"
    
    with open(filepath,mode) as f:
        if mode == "w":
            jsonData = data.to_dicts()
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
    validatedResponse = validate(response,source["model"])
    localFile = get_create_local_copy(source["path"],source["localFileName"],validatedResponse)
    

