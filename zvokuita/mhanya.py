import json
from config import configDict
from data import pipeline

def run():
    # sanganisa target yoga nemumushandi anoita zvese 
    # achishandisa config yaanenge apuhwa
    for source in configDict.values():
        pipeline(source)
    
    # KANA NDAZOFUNGA
    # trigger remotely

if __name__ == "__main__":
    run()
