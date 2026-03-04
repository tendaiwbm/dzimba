from datetime import datetime

househuntingConfig = {
                       "name": "HouseHunting",
                       "domain": "https://househunting.nl",
                       "endpoint": "wp-json/houses/posts",
                       "requestParams" : { 
                                           "page": 1, 
                                           "available-since": datetime.strftime(datetime.today(),"%Y-%m-%d"), 
                                           "type": "for-rent", 
                                           "min-price": 700,
                                           "max-price": 1500 
                                         },
                       "responseType": "json",
                       "filters": 
                                 {
                                   "city": ["Eindhoven","Rotterdam","Tilburg","Den Bosch","Amsterdam","Utrecht"],
                                 },
                       "path": "/app/mufambi/househunting",
                       "localFileName": "househunting.json"
                     }           
