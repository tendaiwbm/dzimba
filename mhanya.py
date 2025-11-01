from mufambi.verra.dig import pipeline as verra
from mufambi.househunting.dig import pipeline as househunting
from mufambi.rentanapartmentnl.dig import pipeline as raanl
from mufambi.pararius.dig import pipeline as pararius
from mufambi.rentalrotterdam.dig import pipeline as rr
from mufambi.livresidential.dig import pipeline as liv

from mufambi.mail import send_email

def run():
    # sanganisa target yoga nemumushandi anoita zvese 
    # achishandisa config yaanenge apuhwa
    listings = []
    sources = (
                verra,
                househunting,
                raanl,
                pararius,
                rr,
                liv,
              )
    for trigger in sources:
        pipelineResult = trigger()
        if pipelineResult:
            listings.append(pipelineResult)

    if listings:
        list(map(send_email,listings))

    # KANA NDAZOFUNGA
    # trigger remotely

if __name__ == "__main__":
    run()
