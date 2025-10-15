import requests as rq
import time

def hh():
    pageFound = True
    form = { "page": 1, "available-since": "2025-10-01", "type": "for-rent", "min-price": 800, "max-price": 1800 }
    while pageFound:
        request = rq.post(url="https://househunting.nl/wp-json/houses/posts",data=form)
        response = request.json()
        time.sleep(3)
        pageFound = "posts" in response
        
        if not(pageFound):
            break
        
        print(form["page"])
        print(response["posts"])
        
        form["page"] = form["page"] + 100
        

if __name__ == "__main__":
    hh()
