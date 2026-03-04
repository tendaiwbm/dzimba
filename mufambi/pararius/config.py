parariusConfig = {
                   "name": "Pararius",
                   "domain": "https://www.pararius.nl",
                   "endpoint": "huurwoningen",
                   "filters": {
                                "rentalPrice": { "min": 800, "max": 1500 },
                                "datePosted": "sinds-1",
                                "city": ["Amsterdam","Eindhoven","Tilburg","Den Bosch","Dordrecht","Den Haag","Rotterdam","Utrecht","Hoofddorp"]
                              },
                   "responseType": "html",
                   "requestParams": {
                                      "page": 1
                                    },
                   "path": "/app/mufambi/pararius",
                   "localFileName": "pararius.json"
                 }           

