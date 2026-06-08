import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy.exc import OperationalError

from models import db, User, Item, Auction, Payment, Shipment, Bid


def create_app():
    app = Flask(__name__)
    database_url = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)

    with app.app_context():
        try:
            db.create_all()
        except OperationalError as exc:
            if database_url != 'sqlite:///app.db':
                print('Warning: could not connect to DATABASE_URL. Falling back to sqlite:///app.db')
                app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
                db.engine.dispose()
                db.create_all()
            else:
                raise

    def error(message, status=400):
        return jsonify({'error': message}), status

    @app.route('/api/status', methods=['GET'])
    def status():
        return jsonify({'status': 'ok'})

    @app.route('/api/users', methods=['GET'])
    def list_users():
        users = User.query.all()
        return jsonify([user.serialize() for user in users])

    @app.route('/api/items', methods=['GET', 'POST'])
    def items():
        if request.method == 'GET':
            return jsonify([item.serialize() for item in Item.query.all()])

        payload = request.get_json() or {}
        required = ['itemId', 'itemName', 'condition', 'startingPrice', 'sellerLogin']
        missing = [k for k in required if not payload.get(k)]
        if missing:
            return error('Missing fields: ' + ', '.join(missing))

        seller = User.query.filter_by(login=payload['sellerLogin'], role='Seller').first()
        if not seller:
            return error('sellerLogin must reference a Seller user')

        if Item.query.get(payload['itemId']):
            return error('itemId already exists')

        item = Item(
            itemId=payload['itemId'],
            itemName=payload['itemName'],
            category=payload.get('category'),
            imageURL=payload.get('imageURL'),
            condition=payload['condition'],
            startingPrice=float(payload['startingPrice']),
            description=payload.get('description'),
            sellerLogin=payload['sellerLogin']
        )
        db.session.add(item)
        db.session.commit()
        return jsonify(item.serialize()), 201

    @app.route('/api/auctions', methods=['GET', 'POST'])
    def auctions():
        if request.method == 'GET':
            return jsonify([auction.serialize() for auction in Auction.query.all()])

        payload = request.get_json() or {}
        required = ['auctionId', 'auctionStatus', 'sellerLogin', 'itemId']
        missing = [k for k in required if not payload.get(k)]
        if missing:
            return error('Missing fields: ' + ', '.join(missing))

        seller = User.query.filter_by(login=payload['sellerLogin'], role='Seller').first()
        if not seller:
            return error('sellerLogin must reference a Seller user')

        item = Item.query.get(payload['itemId'])
        if not item:
            return error('itemId must reference an existing item')

        if Auction.query.get(payload['auctionId']):
            return error('auctionId already exists')

        auction = Auction(
            auctionId=payload['auctionId'],
            auctionStatus=payload['auctionStatus'],
            currentHighestBid=float(payload.get('currentHighestBid', 0.0)),
            sellerLogin=payload['sellerLogin'],
            itemId=payload['itemId']
        )
        db.session.add(auction)
        db.session.commit()
        return jsonify(auction.serialize()), 201

    @app.route('/api/auctions/<auction_id>', methods=['PATCH'])
    def update_auction(auction_id):
        payload = request.get_json() or {}
        if not payload.get('adminLogin'):
            return error('adminLogin is required')

        admin = User.query.filter_by(login=payload['adminLogin'], role='Admin').first()
        if not admin:
            return error('adminLogin must reference an Admin user')

        auction = Auction.query.get(auction_id)
        if not auction:
            return error('auctionId does not exist')

        if 'auctionStatus' in payload:
            auction.auctionStatus = payload['auctionStatus']

        db.session.commit()
        return jsonify(auction.serialize())

    @app.route('/api/bids', methods=['GET', 'POST'])
    def bids():
        if request.method == 'GET':
            return jsonify([bid.serialize() for bid in Bid.query.order_by(Bid.bidTimestamp.desc()).all()])

        payload = request.get_json() or {}
        required = ['bidId', 'bidAmount', 'buyerLogin', 'auctionId']
        missing = [k for k in required if not payload.get(k)]
        if missing:
            return error('Missing fields: ' + ', '.join(missing))

        buyer = User.query.filter_by(login=payload['buyerLogin'], role='Buyer').first()
        if not buyer:
            return error('buyerLogin must reference a Buyer user')

        auction = Auction.query.get(payload['auctionId'])
        if not auction:
            return error('auctionId does not exist')
        if auction.auctionStatus != 'active':
            return error('Auction must be active to place a bid')

        bid_amount = float(payload['bidAmount'])
        if bid_amount <= auction.currentHighestBid:
            return error('bidAmount must be higher than the current highest bid')

        if Bid.query.get(payload['bidId']):
            return error('bidId already exists')

        bid = Bid(
            bidId=payload['bidId'],
            bidAmount=bid_amount,
            buyerLogin=payload['buyerLogin'],
            auctionId=payload['auctionId']
        )
        auction.currentHighestBid = bid_amount
        auction.buyerLogin = payload['buyerLogin']

        db.session.add(bid)
        db.session.commit()
        return jsonify(bid.serialize()), 201

    @app.route('/api/payments', methods=['GET', 'POST'])
    def payments():
        if request.method == 'GET':
            return jsonify([payment.serialize() for payment in Payment.query.all()])

        payload = request.get_json() or {}
        required = ['paymentId', 'amount', 'paymentStatus', 'buyerLogin', 'auctionId']
        missing = [k for k in required if not payload.get(k)]
        if missing:
            return error('Missing fields: ' + ', '.join(missing))

        buyer = User.query.filter_by(login=payload['buyerLogin'], role='Buyer').first()
        if not buyer:
            return error('buyerLogin must reference a Buyer user')

        auction = Auction.query.get(payload['auctionId'])
        if not auction:
            return error('auctionId does not exist')

        if Payment.query.filter_by(auctionId=payload['auctionId']).first():
            return error('auctionId already has payment')

        payment = Payment(
            paymentId=payload['paymentId'],
            amount=float(payload['amount']),
            paymentStatus=payload['paymentStatus'],
            buyerLogin=payload['buyerLogin'],
            auctionId=payload['auctionId']
        )
        db.session.add(payment)
        db.session.commit()
        return jsonify(payment.serialize()), 201

    @app.route('/api/shipments', methods=['GET', 'POST'])
    def shipments():
        if request.method == 'GET':
            return jsonify([shipment.serialize() for shipment in Shipment.query.all()])

        payload = request.get_json() or {}
        required = ['shipmentId', 'address', 'shipmentStatus', 'auctionId']
        missing = [k for k in required if not payload.get(k)]
        if missing:
            return error('Missing fields: ' + ', '.join(missing))

        auction = Auction.query.get(payload['auctionId'])
        if not auction:
            return error('auctionId does not exist')

        if Shipment.query.filter_by(auctionId=payload['auctionId']).first():
            return error('auctionId already has shipment')

        shipment = Shipment(
            shipmentId=payload['shipmentId'],
            address=payload['address'],
            shipmentStatus=payload['shipmentStatus'],
            trackingNumber=payload.get('trackingNumber'),
            auctionId=payload['auctionId']
        )
        db.session.add(shipment)
        db.session.commit()
        return jsonify(shipment.serialize()), 201

    @app.route('/api/seed', methods=['POST'])
    def seed_data():
        entries = []

        users = [
            User(login='seller1', phoneNum='5551234567', role='Seller', password='sellerpass', address='123 Seller St', favoriteCategory='Art'),
            User(login='buyer1', phoneNum='5559876543', role='Buyer', password='buyerpass', address='456 Buyer Ave', favoriteCategory='Collectibles'),
            User(login='admin', phoneNum='5550001111', role='Admin', password='adminpass', address='789 Admin Blvd', favoriteCategory='All')
        ]
        for user in users:
            if not User.query.get(user.login):
                db.session.add(user)
                entries.append(user.login)

        item = Item(
            itemId='item1',
            itemName='Classic vase',
            category='Antiques',
            imageURL='https://placekitten.com/300/200',
            condition='available',
            startingPrice=50.0,
            description='A beautiful porcelain vase.',
            sellerLogin='seller1'
        )
        if not Item.query.get(item.itemId):
            db.session.add(item)
            entries.append(item.itemId)

        auction = Auction(
            auctionId='auction1',
            auctionStatus='active',
            currentHighestBid=50.0,
            sellerLogin='seller1',
            itemId='item1'
        )
        if not Auction.query.get(auction.auctionId):
            db.session.add(auction)
            entries.append(auction.auctionId)

        db.session.commit()
        return jsonify({'seeded': entries})

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5001, debug=True)
