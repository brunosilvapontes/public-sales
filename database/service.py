# service.py
# Python 3.7.4
from database.models import Auction

def updateAuctions(source, currentAuctions):
    # Get all active auctions from source
    for x in Auction.objects(title__nin=['50% DO IMÓVEL NA QN 513 - SAMAMBAIA/DF']):
        print(f'->> {x.title}')

    # for currentAuction in currentAuctions:
    #     currentAuction.save()
