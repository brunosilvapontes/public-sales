# service.py
# Python 3.7.4
from database.models import Auction

def updateAuctions(source, currentAuctions):
    # Disable active auctions that is not in the current list
    currentTitles = [auction.title for auction in currentAuctions]
    Auction.objects(source=source, disabled=False, title__nin=currentTitles).update(
        set__disabled=True)

    # Create or update auctions
    for currentAuction in currentAuctions:
        Auction.objects(title=currentAuction.title).update_one(
            set__status=currentAuction.status,
            set__url=currentAuction.url,
            set__source=currentAuction.source,
            set__title=currentAuction.title,
            set__currentBid=currentAuction.currentBid,
            set__startingBid=currentAuction.startingBid,
            set__description=currentAuction.description,
            set__evaluation=currentAuction.evaluation,
            set__auction1Opening=currentAuction.auction1Opening,
            set__auction1Closure=currentAuction.auction1Closure,
            set__auction1Bid=currentAuction.auction1Bid,
            set__auction2Opening=currentAuction.auction2Opening,
            set__auction2Closure=currentAuction.auction2Closure,
            set__auction2Bid=currentAuction.auction2Bid,
            upsert=True)
