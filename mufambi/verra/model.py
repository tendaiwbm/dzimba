def check_keys(props,listing):
    for key in props:
        if props[key] != "energyLabel":
            try:
                assert props[key] in listing
            except:
                print(f"key {props[key]} not found")


class VerraModel:
    id_ = "_id"
    itemUrl = "url"
    address = "address"
    state = "state"
    zipcode = "zipcode"
    city = "city"
    district = "district"
    neighbourhood = "neighbourhood"
    country = "country"
    forSale = "isSales"
    forRental = "isRentals"
    price = "price"
    rentalPrice = "rentalsPrice"
    numRooms = "rooms"
    numBedrooms = "bedrooms"
    furnished = "isFurnished"
    partlyFurnished = "isPartlyFurnished"
    renovated = "isRenovated"
    isShell = "isShell"
    shortStay = "isShortStay"
    new = "isNew"
    status = "status"
    statusEN = "statusOrig"
    hasGarden = "garden"
    hasBalcony = "balcony"
    energyLabel = "energyLabel"
    constructionDate = "dateOfConstruction"
    
    def validate(data):
        props = VerraModel.__dict__
        props = {key: props[key] for key in props if not(key.startswith("__")) and not(key == "validate")}
        
        list(map(lambda listing: check_keys(props,listing),data))
        
        return data
