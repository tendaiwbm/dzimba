from datetime import datetime

househuntingConfig = {
                       "name": "HouseHunting",
                       "domain": "https://househunting.nl",
                       "endpoint": "wp-json/houses/posts",
                       "requestParams" : { 
                                           "page": 1, 
                                           "available-since": datetime.strftime(datetime.today(),"%Y-%m-%d"), 
                                           "type": "for-rent", 
                                           "min-price": 800,
                                           "max-price": 1800 
                                         },
                       "responseType": "json",
                       "filters": 
                                 {
                                   "city": ["Eindhoven","Rotterdam","Amsterdam","Utrecht"],
                                 },
                       "path": "/app/mufambi/househunting",
                       "localFileName": "househunting.json"
                     }           
