WoonzekerConfig = {
                 "name": "Woonzeker",
                 "host": "https://woonzeker.com/huur/woningen",
                 "dataUrl": "https://woonzeker.com/api/ms/listing/properties?page=1&perPage=30&sort=stage&filter[price]=1000,2000&filter[import_type]=RentResident",
                 "responseType": "json",
                 "filters": 
                           {
                             "rentalStatusNL": "Beschikbaar",
                           },
                 "path": "/app/mufambi/woonzeker",
                 "localFileName": "woonzeker.json"
              }           
