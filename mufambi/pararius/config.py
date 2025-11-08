parariusConfig = {
                   "name": "Pararius",
                   "domain": "https://www.pararius.nl",
                   "endpoint": "huurwoningen",
                   "filters": {
                                "rentalPrice": { "min": 850, "max": 1500 },
                                "datePosted": "sinds-1",
                                "city": ["Amsterdam","Eindhoven","Den Haag","Rotterdam","Utrecht"]
                              },
                   "responseType": "html",
                   "requestParams": {
                                      "page": 1
                                    },
                   "path": "/app/mufambi/pararius",
                   "localFileName": "pararius.json"
                 }           

