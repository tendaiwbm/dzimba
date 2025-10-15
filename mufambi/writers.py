import json 

def write_csv(data,filepath,object_type="frame"):
    if object_type == "frame":
        data.to_csv(filepath,index=False)

def write_json(data,filepath,mode="w",object_type="frame"):
    with open(filepath,mode) as writer:
        if object_type == "frame":
            jsonData = data.to_dict(orient="records")
            json.dump(jsonData,writer)


