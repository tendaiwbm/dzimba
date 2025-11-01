verraConfig = {
                 "name": "VERRA Makelaars",
                 "domain": "https://verra.nl",
                 "endpoint": "nl/realtime-listings/consumer",
                 "responseType": "json",
                 "filters": 
                           {
                             "city": ["Rotterdam","Amsterdam","Utrecht","Den Haag","The Hague","Hoofddorp","Eindhoven"],
                             "energyLabel": ["A++++","A+++","A++","A+","A","B","C"],
                             "isForRental": True,
                             "rentalStatusNL": "Beschikbaar",
                             "rentalStatusEN": "available",
                             "rentalPrice": {"min": 1000, "max": 2000}
                           },
                 "path": "/app/mufambi/verra",
                 "localFileName": "verra.json"
              }           
