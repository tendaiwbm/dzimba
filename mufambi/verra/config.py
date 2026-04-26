verraConfig = {
                 "name": "VERRA Makelaars",
                 "domain": "https://verra.nl",
                 "endpoint": "nl/realtime-listings/consumer",
                 "responseType": "json",
                 "filters": 
                           {
                             "city": [
                                       "Utrecht",
                                       "Den Haag",
                                       "The Hague",
                                       "Hoofddorp",
                                       "Haarlem",
                                       "Delft",
                                       "Weesp",
                                       "Leiden",
                                       "Gouda",
                                       "Almere",
                                       "Lelystad",
                                       "Hilversum",
                                       "Amersfoort",
                                       "Den Bosch"
                                     ],
                             "energyLabel": ["A++++","A+++","A++","A+","A","B","C"],
                             "isForRental": True,
                             "rentalStatusNL": "Beschikbaar",
                             "rentalStatusEN": "available",
                             "rentalPrice": {"min": 1000, "max": 2000}
                           },
                 "path": "/app/mufambi/verra",
                 "localFileName": "verra.json"
              }           
