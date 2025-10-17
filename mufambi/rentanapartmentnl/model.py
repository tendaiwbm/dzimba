def check_keys(props,listing):
    for key in props:
        try:
            assert props[key] in listing
        except:
            print(f"key {props[key]} not found")


class RAANLModel:
    id_ = "_id"
    itemUrl = "url"
    city = "city"
    price = "price"
    energyLabel = "energyLabel"
    
    def validate(data):
        props = RAANLModel.__dict__
        props = {key: props[key] for key in props if not(key.startswith("__")) and not(key == "validate")}
        
        list(map(lambda listing: check_keys(props,listing),data))
        
        return data
