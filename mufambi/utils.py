import os
import logging

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

    def set_logger(self):
        try:
            assert "logger" in self.config
            self.logger = self.config["logger"]
        except:
            logging.warning(f"No logger configured for source {self.config['source']}.")
            self.logger = logging
        
    def request(self):
        self.logger.debug(f"Fetching data for source {self.config['source']}")
        function = self.config["request"]["function"]
        args = self.config["request"]["args"]
        return function(*args)

    def parse_payload(self,payload):
        self.logger.debug(f"Parsing data for source {self.config['source']}")
        return self.config["parser"](payload)
    
    def validate(self,data):
        self.logger.debug(f"Validating data for source {self.config['source']}")
        validatedData = self.config["model"].validate(data)
        return dict_rows_to_df(validatedData)

    def apply_filters(self,data):
        self.logger.debug(f"Filtering data for source {self.config['source']}")
        self.logger.info(f"Applying filters on source '{self.config["source"]}'.")
        self.logger.info(f"Number of listings before filtering:\t{len(data)}")

        message = "Number of listings after applying filter '{}':\t{}"
        filters = self.config["filter"]
        model = self.config["model"]

        if "city" in filters:
            data = data[data[model.city].isin(filters["city"])]
            self.logger.info(message.format("city",len(data)))

        if "isForRental" in filters:
            data = data[data[model.forRental]]
            self.logger.info(message.format("isForRental",len(data)))

        if "rentalStatusNL" in filters:
            data = data[data[model.status] == filters["rentalStatusNL"]]
            self.logger.info(message.format("rentalStatusNL",len(data)))

        if "rentalStatusEN" in filters:
            data = data[data[model.statusEN] == filters["rentalStatusEN"]]
            self.logger.info(message.format("rentalStatusEN",len(data)))

        if "rentalPrice" in filters:
            data = data.loc[(data[model.rentalPrice] >= filters["rentalPrice"]["min"]) &
                            (data[model.rentalPrice] <= filters["rentalPrice"]["max"])]
            self.logger.info(message.format("rentalPrice",len(data)))

        if "energyLabel" in filters:
            try:
                assert model.energyLabel in data.columns
                assert all(p.notna(data[model.energyLabel]))
                
                data = data[(data[model.energyLabel] == None) | 
                            (data[model.energyLabel].isin(filters["energyLabel"]))]
                
                self.logger.info(message.format("energyLabel",len(data)))
            except:
                self.logger.warning(f"Filtering by energy label failed for source '{self.config["source"]}'")

        return data

    def get_create_local_copy(self,data):
        filepath = create_path([self.config["directory"],self.config["file"]])

        if self.config["file"] in os.listdir(self.config["directory"]):
            self.logger.info(f"Local copy for {self.config['source']} already created. Retrieving")
            return dict_rows_to_df(read_json(filepath))
        else:
            self.logger.info(f"Local copy for {self.config['source']} does not exist. Creating")
            write_json(data,filepath)

    def extract_new_listings(self,old,new):
        if isinstance(old,type(None)): 
            self.logger.info(f"All {len(new)} listings from {self.config['source']} new")
            return new
        
        unique_id_column = self.config["model"].id_

        updatedSet = p.CategoricalIndex(new[unique_id_column])
        previousSet = p.CategoricalIndex(old[unique_id_column])
        newListingIds = updatedSet.difference(previousSet)

        if newListingIds.empty: 
            self.logger.info(f"No new listings extracted from {self.config['source']}")
            return

        newListings = new[new[unique_id_column].isin(newListingIds)]
        self.logger.info(f"{len(newListings)} new listings found from {self.config['source']} after diffing with local copy")

        return newListings

    def update_known_listings(self,old,new):
        if isinstance(old,type(None)): 
            self.logger.info(f"All {len(new)} listings from {self.config['source']} new, therefore first known copy")
            return new

        return p.concat([old,new])

    def save_known_listings(self,listings):
        self.logger.info(f"Saving {len(new)} known listings from {self.config['source']} into local copy")
        
        write_json(listings,
                   create_path([self.config["directory"],
                   self.config["file"]]))

    def prepare_email_payload(self,listings):
        assert isinstance(listings,p.DataFrame)

        listings[self.config["listingUrlColumn"]] = self.config["hostUrl"] + listings[self.config["listingUrlColumn"]]
        listingDetailUrls = listings[self.config["listingUrlColumn"]].tolist()
        formattedListings = "\n".join(listingDetailUrls)
        
        return formattedListings

    def email(self,listings):
        if isinstance(listings,p.DataFrame) and len(listings) > 0:
            payload = self.prepare_email_payload(listings)
            send_email(self.config["source"],payload)
        else:
            self.logger.critical(f"Payload containing {len(listings)} listings from {self.config['source']} received as type {type(listings)} not emailed")
        
    def execute(self):
        self.set_logger()

        response = self.request()

        if not(response): 
            self.logger.info(f"No results returned in response from {self.config['source']}")
            return
        
        if self.config["parser"]:
            response = self.parse_payload(response)
        if not(response): 
            self.logger.info(f"No listings extracted after parsing response from {self.config['source']}") 
            return

        currentListings = self.validate(response)
        
        if self.config["filter"]:
            currentListings = self.apply_filters(currentListings)

        knownListings = self.get_create_local_copy(currentListings)
        newListings = self.extract_new_listings(knownListings,currentListings)

        try:    
            assert newListings is not None
        except:
            self.logger.info(f"No new listings from {self.config['source']}")
            return

        knownListings = self.update_known_listings(knownListings,newListings)
        self.save_known_listings(knownListings)
        
        #self.email(newListings)
