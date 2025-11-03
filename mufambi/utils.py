import os
import pandas as p

from .writers import write_json
from .readers import read_json
from .mail import send_email

def create_path(parts):
    return "/".join(parts)

def dict_rows_to_df(dict_rows):
    return p.DataFrame(dict_rows)

class Pipeline:
    def __init__(self,config):
        self.config = config

    def request(self):
        function = self.config["request"]["function"]
        args = self.config["request"]["args"]
        return function(*args)

    def parse_payload(self,payload):
        return self.config["parser"](payload)
    
    def validate(self,data):
        validatedData = self.config["model"].validate(data)
        return dict_rows_to_df(validatedData)

    def apply_filters(self):
        return

    def get_create_local_copy(self,data):
        filepath = create_path([self.config["directory"],self.config["file"]])

        if self.config["file"] in os.listdir(self.config["directory"]):
            return dict_rows_to_df(read_json(filepath))
        else:
            write_json(data,filepath)

    def extract_new_listings(self,old,new):
        if isinstance(old,type(None)): return new
        
        unique_id_column = self.config["model"].id_

        updatedSet = p.CategoricalIndex(new[unique_id_column])
        previousSet = p.CategoricalIndex(old[unique_id_column])
        newListingIds = updatedSet.difference(previousSet)

        if newListingIds.empty: return

        newListings = new[new[unique_id_column].isin(newListingIds)]

        return newListings

    def update_known_listings(self,old,new):
        if isinstance(old,type(None)): return new

        return p.concat([old,new])

    def save_known_listings(self,listings):
        write_json(listings,create_path([self.config["directory"],self.config["file"]]))

    def email(self,pipeline_result):
        #assert isinstance(listings,p.DataFrame)

        #listings[path_column_name] = source_domain_url + listings[path_column_name]
        #listingEndpoints = listings[path_column_name].tolist()
        #formattedListings = "\n".join(listingEndpoints)
        
        send_email(pipeline_result)
        
    def execute(self):
        payload = self.request()

        if not(payload): return False

        response = self.parse_payload(payload)
        currentListings = self.validate(response)

        if self.config["filter"]:
            currentListings = self.apply_filters(currentListings)

        knownListings = self.get_create_local_copy(currentListings)
        newListings = self.extract_new_listings(knownListings,currentListings)

        try:    assert newListings is not None
        except: return False

        knownListings = self.update_known_listings(knownListings,newListings)
        self.save_known_listings(knownListings)
        
        self.email({ self.config["source"]: newListings, "domain": self.config["hostUrl"], "endpoint": self.config["listingUrlColumn"] })
