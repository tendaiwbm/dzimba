import logging
from os import getenv
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename=getenv("log_filename_main"))

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
                #liv,
                wzk,
              )
    
    msgScaffolding = '-'*50
    logging.info(f"{msgScaffolding} Initiating Dzimba {msgScaffolding}")

    for trigger in sources:
        trigger()

    logging.info(f"{msgScaffolding} Terminating Dzimba {msgScaffolding}")

if __name__ == "__main__":
    run()
