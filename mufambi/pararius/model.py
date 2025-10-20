def check_keys(props,listing):
    for key in props:
        if props[key] != "energyLabel":
            try:
                assert props[key] in listing
            except:
                print(f"key {props[key]} not found")


class ParariusModel:
    id_ = "_id"
    itemUrl = "url"
    
    def validate(data):
        props = ParariusModel.__dict__
        props = {key: props[key] for key in props if not(key.startswith("__")) and not(key == "validate")}
        
        list(map(lambda listing: check_keys(props,listing),data))
        
        return data
