import logging

from mufambi.verra.dig import pipeline as verra
from mufambi.househunting.dig import pipeline as househunting
from mufambi.rentanapartmentnl.dig import pipeline as raanl
from mufambi.pararius.dig import pipeline as pararius
from mufambi.rentalrotterdam.dig import pipeline as rr
from mufambi.livresidential.dig import pipeline as liv
from mufambi.woonzeker.dig import pipeline as wzk

def run():
    sources = (
                verra,
                househunting,
                raanl,
                pararius,
                rr,
                liv,
                wzk,
              )
    
    for trigger in sources:
        trigger()

if __name__ == "__main__":
    run()
