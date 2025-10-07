import requests as r

if __name__ == "__main__":
    data = r.get("")
    print(data.json())
