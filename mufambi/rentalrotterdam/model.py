def check_keys(props,listing):
    for key in props:
        try:
            assert props[key] in listing
        except:
            raise KeyError(f"Key '{props[key]}' not found.")

class RentalRotterdamModel:
    id_ = "_id"
    energyLabel = "energyLabel"
    itemUrl = "url"
    city = "city"
    price = "price"

    def validate(data):
        props = RentalRotterdamModel.__dict__
        props = {key: props[key] for key in props if not(key.startswith("__")) and not(key == "validate")}

        list(map(lambda listing: check_keys(props,listing),data))

        return data

