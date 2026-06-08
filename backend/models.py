from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, Numeric, func

# Shared SQLAlchemy instance

db = SQLAlchemy()

UserRole = Enum('Seller', 'Buyer', 'Admin', name='user_role')
ItemCondition = Enum('available', 'sold', 'removed', name='item_condition')
AuctionStatus = Enum('active', 'closed', 'cancelled', name='auction_status')
PaymentStatus = Enum('pending', 'completed', 'failed', name='payment_status')
ShipmentStatus = Enum('pending', 'shipped', 'delivered', name='shipment_status')

class User(db.Model):
    __tablename__ = 'users'

    login = db.Column(db.String(20), primary_key=True)
    phoneNum = db.Column(db.String(20))
    role = db.Column(UserRole, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    favoriteCategory = db.Column(db.String(255))

    items = db.relationship('Item', back_populates='seller', lazy=True)
    auctions = db.relationship('Auction', back_populates='seller', lazy=True, foreign_keys='Auction.sellerLogin')
    bids = db.relationship('Bid', back_populates='buyer', lazy=True)
    payments = db.relationship('Payment', back_populates='buyer', lazy=True)

    def serialize(self):
        return {
            'login': self.login,
            'phoneNum': self.phoneNum,
            'role': self.role,
            'address': self.address,
            'favoriteCategory': self.favoriteCategory
        }

class Item(db.Model):
    __tablename__ = 'items'

    itemId = db.Column(db.String(20), primary_key=True)
    itemName = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255))
    imageURL = db.Column(db.String(255))
    condition = db.Column(ItemCondition, nullable=False)
    startingPrice = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    sellerLogin = db.Column(db.String(20), db.ForeignKey('users.login'), nullable=False)

    seller = db.relationship('User', back_populates='items')

    def serialize(self):
        return {
            'itemId': self.itemId,
            'itemName': self.itemName,
            'category': self.category,
            'imageURL': self.imageURL,
            'condition': self.condition,
            'startingPrice': self.startingPrice,
            'description': self.description,
            'sellerLogin': self.sellerLogin
        }

class Auction(db.Model):
    __tablename__ = 'auctions'

    auctionId = db.Column(db.String(30), primary_key=True)
    auctionStatus = db.Column(AuctionStatus, nullable=False)
    currentHighestBid = db.Column(db.Float, nullable=False, default=0.0)
    sellerLogin = db.Column(db.String(20), db.ForeignKey('users.login'), nullable=False)
    itemId = db.Column(db.String(20), db.ForeignKey('items.itemId'), nullable=False)
    buyerLogin = db.Column(db.String(20), db.ForeignKey('users.login'))

    seller = db.relationship('User', foreign_keys=[sellerLogin], back_populates='auctions')
    buyer = db.relationship('User', foreign_keys=[buyerLogin])
    item = db.relationship('Item')
    bids = db.relationship('Bid', back_populates='auction', lazy=True)
    payment = db.relationship('Payment', back_populates='auction', uselist=False)
    shipment = db.relationship('Shipment', back_populates='auction', uselist=False)

    def serialize(self):
        return {
            'auctionId': self.auctionId,
            'auctionStatus': self.auctionStatus,
            'currentHighestBid': self.currentHighestBid,
            'sellerLogin': self.sellerLogin,
            'itemId': self.itemId,
            'itemName': self.item.itemName if self.item else None,
            'buyerLogin': self.buyerLogin,
            'highestBidder': self.buyerLogin
        }

class Payment(db.Model):
    __tablename__ = 'payments'

    paymentId = db.Column(db.String(30), primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    paymentStatus = db.Column(PaymentStatus, nullable=False)
    buyerLogin = db.Column(db.String(20), db.ForeignKey('users.login'), nullable=False)
    auctionId = db.Column(db.String(30), db.ForeignKey('auctions.auctionId'), unique=True, nullable=False)

    buyer = db.relationship('User', back_populates='payments')
    auction = db.relationship('Auction', back_populates='payment')

    def serialize(self):
        return {
            'paymentId': self.paymentId,
            'amount': self.amount,
            'paymentStatus': self.paymentStatus,
            'buyerLogin': self.buyerLogin,
            'auctionId': self.auctionId
        }

class Shipment(db.Model):
    __tablename__ = 'shipments'

    shipmentId = db.Column(db.String(30), primary_key=True)
    address = db.Column(db.Text, nullable=False)
    shipmentStatus = db.Column(ShipmentStatus, nullable=False)
    trackingNumber = db.Column(Numeric(10, 0))
    auctionId = db.Column(db.String(30), db.ForeignKey('auctions.auctionId'), unique=True, nullable=False)

    auction = db.relationship('Auction', back_populates='shipment')

    def serialize(self):
        return {
            'shipmentId': self.shipmentId,
            'address': self.address,
            'shipmentStatus': self.shipmentStatus,
            'trackingNumber': str(self.trackingNumber) if self.trackingNumber is not None else None,
            'auctionId': self.auctionId
        }

class Bid(db.Model):
    __tablename__ = 'bids'

    bidId = db.Column(db.String(30), primary_key=True)
    bidAmount = db.Column(db.Float, nullable=False)
    bidTimestamp = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    buyerLogin = db.Column(db.String(20), db.ForeignKey('users.login'), nullable=False)
    auctionId = db.Column(db.String(30), db.ForeignKey('auctions.auctionId'), nullable=False)

    buyer = db.relationship('User', back_populates='bids')
    auction = db.relationship('Auction', back_populates='bids')

    def serialize(self):
        return {
            'bidId': self.bidId,
            'bidAmount': self.bidAmount,
            'bidTimestamp': self.bidTimestamp.isoformat(),
            'buyerLogin': self.buyerLogin,
            'auctionId': self.auctionId
        }
