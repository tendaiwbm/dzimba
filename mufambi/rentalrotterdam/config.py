rentalRotterdamConfig = {
                          "name": "Rental Rotterdam",
                          "domain": "https://www.rentalrotterdam.nl",
                          "endpoint": "0-2ac6/aanbod-pagina",
                          "requestParams" : { 
                                              "take": 14, 
                                              "availability": 1, 
                                              "pricerange.minprice": 800,
                                              "pricerange.maxprice": 1400,
                                              "forsaleorrent": "FOR_RENT"
                                            },
                          "responseType": "html",
                          "filters": 
                                    {
                                      "energyLabel": ["A++++","A+++","A++","A+","A","B","C"],
                                      "city": ["Rotterdam","Den Haag","Delft"]
                                    },
                          "path": "/app/mufambi/rentalrotterdam",
                          "localFileName": "rentalrotterdam.json"
                        }           
