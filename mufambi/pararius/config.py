parariusConfig = {
                   "name": "Pararius",
                   "domain": "https://www.pararius.nl",
                   "endpoint": "huurwoningen",
                   "filters": {
                                "rentalPrice": { "min": 1000, "max": 1800 },
                                "datePosted": "sinds-1",
                                "minNumberOfBedrooms": "2-slaapkamers",
                                "city": ["Haarlem",
                                         "Amersfoort",
                                         "Hilversum",
                                         "Weesp",
                                         "Utrecht",
                                         "Delft",
                                         "Den Bosch",
                                         "Den Haag",
                                         "Almere",
                                         "Utrecht",
                                         "Lelystad",
                                         "Leiden",
                                         "Gouda"]
                              },
                   "responseType": "html",
                   "path": "/app/mufambi/pararius",
                   "localFileName": "pararius.json"
                 }           

