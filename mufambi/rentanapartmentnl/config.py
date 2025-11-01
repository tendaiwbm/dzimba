raanlConfig = {
                 "name": "Rent An Apartment NL",
                 "domain": "https://www.rentanapartment.nl",
                 "endpoint": "woningaanbod",
                 "responseType": "html",
                 "requestParams": {
                                    "page": 1
                                  },
                 "filters": 
                           {
                             "city": ["Rotterdam","Delft","Den Haag","The Hague"],
                             "energyLabel": ["A++++","A+++","A++","A+","A","B","C"],
                             "rentalPrice": {"min": 1000, "max": 2000}
                           },
                 "path": "/app/mufambi/rentanapartmentnl",
                 "localFileName": "raanl.json"
              }           
