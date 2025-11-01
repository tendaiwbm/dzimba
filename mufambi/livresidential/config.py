LivResidentialConfig = {
                          "name": "LIV Residential",
                          "domain": "https://www.livresidential.nl/huurwoningen/",
                          "dataUrl": "https://search.livresidential.nl/indexes/livnl_prod_properties/search",
                          "headers": {
                                       "Authorization": "Bearer e55820f9747fa8bf0973bf670007d9a04340dd818534004a757d54bad8e38e40",
                                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0",
                                       "Content-Type": "application/json"},
                          "requestParams" : {"q": "", 
                                             "facets": ["bedrooms","city","price","type"],
                                             "attributesToHighlight": ["*"],
                                             "highlightPreTag": "__ais-highlight__",
                                             "highlightPostTag": "__/ais-highlight__",
                                             "limit": 201,
                                             "offset": 0,
                                             "filter": [
                                                          [
                                                            "city=\"Amstelveen\"",
                                                            "city=\"Amsterdam\"",
                                                            "city=\"Den Haag\"",
                                                            "city=\"Eindhoven\"",
                                                            "city=\"Rotterdam\""
                                                          ],
                                                          "price>=700",
                                                          "price<=1500"
                                                       ]
                                            },
                          "responseType": "json",
                          "filters": 
                                    {
                                      "energyLabel": ["A++++","A+++","A++","A+","A","B","C"],
                                      "city": ["Rotterdam","Den Haag","Delft"]
                                    },
                          "path": "/app/mufambi/livresidential",
                          "localFileName": "livresidential.json"
                        }           
